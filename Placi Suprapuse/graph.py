from nod_parcurgere import NodParcurgere
import sys
import queue
import stopit
import time


class Graph:
    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        sir_fisier = f.read()

        linii = sir_fisier.strip().split("\n")
        nr_bile = 0
        harta = []
        for linie in linii:
            coloana = 0
            nivel_harta = []
            while coloana < len(linie):
                placa = linie[coloana]
                final_placa = coloana
                while final_placa < len(linie) and linie[final_placa] == placa:
                    final_placa += 1

                if placa == '*':
                    nr_bile += final_placa - coloana
                nivel_harta.append([coloana, final_placa - 1, placa])
                coloana = final_placa  # urmatoarea placa
            harta.append(nivel_harta)
        self.start = NodParcurgere(harta, None, nr_bile)
        self.nr_noduri = 0
        self.start.elimina_bile(self.start.info[self.start.nr_niveluri-1])
        if self.start.testeaza_scop():
            print("Stare initiala este si stare finala")
            sys.exit(0)

        for idx_nivel, linie in enumerate(harta):
            for idx_placa, placa in enumerate(linie):
                if placa[2] != '.':
                    if not self.start.are_sustinere(idx_nivel, harta[min(idx_nivel + 1, len(harta) - 1)], placa):
                        print("Stare initiala invalida")
                        sys.exit(0)

    @stopit.threading_timeoutable(default="timeout depth first")
    def depth_first(self, t1, fout, nr_solutii_cautate=10):
        # vom simula o stiva prin relatia de parinte a nodului curent
        vizitat = [self.start.info]
        prev_sol = nr_solutii_cautate
        while nr_solutii_cautate > 0:
            nr_solutii_cautate = self.df(NodParcurgere(self.start.info, None, self.start.nr_bile), t1, fout,
                                         nr_solutii_cautate, vizitat)
            if prev_sol == nr_solutii_cautate:
                return
            prev_sol = nr_solutii_cautate

    def df(self, nod_curent, t1, fout, nr_sol_cautate, vizitat):
        # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nr_sol_cautate=0)
        if nr_sol_cautate <= 0:
            return nr_sol_cautate
        # print("Stiva actuala:\n" + (str(nod_curent.afis_drum())))
        # input()
        if nod_curent.testeaza_scop():
            t2 = time.time()
            fout.write(f"Solutie: \n")
            nod_curent.afis_drum(fout)
            fout.write(f"\n\n Timp gasire solutie: {t2 - t1} \n")
            fout.write(f"Numar maxim de noduri in memorie: {self.nr_noduri}\n")
            fout.write("\n----------------\n")
            nr_sol_cautate -= 1
            if nr_sol_cautate <= 0:
                return nr_sol_cautate

            nod_curent = nod_curent.parinte

        l_succesori = nod_curent.genereaza_succesori(nod_curent)
        for succ in l_succesori:
            if nr_sol_cautate != 0 and succ.info not in vizitat:
                vizitat.append(succ.info)
                nr_sol_cautate = self.df(succ, t1, fout, nr_sol_cautate, vizitat)

        return nr_sol_cautate

    @stopit.threading_timeoutable(default="timeout breadth_first")
    def breadth_first(self, t1, fout, nr_solutii_cautate=1):
        # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
        c = queue.Queue()
        c.put(NodParcurgere(self.start.info, None, self.start.nr_bile))
        n_bile = sys.maxsize

        while not c.empty():
            nod_curent = c.get()
            while nod_curent.nr_bile > n_bile:
                nod_curent = c.get()

            if nod_curent.testeaza_scop():
                t2 = time.time()
                fout.write("Solutie:\n")
                nod_curent.afis_drum(fout)
                fout.write(f"\n\n Timp gasire solutie: {t2 - t1} \n")
                fout.write(f"Numar maxim de noduri in memorie: {self.nr_noduri}\n")
                fout.write("\n----------------\n")
                nr_solutii_cautate -= 1
                if nr_solutii_cautate == 0:
                    return
            l_succesori = nod_curent.genereaza_succesori("euristica1")
            nr_succ_noi = len(l_succesori)
            self.nr_noduri += nr_succ_noi
            for succ in l_succesori:
                c.put(succ)

    #
    @stopit.threading_timeoutable(default="timeout dfi")
    def depth_first_iterativ(self, t1, fout, nr_solutii_cautate=1):
        for i in range(1, self.nr_noduri + 2):
            if nr_solutii_cautate == 0:
                return
            fout.write(f"**************\nAdancime maxima: {i}")
            nr_solutii_cautate = self.dfi(NodParcurgere(self.start.info, None, self.start.nr_bile), t1, fout,
                                          3, nr_solutii_cautate)

    def dfi(self, nod_curent, t1, fout,adancime, nr_solutii_cautate=10):
        if adancime == 1 and nod_curent.testeaza_scop():
            t2 = time.time()
            fout.write("Solutie: \n")
            nod_curent.afis_drum(fout)
            fout.write(f"\n\n Timp gasire solutie: {t2 - t1} \n")
            fout.write(f"Numar maxim de noduri in memorie: {self.nr_noduri}\n")
            fout.write("\n----------------\n")
            nr_solutii_cautate -= 1
            if nr_solutii_cautate == 0:
                return nr_solutii_cautate
        if adancime > 1:
            l_succesori = nod_curent.genereaza_succesori()
            for succ in l_succesori:
                if nr_solutii_cautate != 0:
                    nr_solutii_cautate = self.dfi(succ, t1, fout, adancime - 1, nr_solutii_cautate)
        return nr_solutii_cautate

    @stopit.threading_timeoutable(default="timeout a_star")
    def a_star(self, t1, fout, euristica, nr_solutii_cautate=10):
        # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
        c = queue.PriorityQueue()
        c.put(NodParcurgere(self.start.info, None, self.start.nr_bile, 0, self.start.calculeaza_h(euristica)))

        while not c.empty():
            nod_curent = c.get()

            if nod_curent.testeaza_scop():
                t2 = time.time()
                fout.write("Solutie: \n")
                nod_curent.afis_drum(fout)
                fout.write(f"\n\n Timp gasire solutie: {t2 - t1} \n")
                fout.write(f"Numar maxim de noduri in memorie: {self.nr_noduri}\n")
                fout.write("\n----------------\n")
                nr_solutii_cautate -= 1
                if nr_solutii_cautate == 0:
                    return
            l_succesori = nod_curent.genereaza_succesori()
            for s in l_succesori:
                c.put(s)

    @stopit.threading_timeoutable(default="timeout a_star_optimizat")
    def a_star_optimizat(self, t1, fout, euristica):
        # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
        l_open = [NodParcurgere(self.start.info, None, self.start.nr_bile, 0, self.start.calculeaza_h(euristica))]

        # l_open contine nodurile candidate pentru expandare (este echivalentul lui c din A* varianta neoptimizata)

        # l_closed contine nodurile expandate
        l_closed = []
        while len(l_open) > 0:
            nod_curent = l_open.pop(0)
            l_closed.append(nod_curent)
            if nod_curent.testeaza_scop():
                t2 = time.time()
                fout.write("Solutie: \n")
                nod_curent.afis_drum(fout)
                fout.write(f"\n\n Timp gasire solutie: {t2 - t1} \n")
                fout.write(f"Numar maxim de noduri in memorie: {self.nr_noduri}\n")
                fout.write("\n----------------\n")
                return
            l_succesori = nod_curent.genereaza_succesori()
            for s in l_succesori:
                gasitC = False
                for nodC in l_open:
                    if s.info == nodC.info:
                        gasitC = True
                        if s.f >= nodC.f:
                            l_succesori.remove(s)
                        else:  # s.f<nodC.f
                            l_open.remove(nodC)
                        break
                if not gasitC:
                    for nodC in l_closed:
                        if s.info == nodC.info:
                            if s.f >= nodC.f:
                                l_succesori.remove(s)
                            else:  # s.f<nodC.f
                                l_closed.remove(nodC)
                            break
            for s in l_succesori:
                i = 0
                gasit_loc = False
                for i in range(len(l_open)):
                    # diferenta fata de UCS e ca ordonez crescator dupa f
                    # daca f-urile sunt egale ordonez descrescator dupa g
                    if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].g <= s.g):
                        gasit_loc = True
                        break
                if gasit_loc:
                    l_open.insert(i, s)
                else:
                    l_open.append(s)

    @stopit.threading_timeoutable(default="timeout a_star_optimizat")
    def ida_star(self, t1, fout, euristica, nr_sol_cautate=10):

        nod_start = NodParcurgere(self.start.info, None, self.start.nr_bile, 0, self.start.calculeaza_h(euristica))
        limita = nod_start.f
        while True:
            fout.write(f"Limita de pornire: {limita}\n")
            nr_sol_cautate, rez = self.construieste_drum(t1, fout, nod_start, limita, nr_sol_cautate)
            if rez == "gata":
                break
            if rez == float('inf'):
                fout.write("Nu mai exista solutii!\n")
                break
            limita = rez
            fout.write(f">>> Limita noua: {limita}\n")

    def construieste_drum(self, t1, fout, nod_curent, limita, nr_sol_cautate):
        fout.write(f"A ajuns la:\n{nod_curent}")
        if nod_curent.f > limita:
            return nr_sol_cautate, nod_curent.f
        if nod_curent.testeaza_scop() and nod_curent.f == limita:
            t2 = time.time()
            fout.write("Solutie: \n")
            nod_curent.afis_drum()
            fout.write(f"\n\n Timp gasire solutie: {t2 - t1} \n")
            fout.write(f"Numar maxim de noduri in memorie: {self.nr_noduri}\n")
            fout.write("\n-------------------------\n")
            nr_sol_cautate -= 1
            if nr_sol_cautate == 0:
                return 0, "gata"
        l_succesori = nod_curent.genereaza_succesori()
        minim = float('inf')
        for s in l_succesori:
            nr_sol_cautate, rez = self.construieste_drum(t1, fout, s, limita, nr_sol_cautate)
            if rez == "gata":
                return 0, "gata"
            fout.write(f"Compara {rez} cu {minim}\n")
            if rez < minim:
                minim = rez
                fout.write(f"Noul minim: {minim}\n")
        return nr_sol_cautate, minim

from nod_parcurgere import NodParcurgere
import sys
import queue


# placile, bilele si spatiile sunt reprezentate ca tupluri de 3 elemente
# tuplu[0] -> index start
# tuplu[1] -> index stop
# tuplu[2] -> elementul (caracter)
class Graph:
    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        sir_fisier = f.read()
        try:
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
                    nivel_harta.append((coloana, final_placa - 1, placa))
                    coloana = final_placa  # urmatoarea placa
                harta.append(nivel_harta)
            print(*harta, sep="\n")
            self.start = NodParcurgere(harta, None, nr_bile)
        except:
            print("Eroare la parsare!")
            sys.exit(0)  # iese din program
    #
    # def depth_first(self, nr_solutii_cautate=10):
    #     # vom simula o stiva prin relatia de parinte a nodului curent
    #     vizitat = [self.start.info]
    #     prev_sol = nr_solutii_cautate
    #     while nr_solutii_cautate > 0:
    #         nr_solutii_cautate = self.df(NodParcurgere(self.start.info, None, self.start.nr_bile), nr_solutii_cautate, vizitat)
    #         if prev_sol == nr_solutii_cautate:
    #             return
    #         else:
    #             prev_sol = nr_solutii_cautate
    #
    # def df(self, nod_curent, nr_sol_cautate, vizitat):
    #     # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
    #     if nr_sol_cautate <= 0:
    #         return nr_sol_cautate
    #     # print("Stiva actuala:\n" + (str(nod_curent.afis_drum())))
    #     # input()
    #     if nod_curent.testeaza_scop():
    #         print(f"Solutie: ", end="\n")
    #         nod_curent.afis_drum()
    #         print("\n----------------\n")
    #         # input()
    #         nr_sol_cautate -= 1
    #         if nr_sol_cautate <= 0:
    #             return nr_sol_cautate
    #
    #         nod_curent = nod_curent.parinte
    #
    #     lSuccesori = nod_curent.genereaza_succesori(nod_curent)
    #     for succ in lSuccesori:
    #         if nr_sol_cautate != 0 and succ.info not in vizitat:
    #             vizitat.append(succ.info)
    #             nr_sol_cautate = self.df(succ, nr_sol_cautate, vizitat)
    #
    #     return nr_sol_cautate
    #
    # def bf(self, nr_solutii_cautate=1):
    #     # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    #     c = queue.Queue()
    #     c.put(NodParcurgere(self.start.info, None, self.start.nr_bile))
    #     print(self.start)
    #     n_bile = sys.maxsize
    #
    #     while not c.empty():
    #         # print("Coada actuala: " + str(c))
    #         # input()
    #         nod_curent = c.get()
    #         while nod_curent.nr_bile > n_bile:
    #             nod_curent = c.get()
    #
    #         n_bile = min(n_bile, nod_curent.nr_bile)
    #         print(nod_curent)
    #
    #         if nod_curent.testeaza_scop():
    #             print("Solutie:")
    #             nod_curent.afis_drum()
    #             print("\n----------------\n")
    #             nr_solutii_cautate -= 1
    #             if nr_solutii_cautate == 0:
    #                 return
    #         lSuccesori = nod_curent.genereaza_succesori("f")
    #         for succ in lSuccesori:
    #             if succ.nr_bile <= n_bile:
    #                 c.put(succ)
    #
    # def depth_first_iterativ(self, nr_solutii_cautate=1):
    #     for i in range(1, self.nr_noduri + 1):
    #         if nr_solutii_cautate == 0:
    #             return
    #         print("**************\nAdancime maxima: ", i)
    #         nr_solutii_cautate = self.dfi(NodParcurgere(self.start.info, None), i, nr_solutii_cautate)
    #
    # def dfi(self, nod_curent, adancime, nr_solutii_cautate):
    #     print("Stiva actuala: " + "->".join(nod_curent.obtine_drum()))
    #     input()
    #     if adancime == 1 and nod_curent.testeaza_scop():
    #         print("Solutie: ", end="")
    #         nod_curent.afis_drum()
    #         print("\n----------------\n")
    #         input()
    #         nr_solutii_cautate -= 1
    #         if nr_solutii_cautate == 0:
    #             return nr_solutii_cautate
    #     if adancime > 1:
    #         lSuccesori = nod_curent.genereaza_succesori()
    #         for sc in lSuccesori:
    #             if nr_solutii_cautate != 0:
    #                 nr_solutii_cautate = self.dfi(sc, adancime - 1, nr_solutii_cautate)
    #     return nr_solutii_cautate
    #
    # def a_star(self, nrSolutiiCautate):
    #     # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    #     c = [NodParcurgere(self.indiceNod(self.start), self.start, None, 0, gr.calculeaza_h(gr.start))]
    #
    #     while len(c) > 0:
    #         print("Coada actuala: " + str(c))
    #         input()
    #         nodCurent = c.pop(0)
    #
    #         if gr.testeaza_scop(nodCurent):
    #             print("Solutie: ")
    #             nodCurent.afisDrum()
    #             print("\n----------------\n")
    #             input()
    #             nrSolutiiCautate -= 1
    #             if nrSolutiiCautate == 0:
    #                 return
    #         lSuccesori = gr.genereazaSuccesori(nodCurent)
    #         for s in lSuccesori:
    #             i = 0
    #             gasit_loc = False
    #             for i in range(len(c)):
    #                 # diferenta fata de UCS e ca ordonez dupa f
    #                 if c[i].f > s.f:
    #                     gasit_loc = True
    #                     break
    #             if gasit_loc:
    #                 c.insert(i, s)
    #             else:
    #                 c.append(s)

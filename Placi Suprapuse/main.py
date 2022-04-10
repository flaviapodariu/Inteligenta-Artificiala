import copy
import sys
import os
import time


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def testeaza_scop(self):
        for nivel in self.info:
            for element in nivel:
                if element == '*':
                    return False
        return True

    def obtine_drum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afis_drum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtine_drum()
        for i, nod in enumerate(l):
            print(i + 1, ")\n", str(nod), sep="")
        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
            print("Lungime: ", len(l))
        return len(l)

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return sir

    def __str__(self):
        sir = ""
        for linie in self.info:
            sir += " ".join([str(elem) for elem in linie]) + "\n"
        sir += "Cost " + str(self.f) + "\n"
        return sir

    def genereaza_succesori(self, tip_euristica="euristica banala"):
        lista_succesori = []
        if tip_euristica == "euristica_banala":
            nivel_start = 0
        else:
            # caut succesorii de la primul nivel pe care gasesc o bila
            nivel_start = -1
            for i, nivel in enumerate(self.info):
                if '*' in nivel:
                    nivel_start = i
                    break

        for linie in range(nivel_start, len(self.info)):  # caut succesori incepand cu nivelul primei bile
            idx_bila_n = -1
            for i, elem in enumerate(self.info[linie]):
                if elem == '.':
                    idx_spatiu = i
                    if self.info[linie][max(nivel_start, i - 1)] != '*' \
                            and 0 < idx_spatiu <= len(self.info[linie]) - 1:  # daca i = 0, i-1 out of bounds
                        directie = -1  # stanga
                        succesor = self.succesor_caz_bloc(idx_spatiu,
                                                          linie, directie)
                        if succesor is not None:
                            lista_succesori.append(succesor)

                    if self.info[linie][min(i + 1, len(self.info) - 1)] != '*' \
                            and 0 <= idx_spatiu < len(self.info[linie]) - 1:
                        directie = 1  # dreapta
                        succesor = self.succesor_caz_bloc(idx_spatiu,
                                                          linie, directie)
                        if succesor is not None:
                            lista_succesori.append(succesor)

                elif elem == '*' and i > idx_bila_n:
                    idx_bila_1 = i
                    idx_bila_n = self.index_bila_n(self.info[linie], idx_bila_1)
                    nr_bile = idx_bila_n - idx_bila_1 + 1

                    if self.info[linie][i - 1] != '.' \
                            and self.info[linie][idx_bila_n + 1] != '.':
                        continue  # bila este blocata intre blocuri
                    if self.info[linie][i - 1] == '.' \
                            and self.info[linie][idx_bila_n + 1] == '.':
                        continue

                    if self.info[linie][i - 1] != '.':  # mut bila spre dreapta
                        directie = 1
                    else:  # mut bila spre stanga
                        directie = -1

                    start_bloc = self.index_nou_start(self.info[linie], i - 1, -directie, False)
                    marime_bloc = abs(idx_bila_1 - start_bloc)

                    succesor = self.succesor_caz_bila(nr_bile, idx_bila_1,
                                                      idx_bila_n, linie, directie, marime_bloc)
                    if succesor is not None:
                        lista_succesori.append(succesor)


        return lista_succesori

    def mutare_bila(self, harta, coord_bila, coord_bila_noi, directie):
        """

        :param harta: nodul curent
        :param coord_bila: tuplu care contine linia si coloana bilei inainte de mutare
        :param coord_bila_noi: tuplu care contine linia si coloana bilei dupa mutare
        :param directie: -1 pt stanga, 1 pt dreapta
        :return: harta noua
        """
        if coord_bila[0] == coord_bila_noi[0]:  # bila nu cade pe alt nivel
            h = copy.deepcopy(harta[coord_bila[0]])

            if directie == 1:
                h = h[:coord_bila[1]] + '.' + '*' + h[coord_bila[1] + 2:]
            else:
                h = h[:coord_bila[1] - 1] + '*' + '.' + h[coord_bila[1] + 1:]
            harta[coord_bila[0]] = h
        else:
            niv_bila = copy.deepcopy(harta[coord_bila[0]])
            niv_bila_nou = copy.deepcopy(harta[coord_bila_noi[0]])

            niv_bila = niv_bila[:coord_bila[1]] + '.' + niv_bila[coord_bila[1] + 1:]
            niv_bila_nou = niv_bila_nou[:coord_bila_noi[1]] + '*' + niv_bila_nou[coord_bila_noi[1] + 1:]

            harta[coord_bila[0]] = niv_bila
            harta[coord_bila_noi[0]] = niv_bila_nou

        return harta

    def index_bila_n(self, nivel, idx_bila_1):
        prev = nivel[idx_bila_1]
        idx = idx_bila_1
        for i in range(idx, len(nivel)):
            if nivel[i] != prev:
                return i - 1  # indexul ultimei bile
        return idx  # indexul bilei curente (exista doar o bila in lant)

    def index_nou_start(self, nivel, j, directie, flag_bloc=True):
        """
        :param nivel: nivelul pe care caut
        :param j: indexul spatiului
        :param directie: -1 pt cautare spre stanga, 1 pt dreapta
        :param flag_bloc: True -> index spatiu nou, False -> index spatiu nou dupa ce un bloc impinge bile
                                                            (indexul lui bloc[0])
        :return: indexul primei bucati din blocul pe care il voi muta/ noul index pt spatiu
                 -1 pt eroare
        """

        if directie != -1 and directie != 1:
            return -1

        j += directie
        prev = nivel[j]
        if prev == '*' and flag_bloc:
            return
        while nivel[j] == prev:
            if j == len(nivel) - 1 or j == 0:
                return j
            j += directie

        return j - directie

    def mutare_spatiu(self, harta, nivel, idx_spatiu, idx_spatiu_nou):
        # cazul in care tragem un bloc de sub bila => bila cade pe urm nivel
        if harta[max(0, nivel - 1)][idx_spatiu_nou] != '*':
            a = '.'
        else:
            a = '*'
            harta[nivel - 1] = harta[nivel - 1][:idx_spatiu_nou] + '.' + harta[nivel - 1][idx_spatiu_nou + 1:]

        b = copy.deepcopy(harta[nivel][idx_spatiu_nou])
        if idx_spatiu > idx_spatiu_nou:  # mut spatiul spre stanga
            harta[nivel] = harta[nivel][:idx_spatiu_nou] + a + \
                           harta[nivel][idx_spatiu_nou + 1: idx_spatiu] + b + harta[nivel][idx_spatiu + 1:]
        elif idx_spatiu < idx_spatiu_nou:
            harta[nivel] = harta[nivel][:idx_spatiu] + b + \
                           harta[nivel][idx_spatiu + 1: idx_spatiu_nou] + a + harta[nivel][idx_spatiu_nou + 1:]

        return harta

    def bila_sparta_alunecare(self, nod_curent, nivel, idx_spatiu):
        # stim ca nod_curent.info[nivel][idx_spatiu] este un spatiu
        if 0 < nivel < len(nod_curent.info) - 1:
            return nod_curent.info[nivel - 1][idx_spatiu] == '*' \
                   and nod_curent.info[nivel + 1][idx_spatiu] == '.'
        return False  # bila e maxim pe ultimul nivel => nu poate fi sparta

    def bila_sparta_impingere(self, nod_curent, nivel, idx_bila_impinsa):
        if nivel < len(nod_curent.info) - 2:
            return nod_curent.info[nivel + 1][idx_bila_impinsa] == '.' \
                   and nod_curent.info[nivel + 2][idx_bila_impinsa] == '.'
        return False

    def succesor_caz_bloc(self, idx_spatiu, nivel, directie):
        if directie != -1 and directie != 1:
            return

        copie_harta = copy.deepcopy(self)
        idx_spatiu_nou = self.index_nou_start(copie_harta.info[nivel], idx_spatiu, directie)
        if idx_spatiu_nou is None:
            return

        if self.bila_sparta_alunecare(copie_harta, nivel, idx_spatiu_nou):
            return

        if copie_harta.info[nivel][idx_spatiu] == copie_harta.info[nivel][idx_spatiu_nou]:
            return

        copie_harta.info = self.mutare_spatiu(copie_harta.info, nivel, idx_spatiu, idx_spatiu_nou)

        lung_bloc = abs(idx_spatiu - idx_spatiu_nou)
        col_bloc = min(idx_spatiu, idx_spatiu_nou) - directie
        copie_harta.info[len(copie_harta.info) - 1] = self.elimina_bile(copie_harta.info[len(copie_harta.info) - 1])

        if nivel == len(copie_harta.info) - 1 or self.are_sustinere(copie_harta.info[nivel + 1], col_bloc, lung_bloc):
            return NodParcurgere(copie_harta.info, self, lung_bloc + 1, self.f)
        return

    def succesor_caz_bila(self, nr_bile, bila_start, bila_stop, nivel, directie, marime_bloc):
        """

        :param nr_bile: nr de bile din lant
        :param bila_start: prima bila de langa blocul care va muta bilele
        :param bila_stop: cea mai departata bila de bloc
        :param nivel: nivelul din harta
        :param directie: -1 pt stanga, 1 pt dreapta
        :param marime_bloc: marimea blocului care va muta bilele (pt calc costului)
        :return: starea hartii dupa mutarea bilei/ bilelor
        """
        if directie == -1:
            ultima_bila = bila_start
            prima_bila = bila_stop
        else:
            ultima_bila = bila_stop
            prima_bila = bila_start

        copie_harta = copy.deepcopy(self)
        copie_harta.info = self.harta_bile_impinse(copie_harta.info, nivel, ultima_bila, nr_bile, directie)
        copie_harta.info = self.mutare_spatiu(copie_harta.info, nivel, prima_bila,
                                              prima_bila - (directie * marime_bloc))

        copie_harta.info[len(copie_harta.info) - 1] = self.elimina_bile(copie_harta.info[len(copie_harta.info) - 1])

        return NodParcurgere(copie_harta.info, self, 2 * (1 + marime_bloc), self.f)

    def elimina_bile(self, nivel):
        nivel = nivel.replace('*', '.')
        return nivel

    def are_sustinere(self, nivel_urm, coloana, bloc_size):
        """

        :param nivel_urm: nivelul de sub bloculul pe care vreau sa il mut
        :param coloana: coloana blocului pe care vreau sa il mut
        :param bloc_size: lungimea blocului pe care vreau sa il mut
        :return: True daca exista o alta valoare decat '.' (are sustinere de la alt bloc)
                 False* altfel
        """
        for elem in range(coloana, coloana + bloc_size):
            if nivel_urm[elem] != '.':
                return True
        return False

    def harta_bile_impinse(self, harta, nivel, idx_ultima_bila, nr_bile, directie):
        if directie != -1 and directie != 1:
            return -1

        if nivel > max(0, len(harta) - 3):
            return

        coloana = idx_ultima_bila
        for _ in range(nr_bile):
            if len(harta) > 2 and harta[nivel + 1][coloana + directie] == '.' \
                    and harta[nivel + 2][coloana + directie] == '.':
                return
            elif harta[nivel + 1][coloana + directie] == '.':
                harta = self.mutare_bila(harta, (nivel, coloana), (nivel + 1, coloana + directie), directie)
            else:
                harta = self.mutare_bila(harta, (nivel, coloana), (nivel, coloana + directie), directie)
            coloana -= directie

        return harta


class Graph:
    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        sirFisier = f.read()
        try:
            linii = sirFisier.strip().split("\n")
            self.start = NodParcurgere([x for x in linii], None)
        except:
            print("Eroare la parsare!")
            sys.exit(0)  # iese din program

    def depth_first(self, nr_solutii_cautate=10):
        # vom simula o stiva prin relatia de parinte a nodului curent
        vizitat = [self.start.info]
        while nr_solutii_cautate > 0:
            self.df(NodParcurgere(self.start.info, None), nr_solutii_cautate, vizitat)

    def df(self, nod_curent, nr_sol_cautate, vizitat):
        # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
        if nr_sol_cautate <= 0:
            return nr_sol_cautate

        # print("Stiva actuala:\n" + (str(nod_curent.afis_drum())))
        # input()
        if nod_curent.testeaza_scop():
            print(f"Solutie: ", end="\n")
            nod_curent.afis_drum()
            print("\n----------------\n")
            input()
            nr_sol_cautate -= 1
            if nr_sol_cautate == 0:
                return nr_sol_cautate

        lSuccesori = nod_curent.genereaza_succesori(nod_curent)
        for succ in lSuccesori:
            if nr_sol_cautate != 0 and succ.info not in vizitat:
                vizitat.append(succ.info)
                nr_sol_cautate = self.df(succ, nr_sol_cautate, vizitat)

        return nr_sol_cautate


# input, output, NSOL, timeout
# if len(sys.argv) != 5:
#     print("Numar de argumente gresit!")
#     sys.exit(0)
# else:
#     input_folder = os.getcwd() + sys.argv[1]
#     output_folder = os.getcwd() + sys.argv[2]
#     NSOL = sys.argv[3]
#     timeout = sys.argv[4]


# lista_inputuri = os.listdir(input_folder)
#
# for input_file in lista_inputuri:
#     # print(input_file)
#     g = Graph(input_folder + "/" + input_file)

g = Graph("inputs/no_ans.txt")
# l = g.start.genereaza_succesori()
# for nod in l:
    # print(nod)
g.depth_first()

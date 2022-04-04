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

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
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
        sir += "\n"
        return sir


class Graph:
    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        sirFisier = f.read()
        try:
            linii = sirFisier.strip().split("\n")
            self.start = [x for x in linii]

            print(self.start, sep='\n')
        except:
            print("Eroare la parsare!")
            sys.exit(0)  # iese din program

    def testeaza_scop(self, nod_curent):
        for nivel in nod_curent:
            for element in nivel:
                if element == '*':
                    return False
        return True

    def are_sustinere(self, linie, coloana, bloc_size):
        '''

        :param linie: linia blocului pe care vreau sa il mut
        :param coloana: coloana blocului pe care vreau sa il mut
        :param bloc_size: lungimea blocului pe care vreau sa il mut
        :return: True daca exista o alta valoare decat '.' (are sustinere de la alt bloc)
                 False* altfel
        '''
        for componenta_bloc in range(coloana, coloana + bloc_size):
            if componenta_bloc != '.':
                return True
        return False

    def index_nou_spatiu(self, nivel, j, directie):
        """
        :param nivel: nivelul pe care caut
        :param j: indexul spatiului
        :param directie: -1 pt cautare spre stanga, 1 pt dreapta
        :return: indexul primei bucati din blocul pe care il voi muta/ noul index pt spatiu
                 -1 pt eroare
        """

        if directie != -1 and directie != 1:
            return -1

        j += directie
        prev = nivel[j]
        while nivel[j] == prev:
            if j == len(nivel) - 1:
                return j
            j += directie

        return j - directie

    def mutare_spatiu(self, nivel, idx_spatiu, idx_spatiu_nou):
        a = copy.deepcopy(nivel[idx_spatiu])
        b = copy.deepcopy(nivel[idx_spatiu_nou])
        if idx_spatiu > idx_spatiu_nou:  # mut spatiul spre stanga
            nivel = nivel[:idx_spatiu_nou] + a + nivel[idx_spatiu_nou + 1: idx_spatiu] + b + nivel[idx_spatiu + 1:]
        else:
            nivel = nivel[:idx_spatiu] + b + nivel[idx_spatiu + 1: idx_spatiu_nou] + a + nivel[idx_spatiu_nou + 1:]

        return nivel

    def genereaza_succesori(self, nod_curent, tip_euristica="euristica banala"):
        listaSuccesori = []
        # caut succesorii de la primul nivel in care gasesc bila
        nivelStart = -1
        for i, nivel in enumerate(nod_curent.info):
            if '*' in nivel:
                nivelStart = i
                break

        for linie in range(nivelStart, len(nod_curent.info)):  # caut succesori incepand cu nivelul primei bile
            for i, elem in enumerate(nod_curent.info[linie]):
                if elem == '.':
                    idx_spatiu = i
                else:
                    continue

                if 0 < idx_spatiu < len(nod_curent.info[linie]) - 1:
                    copieHartaSt = copy.deepcopy(nod_curent.info)
                    idx_spatiu_nou = self.index_nou_spatiu(copieHartaSt[linie], idx_spatiu, -1)
                    copieHartaSt[linie] = self.mutare_spatiu(copieHartaSt[linie], idx_spatiu, idx_spatiu_nou)
                    print(copieHartaSt[linie])

                    copieHartaDr = copy.deepcopy(nod_curent.info)
                    idx_spatiu_nou = self.index_nou_spatiu(copieHartaDr[linie], idx_spatiu, 1)
                    copieHartaDr[linie] = self.mutare_spatiu(copieHartaDr[linie], idx_spatiu, idx_spatiu_nou)
                    print(copieHartaDr[linie])


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
g.genereaza_succesori(NodParcurgere(g.start, None, 0))

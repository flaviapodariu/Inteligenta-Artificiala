import copy
from bisect import bisect_right, bisect_left


class NodParcurgere:
    def __init__(self, info, parinte, nr_bile, cost=0, h=0):
        self.info = info
        self.lungime = 0 if len(self.info) <= 0 else len(self.info[0])  # lungime nivel
        self.nr_niveluri = len(self.info)
        self.parinte = parinte
        self.nr_bile = nr_bile
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def testeaza_scop(self):
        return True if self.nr_bile == 0 else False

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
            for elem in linie:
                lungime = elem[1] - elem[0] + 1
                for _ in range(lungime):
                    sir += elem[2]
            sir += "\n"
        sir += "Cost " + str(self.f) + "\n"
        return sir

    def genereaza_succesori(self, tip_euristica="euristica banala"):
        lista_succesori = []
        for idx_nivel, nivel in enumerate(self.info):
            for idx_placa, placa in enumerate(nivel):
                if placa[2] == '*':
                    placa_prec = nivel[max(0, idx_placa - 1)][2]
                    placa_urm = nivel[min(idx_placa + 1, len(nivel) - 1)][2]

                    if placa_prec == '.' and placa_urm == '.':
                        # cazul in care nu exista placi pt a impinge bilele
                        continue

                    if placa_prec != '.' and placa_urm != '.':
                        # cazul in care bila/bilele sunt blocate intre placi
                        continue
                    elif placa_prec != '.':
                        # pot impinge bila spre dreapta
                        directie = 1
                    else:
                        # pot impinge bila spre stanga
                        directie = -1
                    lista_succesori.append(self.mutare_bile(idx_nivel, idx_placa, directie))

                # elif placa[2] == '.':

        return lista_succesori

    def bila_sparta_impingere(self, idx_nivel, idx_placa, directie):
        # stim ca self.info[idx_nivel][idx_placa+directie] e un spatiu
        # pt ca apelam functia din mutare_bile()
        if directie == 1:
            idx_spatiu = self.info[idx_nivel][idx_placa][1] + directie
            idx_placa_niv1 = bisect_right(self.info[idx_nivel + 1], idx_spatiu, key=lambda x: x[0])

        else:
            idx_spatiu = self.info[idx_nivel][idx_placa][0] + directie
            idx_placa_niv1 = bisect_left(self.info[idx_nivel + 1], idx_spatiu, key=lambda x: x[0])

        if len(self.info) < 3:
            return False, idx_placa_niv1 - 1

        print(idx_placa_niv1)
        if self.info[idx_nivel + 1][idx_placa_niv1][1] >= idx_spatiu and self.info[idx_nivel + 1][idx_placa_niv1][
            2] == '.':
            if directie == 1:
                idx_placa_niv2 = bisect_right(self.info[idx_nivel + 2], idx_spatiu, key=lambda x: x[0])
            else:
                idx_placa_niv2 = bisect_left(self.info[idx_nivel + 2], idx_spatiu, key=lambda x: x[0])

            if self.info[idx_nivel + 2][idx_placa_niv2][1] >= idx_spatiu and self.info[idx_nivel + 2][idx_placa_niv2][
                2] == '.':
                return True, -1

            return False, idx_placa_niv1 - 1  # a intrat in primul if deci bila cade
        return False, -1  # bila nu cade

    def mutare_bile(self, idx_nivel, idx_placa, directie):
        copie = copy.deepcopy(self.info)
        nr_elem_nivel = len(copie) - 1

        prev = copie[idx_nivel][idx_placa - 1]
        urm = copie[idx_nivel][idx_placa + 1]
        lung_placa_cost = prev[1] - prev[0] + 1 if directie == 1 else urm[1] - urm[0] + 1
        print(copie)
        test_bila = self.bila_sparta_impingere(idx_nivel, idx_placa, directie)
        if test_bila[0]:
            return
        elif test_bila[1] != -1:
            placa_schimb = copie[idx_nivel + 1][test_bila[1]]
            idx_bila_cazuta = copie[idx_nivel][idx_placa][0] - 1 if directie == -1 else copie[idx_nivel][idx_placa][
                                                                                            1] + 1

            if placa_schimb[0] == placa_schimb[1]:
                placa_schimb[2] = '*'
            else:
                bila = [idx_bila_cazuta, idx_bila_cazuta, '*']
                copie[idx_nivel + 1].insert(test_bila[1], bila)
                if directie == 1:
                    spatiu = [copie[idx_nivel][idx_placa - 1][0], copie[idx_nivel][idx_placa - 1][0], '.']
                    placa_schimb[0] += directie
                else:
                    spatiu = [copie[idx_nivel][idx_placa + 1][1], copie[idx_nivel][idx_placa + 1][1],
                              '.']  # check for indexing problems
                    placa_schimb[1] += directie

                if placa_schimb[0] > placa_schimb[1]:
                    copie[idx_nivel + 1].pop(test_bila[1])

                if copie[idx_nivel][min(idx_placa - 2 * directie, len(copie[idx_nivel]) - 1)][2] != '.':
                    copie[idx_nivel].insert(min(idx_placa - 2 * directie, len(copie[idx_nivel])), spatiu)
                    # indexul placii cu bile nu se va mai muta dupa noua inserare (inserarea se va face dupa idx_placa)
                else:
                    copie[idx_nivel][idx_placa - 2 * directie][1] += 1

        copie[idx_nivel][idx_placa][0] += directie
        copie[idx_nivel][idx_placa][1] += directie

        prec = copie[idx_nivel][max(0, idx_placa - 1)]
        urm = copie[idx_nivel][min(idx_placa + 1, len(copie[idx_nivel]) - 1)]

        if directie == 1:
            prec[0] += directie
            prec[1] += directie
            # urm[0] += directie

            if urm[0] > urm[1]:
                # in urma mutarii, spatiul a fost acoperit integral de bile
                copie[idx_nivel].pop(idx_placa + 1)

        if directie == -1:
            urm[0] += directie
            urm[1] += directie

            if prec[0] > prec[1]:
                copie[idx_nivel].pop(idx_placa - 1)

        copie[idx_nivel].pop(idx_placa)
        copie[nr_elem_nivel], nr_bile = self.elimina_bile(copie[nr_elem_nivel])
        print(copie)
        return NodParcurgere(copie, self, nr_bile, 2 * (1 + lung_placa_cost))

    def bila_sparta_alunecare(self, nod_curent, nivel, idx_spatiu):
        # stim ca nod_curent.info[nivel][idx_spatiu] este un spatiu
        if 0 < nivel < self.nr_niveluri - 1:
            return nod_curent.info[nivel - 1][idx_spatiu] == '*' \
                   and nod_curent.info[nivel + 1][idx_spatiu] == '.'
        return False  # bila e maxim pe ultimul nivel => nu poate fi sparta

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
        copie_harta.info[self.nr_niveluri - 1], n_bile = self.elimina_bile(copie_harta.info[self.nr_niveluri - 1])

        if nivel == self.nr_niveluri - 1 or self.are_sustinere(copie_harta.info[nivel + 1], col_bloc, lung_bloc):
            return NodParcurgere(copie_harta.info, self, n_bile, lung_bloc + 1, self.f)
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
        if copie_harta.info is None:
            return
        copie_harta.info[self.nr_niveluri - 1], n_bile = self.elimina_bile(copie_harta.info[self.nr_niveluri - 1])

        return NodParcurgere(copie_harta.info, self, n_bile, 2 * (1 + marime_bloc), self.f)

    def elimina_bile(self, nivel):
        bile = 0
        for elem in nivel:
            if elem[2] == '*':
                elem[2] = '.'
                bile = elem[1] - elem[0] + 1
        return nivel, self.nr_bile - bile

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
            return
        if harta is None:
            return

        if nivel > max(0, self.nr_niveluri - 3):
            return

        coloana = idx_ultima_bila
        for _ in range(nr_bile):
            # a cazut bila
            if len(harta) > 2 and harta[nivel + 1][coloana + directie] == '.' \
                    and harta[nivel + 2][coloana + directie] == '.':
                return
            elif harta[nivel + 1][coloana + directie] == '.':
                harta = self.mutare_bila(harta, (nivel, coloana), (nivel + 1, coloana + directie), directie)
            else:
                harta = self.mutare_bila(harta, (nivel, coloana), (nivel, coloana + directie), directie)
            coloana -= directie

        return harta

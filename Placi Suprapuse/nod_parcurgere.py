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

                placa_prec = nivel[max(0, idx_placa - 1)][2]
                placa_urm = nivel[min(idx_placa + 1, len(nivel) - 1)][2]
                if placa[2] == '*':
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

                elif placa[2] == '.':
                    succ_st = self.mutare_placa(idx_nivel, idx_placa + 1, -1)
                    if succ_st is not None:
                        lista_succesori.append(succ_st)
                    succ_dr = self.mutare_placa(idx_nivel, idx_placa - 1, 1)
                    if succ_dr is not None:
                        lista_succesori.append(succ_dr)

        return lista_succesori

    def mutare_placa(self, idx_nivel, idx_placa, directie):
        if self.bila_sparta_alunecare(idx_nivel, self.info[idx_nivel][idx_placa], directie):
            return None
        if not self.are_sustinere(idx_nivel, self.info[idx_nivel], self.info[idx_nivel][idx_placa]):
            return None
        copie = copy.deepcopy(self.info)

        if directie == 1:
            if copie[idx_nivel][idx_placa - 1][2] != '.':
                spatiu = [copie[idx_nivel][idx_placa][0] - 1, copie[idx_nivel][idx_placa][0] - 1, '.']
                copie[idx_nivel].insert(idx_placa - 1, spatiu)
                idx_placa += 1
            else:
                copie[idx_nivel][idx_placa - 1][1] += 1
        else:
            if copie[idx_nivel][idx_placa + 1][2] != '.':
                spatiu = [copie[idx_nivel][idx_placa][1] + 1, copie[idx_nivel][idx_placa][1] + 1, '.']
                copie[idx_nivel].insert(idx_placa + 1, spatiu)
            else:
                copie[idx_nivel][idx_placa + 1][0] -= 1

        copie[idx_nivel][idx_placa][0] += directie
        copie[idx_nivel][idx_placa][1] += directie
        lung_placa_cost = copie[idx_nivel][idx_placa][1] - copie[idx_nivel][idx_placa][0] + 1

        copie[len(copie) - 1], nr_bile = self.elimina_bile(copie[len(copie) - 1])
        return NodParcurgere(copie, self, nr_bile, 1 + lung_placa_cost)

    def bila_sparta_impingere(self, idx_nivel, idx_placa, directie):
        # stim ca self.info[idx_nivel][idx_placa+directie] e un spatiu
        # pt ca apelam functia din mutare_bile()
        if directie == 1:
            idx_spatiu = self.info[idx_nivel][idx_placa][1] + directie
        else:
            idx_spatiu = self.info[idx_nivel][idx_placa][0] + directie

        idx_placa_niv1 = bisect_right(self.info[idx_nivel + 1], idx_spatiu, key=lambda x: x[0])

        if len(self.info) < 3:
            return False, idx_placa_niv1 - 1

        if self.info[idx_nivel + 1][idx_placa_niv1][1] >= idx_spatiu and self.info[idx_nivel + 1][idx_placa_niv1][
            2] == '.':
            idx_placa_niv2 = bisect_right(self.info[idx_nivel + 2], idx_spatiu, key=lambda x: x[0])

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

        return NodParcurgere(copie, self, nr_bile, 2 * (1 + lung_placa_cost))

    def elimina_bile(self, nivel):
        bile = 0
        for elem in nivel:
            if elem[2] == '*':
                elem[2] = '.'
                bile = elem[1] - elem[0] + 1
        return nivel, self.nr_bile - bile

    def exista_spatiu(self, idx_nivel, margine_placa):
        idx_posibil_spatiu = bisect_right(self.info[idx_nivel + 1], margine_placa, key=lambda x: x[0])
        if self.info[idx_nivel + 1][idx_posibil_spatiu][0] == margine_placa and \
                self.info[idx_nivel + 1][idx_posibil_spatiu][2] == '.':
            return True
        elif self.info[idx_nivel + 1][idx_posibil_spatiu][1] >= margine_placa and \
                self.info[idx_nivel + 1][idx_posibil_spatiu][2] == '.':
            return True
        return False

    def bila_sparta_alunecare(self, idx_nivel, info_placa, directie):
        # trebuie sa verificam daca deasupra marginilor placii exista o bila (start pt directia dreapta, stop altfel)
        # daca nu exista returnam False
        # daca exista, trebuie sa verificam in plus daca pe aceeasi pozitie sub placa este un spatiu
        # marginea placii (start/stop in fct de directie) va deveni un spatiu dupa mutare, deci nu vom mai verifica
        start_placa = info_placa[0]
        stop_placa = info_placa[1]
        if idx_nivel == len(self.info) - 1:
            return False  # placa este prea jos ca sa poata sparge o bila
        nivel_bila = max(0, idx_nivel-1)

        if directie == 1:
            idx_posibil_bila = bisect_right(self.info[nivel_bila], start_placa, key=lambda x: x[0])
            if self.info[nivel_bila][idx_posibil_bila][0] == start_placa and \
                    self.info[nivel_bila][idx_posibil_bila][2] != '*':
                return False
            elif self.info[nivel_bila][idx_posibil_bila][2] == '*':
                # verificam daca avem spatiu sub placa
                if self.exista_spatiu(idx_nivel, start_placa):
                    return True

            elif self.info[nivel_bila][idx_posibil_bila][1] >= start_placa and \
                    self.info[nivel_bila][idx_posibil_bila][2] != '*':
                return False
            elif self.info[nivel_bila][idx_posibil_bila][2] == '*':
                if self.exista_spatiu(idx_nivel, start_placa):
                    return True

        else:
            idx_posibil_bila = bisect_right(self.info[nivel_bila], stop_placa, key=lambda x: x[0])
            if self.info[nivel_bila][idx_posibil_bila][0] == stop_placa and \
                    self.info[nivel_bila][idx_posibil_bila][2] != '*':
                return False
            elif self.info[nivel_bila][idx_posibil_bila][2] == '*':
                # verificam daca avem spatiu sub placa
                if self.exista_spatiu(idx_nivel, stop_placa):
                    return True

            elif self.info[nivel_bila][idx_posibil_bila][1] >= stop_placa and \
                    self.info[nivel_bila][idx_posibil_bila][2] != '*':
                return False
            elif self.info[nivel_bila][idx_posibil_bila][2] == '*':
                # verificam daca avem spatiu sub placa
                if self.exista_spatiu(idx_nivel, stop_placa):
                    return True
        return False

    def are_sustinere(self, idx_nivel, nivel_urm, info_placa):
        # ne aflam pe ultimul nivel, nu avem ce sa verificam
        if idx_nivel == len(self.info) - 1:
            return True
        start_placa = info_placa[0]
        stop_placa = info_placa[1]
        idx_sub_placa = bisect_right(nivel_urm, start_placa, key=lambda x: x[0])
        if nivel_urm[idx_sub_placa][0] == start_placa and nivel_urm[idx_sub_placa[2]] != '.':
            return True
        elif nivel_urm[idx_sub_placa][0] == start_placa and nivel_urm[idx_sub_placa][1] > stop_placa:
            return False

        # daca indecsii de inceput de placi nu sunt egali, trb sa scad 1 din idx_sub_placa
        # pt ca bisect_right imi da indexul urmator in cazul in care nu gaseste valoarea ceruta in lista
        if nivel_urm[idx_sub_placa - 1][0] <= start_placa <= nivel_urm[idx_sub_placa - 1][1]:
            if nivel_urm[idx_sub_placa][2] != '.':
                return True
            elif nivel_urm[idx_sub_placa - 1][1] > stop_placa:
                return False

        return True  # nu ar trb sa ajunga aici

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

import copy
from bisect import bisect_right, bisect_left


class NodParcurgere:
    def __init__(self, info, parinte, nr_bile, cost=0, h=0):
        self.info = info
        self.nr_niveluri = len(self.info)
        self.parinte = parinte
        self.nr_bile = nr_bile
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def testeaza_scop(self):
        return True if self.nr_bile == 0 else False

    def nu_are_solutii(self):
        # daca un nivel intreg din nod nu are spatii => bila nu are pe unde sa cada
        for nivel in self.info:
            for elem in nivel:
                if elem[2] == '.':
                    return False  # daca gasesc un spatiu pot avea solutii
            return True  # daca nu trec la urm nivel inseamna ca un nivel nu are spatii

    def obtine_drum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afis_drum(self, fout, afis_cost=True, afis_lung=True):  # returneaza si lungimea drumului
        l = self.obtine_drum()
        for i, nod in enumerate(l):
            fout.write(f"{i + 1})\n{nod}\n")
        if afis_cost:
            fout.write(f"Cost: {self.g}\n")
        if afis_lung:
            fout.write(f"Lungime: {len(l)}\n")
        return len(l)

    def afis_drum(self, afis_cost=True, afis_lung=True):  # returneaza si lungimea drumului
        l = self.obtine_drum()
        for i, nod in enumerate(l):
            print(f"{i + 1})\n{nod}\n")
        if afis_cost:
            print(f"Cost: {self.g}\n")
        # if afis_lung:
        #     fout.write(f"Lungime: {len(l)}\n")
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

    def __lt__(self, other):
        return self.f < other.f

    def calculeaza_h(self, euristica):
        if euristica == "banala":
            return 0 if self.testeaza_scop() else 1
        elif euristica == "admisibila1":
            return self.nr_bile
        elif euristica == "neadmisibila":
            return -self.nr_bile
        # elif euristica == "admisibila2":

    def genereaza_succesori(self, tip_euristica="euristica banala"):
        lista_succesori = []

        start_cautare = -1
        for idx_nivel, nivel in enumerate(self.info):
            for placa in nivel:
                if placa[2] == '*':
                    start_cautare = idx_nivel
                    break
            if start_cautare != -1:
                break
        start_cautare = max(0, start_cautare)

        if self.nu_are_solutii():
            return []

        for idx_nivel, nivel in enumerate(self.info[start_cautare:]):
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
                    succ = self.mutare_bile(idx_nivel, idx_placa, directie)  # idx_placa = idx bile

                    if succ is not None:
                        lista_succesori.append(succ)

                if placa[2] == '.':
                    # bilele nu se pot muta fara placi
                    if idx_placa < len(self.info[idx_nivel]) - 1 and self.info[idx_nivel][idx_placa + 1][2] != '*':
                        succ_st = self.mutare_placa(idx_nivel, idx_placa + 1, -1)
                        if succ_st is not None:
                            lista_succesori.append(succ_st)

                    if idx_placa > 0 and self.info[idx_nivel][idx_placa - 1][2] != '*':
                        succ_dr = self.mutare_placa(idx_nivel, idx_placa - 1, 1)
                        if succ_dr is not None:
                            lista_succesori.append(succ_dr)

        return lista_succesori

    def interval_corect(self, placa):
        return 0 <= placa[0] <= placa[1]

    def interschimba(self, nivel, placa1, placa2):
        if nivel[placa1][0] > nivel[placa2][0]:
            nivel[placa1], nivel[placa2] = nivel[placa2], nivel[placa1]
            return True
        return False

    def mutare_placa(self, idx_nivel, idx_placa, directie):
        copie = copy.deepcopy(self.info)
        lim = len(copie[idx_nivel]) - 1
        if directie == 1:
            if copie[idx_nivel][idx_placa - 1][2] != '.':
                spatiu = [copie[idx_nivel][idx_placa][0], copie[idx_nivel][idx_placa][0], '.']
                copie[idx_nivel].insert(idx_placa, spatiu)
                idx_placa += 1
            else:
                copie[idx_nivel][idx_placa - 1][0] += 1  # duc spatiile spre dreapta
                if self.interschimba(copie[idx_nivel], idx_placa - 1, idx_placa):
                    idx_placa -= 1
            copie[idx_nivel][idx_placa + 1][0] += 1  # scot spatiul peste care a intrat placa
            self.interschimba(copie[idx_nivel], idx_placa + 1, min(idx_placa + 2, lim))
            if not self.interval_corect(copie[idx_nivel][idx_placa + 1]):
                # daca spatiul are interval incorect => trebuie eliminat pt ca ne incurca la cautarea binara
                copie[idx_nivel].pop(idx_placa + 1)
        else:
            idx_safe = min(idx_placa + 1, lim)
            if copie[idx_nivel][idx_safe][2] != '.':
                spatiu = [copie[idx_nivel][idx_placa][1], copie[idx_nivel][idx_placa][1], '.']
                copie[idx_nivel].insert(idx_safe, spatiu)
            else:
                copie[idx_nivel][idx_safe][0] -= 1

            copie[idx_nivel][idx_placa - 1][1] -= 1  # scot spatiul peste care a intrat placa
            if not self.interval_corect(copie[idx_nivel][idx_placa - 1]):
                copie[idx_nivel].pop(idx_placa - 1)
                idx_placa -= 1

        copie[idx_nivel][idx_placa][0] += directie
        copie[idx_nivel][idx_placa][1] += directie
        lung_placa_cost = copie[idx_nivel][idx_placa][1] - copie[idx_nivel][idx_placa][0] + 1

        copie[len(copie) - 1], nr_bile = self.elimina_bile(copie[len(copie) - 1])
        if self.bila_sparta_alunecare(idx_nivel, copie[idx_nivel][idx_placa], directie):
            return None
        if not self.are_sustinere(idx_nivel, copie[idx_nivel], copie[idx_nivel][idx_placa]):
            return None
        return NodParcurgere(copie, self, nr_bile, 1 + lung_placa_cost)

    def bila_sparta_impingere(self, idx_nivel, idx_placa, directie):
        """
        stim ca self.info[idx_nivel][idx_placa+directie] e un spatiu
        pt ca apelam functia din mutare_bile()
        :param idx_nivel: nivelul bilei
        :param idx_placa: nr placii pe de nivel unde se afla bila
        :param directie: directia de deplasare
        :return: True pt bila sparta
                False si indexul placii peste care va cadea bila integra
        """

        lim = len(self.info) - 1
        if directie == 1:
            idx_spatiu = self.info[idx_nivel][idx_placa][1] + directie
        else:
            idx_spatiu = self.info[idx_nivel][idx_placa][0] + directie

        idx_safe1 = min(idx_nivel + 1, lim)
        idx_placa_niv1 = bisect_right(self.info[idx_safe1], idx_spatiu, key=lambda x: x[0])
        idx_placa_niv1 = min(idx_placa_niv1, len(self.info[idx_safe1]) - 1)

        if self.info[idx_safe1][idx_placa_niv1][1] >= idx_spatiu and self.info[idx_safe1][idx_placa_niv1][
            2] == '.':
            idx_safe2 = min(idx_nivel + 2, lim)
            idx_placa_niv2 = bisect_right(self.info[idx_safe2], idx_spatiu, key=lambda x: x[0])
            idx_placa_niv2 = min(idx_placa_niv2, len(self.info[idx_safe2]) - 1)

            if self.info[idx_safe2][idx_placa_niv2][1] >= idx_spatiu and self.info[idx_safe2][idx_placa_niv2][
                2] == '.':
                return True, -1

            return False, idx_placa_niv1 - 1  # a intrat in primul if deci bila cade
        return False, -1  # bila nu cade

    def mutare_bile(self, idx_nivel, idx_placa, directie):
        copie = copy.deepcopy(self.info)
        nr_elem_nivel = len(copie) - 1

        prev = copie[idx_nivel][max(0, idx_placa - 1)]
        urm = copie[idx_nivel][min(idx_placa + 1, len(copie[idx_nivel]) - 1)]
        lung_placa_cost = prev[1] - prev[0] + 1 if directie == 1 else urm[1] - urm[0] + 1

        test_bila = self.bila_sparta_impingere(idx_nivel, idx_placa, directie)
        if test_bila[0]:
            # bila se sparge
            return
        else:
            # bila/bielele se muta cel putin pe nivelul curent
            if directie == 1:
                spatiu = [copie[idx_nivel][idx_placa - 1][0], copie[idx_nivel][idx_placa - 1][0], '.']
                idx_inserare = max(0, idx_placa - 2 * directie)
            else:
                spatiu = [copie[idx_nivel][idx_placa + 1][1], copie[idx_nivel][idx_placa + 1][1], '.']
                idx_inserare = min(idx_placa - 2 * directie, len(copie[idx_nivel])-1)

            if copie[idx_nivel][idx_inserare][2] != '.':
                copie[idx_nivel].insert(idx_inserare, spatiu)
                if directie == 1:
                    # in cazul acesta idx_inserare e mai mic decat index placa
                    # trebuie mentinut indexul corect al bilelor
                    idx_placa += 1
            else:
                if directie == 1:
                    copie[idx_nivel][idx_inserare][1] += 1
                else:
                    copie[idx_nivel][idx_inserare][0] -= 1
            # copie[idx_nivel].insert(idx_placa)

        if test_bila[1] != -1:
            # bila cade pe nivelul urmator
            placa_schimb = copie[idx_nivel + 1][test_bila[1]]
            idx_bila_cazuta = copie[idx_nivel][idx_placa][0] if directie == -1 else copie[idx_nivel][idx_placa][
                                                                                            1]

            if placa_schimb[0] == placa_schimb[1]:
                placa_schimb[2] = '*'
            else:
                bila = [idx_bila_cazuta, idx_bila_cazuta, '*']
                copie[idx_nivel + 1].insert(test_bila[1], bila)
                if directie == 1:
                    placa_schimb[0] += directie
                else:
                    placa_schimb[1] += directie

                if placa_schimb[0] > placa_schimb[1]:
                    copie[idx_nivel + 1].pop(test_bila[1])
        # else:
        #     if directie == 1:
        #         id
        #     copie[idx_nivel].pop(idx_placa+1)

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

        copie[idx_nivel].pop(idx_placa+directie)
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
        idx_posibil_spatiu = min(idx_posibil_spatiu, len(self.info[idx_nivel + 1]) - 1)
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
        if idx_nivel == len(self.info) - 1 or idx_nivel == 0:
            return False  # placa este prea jos ca sa poata sparge o bila sau nu are alt nivel deasupra
        nivel_bila = idx_nivel - 1

        if directie == 1:
            idx_posibil_bila = bisect_right(self.info[nivel_bila], start_placa, key=lambda x: x[0])
            idx_posibil_bila = min(idx_posibil_bila, len(self.info[nivel_bila]) - 1)
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
            idx_posibil_bila = min(idx_posibil_bila, len(self.info[nivel_bila]) - 1)
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
        if idx_nivel == self.nr_niveluri - 1:
            return True
        start_placa = info_placa[0]
        stop_placa = info_placa[1]
        idx_sub_placa = bisect_right(nivel_urm, start_placa, key=lambda x: x[0])
        # cautarea binara ne poate da un index dupa ultimul din lista
        idx_sub_placa = min(idx_sub_placa, len(self.info[idx_nivel]) - 1)
        if nivel_urm[idx_sub_placa-1][0] == start_placa and nivel_urm[idx_sub_placa-1][2] != '.':
            return True
        elif nivel_urm[idx_sub_placa-1][0] == start_placa and nivel_urm[idx_sub_placa-1][1] >= stop_placa:
            return False

        if nivel_urm[idx_sub_placa - 1][0] <= start_placa <= nivel_urm[idx_sub_placa - 1][1]:
            if nivel_urm[idx_sub_placa-1][2] != '.':
                return True
            elif nivel_urm[idx_sub_placa - 1][1] > stop_placa:
                return False

        return True  # nu ar trb sa ajunga aici

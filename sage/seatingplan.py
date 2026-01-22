"""
Name: seatingplan.py
Author: Jeff LANCE <jeff.lance@mala.fr>
Date: 29/03/2018

Définition d'une classe 'Plan de classe'.
"""


class SeatingPlan:
    """Plan de classe.

    Est un ensemble de places disposées suivant un nombre donné de rangées et
    de colonnes.
    """

    def __init__(self, row=5, col=8):
        """Instancie un objet plan de classe.

        :param row:
            Nombre de rangées dans la classe.
        :type row: int
        :param col:
            Nombre de colonnes dans la classe.
        :type col: int
        :param mapping:
            Représentation du plan de la classe sous la forme
            {(place): (student)}
        :type mapping: dict
        """
        self.row = row
        self.col = col
        self.mapping = {(i, j): None for i in range(row)
                        for j in range(col)}

    def is_full(self):
        """Renvoie si le plan de classe est plein ou non.

        :return:
            True s'il ne reste aucune place vide. False sinon.
        :rtype: bool
        """
        return None not in self.mapping.values()

    def resize(self, row, col):
        """Redimensionne le plan de classe.

        :param row:
            Nombre de rangées.
        :type row: int
        :param col:
            Nombre de colonnes.
        :type row: int
        """
        self.row = row
        self.col = col
        self.mapping = {(i, j): None for i in range(row)
                        for j in range(col)}

    def get_corners(self):
        """ Renvoie, pour un plan de classe, la liste des places aux coins
        ou extrémités.
        C'est-à-dire une place située en : (0,0), (0,m-1),
        (n-1,0) ou (n-1,m-1) pour un plan de classe de dimensions n x m.

        :param seatingplan:
            Plan de classe.
        :type seatingplan: SeatingPlan

        :return:
            Liste des places aux coins/extrémités.
        :rtype: list
        """
        # Dimensions du plan de classe
        n = self.row
        m = self.col

        # Le plan de classe est un tableau de dimensions n x m :
        # - si n>1 et m>1, il possède 4 coins
        # - si n=1 et m>1, il en possède 2
        # - si n>1 et m=1, il en possède 2
        # - si n=1 et m=1, il en possède 1
        #
        # On utilise donc un set qui va permettre d'éliminer les doublons de
        # coordonnées
        # Ce set est ensuite "traduit" en liste
        corners = list({(0, 0), (n-1, 0), (0, m-1), (n-1, m-1)})
        return corners

    def is_a_seat(self, seat):
        """Renvoie si une place est valide ou non.

        Vérifie si les coordonnées de la place sont valides. C'est-à-dire
        si chacune des coordonnées n'est pas vide et si la place fait bien
        partie du plan de classe.

        :param seat:
            Place.
        :type seat: tuple

        :return:
            True, si la place est valide et appartient au plan de classe.
            False, si non.
        :rtype: bool
        """
        # On suppose par défaut que la place est valide
        valid = True
        # Si les coordonnées sont valides
        if (seat[0] is not None and seat[1] is not None):
            # Si le siège n'est pas dans le plan de classe
            if seat not in self.mapping:
                # La place n'est pas valide
                valid = False
        # Si les coordonnées ne le sont pas, la place non plus
        else:
            valid = False

        # On retourne la validité
        return valid

    def get_student(self, seat):
        """Renvoie l'élève assis à une place.

        :param seat:
            Coordonnées de la place dans le plan de classe.
        :type seat: tuple

        :return: None si personne à cette place.
                 Élève si la place est occupée.
        :rtype: Student ou None
        """
        if self.is_a_seat(seat):
            return self.mapping[seat]

    def get_seat(self, student):
        """Renvoie la place d'un élève.

        :param student:
            Élève.
        :type student: Student

        :return:
            La place de l'élève dans le plan de classe.
            False si l'élèves n'est pas dans le plan de classe.
        :rtype: tuple or False
        """
        try:
            return self.get_seats()[list(self.mapping.values())
                                             .index(student)]
            # return list(self.mapping.keys())[list(self.mapping.values())
            #                                  .index(student)]
        except ValueError:
            return False

    def get_seat_neighbourhood(self, seat, radius):
        """Dans un plan de classe, retourne le voisinage dans un rayon donné
        d'une place.

        :param seat:
            Coordonnées de la place dans le plan de classe.
        :type seat: tuple
        :param radius:
            Rayon du voisinage.
        :type radius: int

        :return:
            Liste des places voisines.
        :rtype: list
        """
        # La liste des voisins
        neighbourhood = []
        # 'position' est un tuple de coordonnées (i, j) où:
        # - i compris entre 0 et seatingplan.row-1
        # - j compris entre 0 et seatingplan.col-1
        #
        # Les voisins sont les élèves aux places de coordonnées situées
        # dans le carré passant par les points suivants :
        # (i, j-radius), (i, j+radius), (i-radius, j), (i+radius, j),
        # (i-radius, j-radius), (i-radius, j+radius),
        # (i+radius, j-radius) et (i+radius, j+radius)
        # On analyse ce voisinage et on n'ajoute un voisin que s'il y en a un
        for i in range(-radius, radius+1, 1):
            for j in range(-radius, radius+1, 1):
                # Traitons la place voisine
                neighbour_seat = (seat[0]+i, seat[1]+j)
                # print("Place: ", neighbour_seat)    # DEBUG #
                # Cette place est-elle ?
                # - différente de la place autour de laquelle on regarde
                # - bien comprise dans le plan de classe (coordonnées de
                #   dépassant pas celles du plan de classe)
                if (neighbour_seat != seat and
                        0 <= neighbour_seat[0] <= self.row-1 and
                        0 <= neighbour_seat[1] <= self.col-1):
                    neighbourhood.append(neighbour_seat)
        # On retourne notre liste de places voisines
        return neighbourhood

    def get_seats(self):
        return list(self.mapping.keys())

    def is_empty_seat(self, seat):
        """Indique si une place est libre.

        :param seat:
            Coordonnées de la place dans le plan de classe.
        :type seat: tuple

        :return:
            True si la place est vide, False sinon.
        :rtype: bool
        """
        if self.is_a_seat(seat):
            return self.get_student(seat) is None
        return False

    def place_student(self, student, seat):
        """Positionne un élève dans le plan de classe.

        :param student:
            Élève à placer.
        :type student: Student
        :param seat:
            Place à laquelle asseoir l'élève.
        :type seat: tuple

        :return:
            True, si la place est libre et que le positionnement s'est
            bien déroulé.
            False, si la place est occupée.
        :rtype: bool
        """
        # On peut placer l'élève a une place si celle-ci est vide
        if self.is_empty_seat(seat):
            # On place l'élève
            self.mapping[seat] = student
            return True
        return False

    def remove_student(self, student):
        """Retire un élève de sa place.

        :param student:
            Élève à retirer.
        :type student: Student

        :return:
            True si la suppression s'est bien déroulée, False sinon.
        :rtype: bool
        """
        # On rećupère la place de l'élève
        seat = self.get_seat(student)
        if seat:
            # Le siège dans le plan de classe est libéré
            self.mapping[seat] = None
            return True
        return False

    def swap_students(self, student_one, student_two):
        """Fait s'échanger de place deux élèves.

        :param student_one:
            Premier élève.
        :type student_one: Student
        :param student_two:
            Deuxième élève.
        :type student_one: Student

        :return:
            Si l'opération s'est bien déroulée.
        :rtype: bool
        """
        # On récupère leur place
        seat_one = self.get_seat(student_one)
        seat_two = self.get_seat(student_two)

        # On les retire
        if (self.remove_student(student_one)
                and self.remove_student(student_two)):
            # On attribue à chacun sa nouvelle place
            if (self.place_student(student_one, seat_two)
                    and self.place_student(student_two, seat_one)):
                return True
        return False

    def flush(self):
        """Vide le plan de classe. Supprime tous les élèves placés.

        :return: None
        """
        for seat in self.get_seats():
            student = self.get_student(seat)
            if student is not None:
                self.remove_student(student)

    def write_solution(self, solution):
        """Place les élèves de la solution dans un plan de classe.

        :param solution:
            Solution de positionnement des élèves dans le plan de classe.
        :type solution: dict

        :return: None
        """
        for place, student in solution.items():
            if student is not None:
                self.place_student(student, place)
            else:
                self.mapping[place] = None
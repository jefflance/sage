"""
Name: engine.py
Author: Jeff LANCE <jeff.lance@mala.fr>
Date: 29/03/2018

Définition d'une classe Engine.

Contient les éléments intervenant dans les calculs de recherche de solutions.
"""


class Engine:
    """Le moteur de calculs qui travaille sur un plan de classe."""

    def __init__(self):
        """Instancie un objet Engine.

        :ivar NEIGHBORHOOD_RADIUS:
            Rayon du voisinage.
        :vartype NEIGHBORHOOD_RADIUS: int
        :ivar DELTA_FOR_MAX_CHAT_LVL_1:
            Différence minimale entre le coefficient de bavardage d'un élève et
            ses voisins lorsque leur coefficient maximal vaut 1.
        :vartype DELTA_FOR_MAX_CHAT_LVL_1: int
        :ivar DELTA_FOR_MAX_CHAT_LVL_2:
            Différence minimale entre le coefficient de bavardage d'un élève et
            ses voisins lorsque leur coefficient maximal vaut 2.
        :vartype DELTA_FOR_MAX_CHAT_LVL_32 int
        :ivar DELTA_FOR_MAX_CHAT_LVL_3:
            Différence minimale entre le coefficient de bavardage d'un élève et
            ses voisins lorsque leur coefficient maximal vaut 3.
        :vartype DELTA_FOR_MAX_CHAT_LVL_3: int
        :ivar DELTA_FOR_MAX_CHAT_LVL_4:
            Différence minimale entre le coefficient de bavardage d'un élève et
            ses voisins lorsque leur coefficient maximal vaut 4.
        :vartype DELTA_FOR_MAX_CHAT_LVL_4: int
        :ivar DELTA_FOR_MAX_CHAT_LVL_5:
            Différence minimale entre le coefficient de bavardage d'un élève et
            ses voisins lorsque leur coefficient maximal vaut 5.
        :vartype DELTA_FOR_MAX_CHAT_LVL_5: int
        """
        self.NEIGHBOURHOOD_RADIUS = 1
        self.DELTA_FOR_MAX_CHAT_LVL_1 = 0
        self.DELTA_FOR_MAX_CHAT_LVL_2 = 1
        self.DELTA_FOR_MAX_CHAT_LVL_3 = 1
        self.DELTA_FOR_MAX_CHAT_LVL_4 = 2
        self.DELTA_FOR_MAX_CHAT_LVL_5 = 2

    def respect_constraints(self, seat, student, seatingplan, solution):
        """Indique si une place associée à une élève satisfait aux
        contraintes, à savoir si :

            - l'élève n'a pas déjà été positionné
            - la place n'est pas déjà occupée
            - la place est libre, que son voisinage est composé de bons voisins
              en termes de bavardages.

        :param seat:
            Place que l'on veut associer à un élève.
        :type seat: tuple
        :param student:
            Élève que l'on veut associer à une place.
        :type student: Student
        :param seatingplan:
            Plan de classe.
        :type seatingplan: SeatingPlan
        :param solution:
            Associations 'place - élève' valides.
        :type solution: dict

        :rtype: bool

        .. todo::
            - Modifier le traitement des contraintes de façon à tolérer
              un certains nombre de voisins ne satisfaisants pas aux
              contraintes.
            - Ajouter les liens sociaux comme contraintes supplémentaires.
        """
        # L'association en cours est supposée valide
        result = True
        # Si l'élève en cours a déjà été traité, l'association est invalide
        if student in solution.values():
            result = False
            # return False
        # Si la place en cours a déjà été traitée, l'association est invalide
        elif seat in solution.keys():
            result = False
            # return False
        else:
            # Si non, veŕifions le voisinage de la place
            # Récupérons le voisinage de la place en cours
            neighbourhood = seatingplan.get_seat_neighbourhood(seat,
                                                               self.NEIGHBOURHOOD_RADIUS)

            for neighbour_seat in neighbourhood:
                # On ne teste les contraintes que sur les sièges déjà occupés
                # donc sur ceux faisant déjà partie des solutions
                if neighbour_seat in list(solution.keys()):
                    # On récupère l'élève du siège voisin
                    neighbour = solution[neighbour_seat]

                    # Lequel de l'élève en cours ou du voisin
                    # est le plus bavard ?
                    max_chat_lvl = max(student.chat_lvl,
                                       neighbour.chat_lvl)

                    # Les contraintes portent sur la différence de
                    # coefficient de bavardage entre deux voisins:
                    if max_chat_lvl == 5:
                        result = result and student.has_safe_neighbour(
                                            neighbour,
                                            self.DELTA_FOR_MAX_CHAT_LVL_5)

                    elif max_chat_lvl == 4:
                        result = result and student.has_safe_neighbour(
                                            neighbour,
                                            self.DELTA_FOR_MAX_CHAT_LVL_4)

                    elif max_chat_lvl == 3:
                        result = result and student.has_safe_neighbour(
                                            neighbour,
                                            self.DELTA_FOR_MAX_CHAT_LVL_3)

                    elif max_chat_lvl == 2:
                        result = result and student.has_safe_neighbour(
                                            neighbour,
                                            self.DELTA_FOR_MAX_CHAT_LVL_2)

                    elif max_chat_lvl == 1:
                        result = result and student.has_safe_neighbour(
                                            neighbour,
                                            self.DELTA_FOR_MAX_CHAT_LVL_1)

                    else:
                        result = result and True
                # Le siège voisin n'est pas occupé, il est donc valide
                result = result and True
        # retournons la validité de l'association
        return result

    def verify_solution(self, seatingplan):
        solution = seatingplan.mapping
        result = True
        for seat in list(solution.keys()):
            student = seatingplan.get_student(seat)
            neighbourhood = seatingplan.get_seat_neighbourhood(seat,
                                                               self.NEIGHBOURHOOD_RADIUS)

            for neighbour_seat in neighbourhood:
                # On ne teste les contraintes que sur les sièges déjà occupés
                # donc sur ceux faisant déjà partie des solutions
                if neighbour_seat in list(solution.keys()):
                    # On récupère l'élève du siège voisin
                    neighbour = solution[neighbour_seat]

                    # Lequel de l'élève en cours ou du voisin
                    # est le plus bavard ?
                    max_chat_lvl = max(student.chat_lvl,
                                       neighbour.chat_lvl)

                    # Les contraintes portent sur la différence de
                    # coefficient de bavardage entre deux voisins:
                    if max_chat_lvl == 5:
                        result = result and student.has_safe_neighbour(
                                            neighbour,
                                            self.DELTA_FOR_MAX_CHAT_LVL_5)

                    elif max_chat_lvl == 4:
                        result = result and student.has_safe_neighbour(
                                            neighbour,
                                            self.DELTA_FOR_MAX_CHAT_LVL_4)

                    elif max_chat_lvl == 3:
                        result = result and student.has_safe_neighbour(
                                            neighbour,
                                            self.DELTA_FOR_MAX_CHAT_LVL_3)

                    elif max_chat_lvl == 2:
                        result = result and student.has_safe_neighbour(
                                            neighbour,
                                            self.DELTA_FOR_MAX_CHAT_LVL_2)

                    elif max_chat_lvl == 1:
                        result = result and student.has_safe_neighbour(
                                            neighbour,
                                            self.DELTA_FOR_MAX_CHAT_LVL_1)

                    else:
                        result = result and True
                # Le siège voisin n'est pas occupé, il est donc valide
                result = result and True
        # retournons la validité de l'association
        return result

    def solve(self, seatingplan, students_list):
        """Cherche pour une liste de places et une liste d'élèves, un ensemble
        de dispositions dans un plan de classe respectueuses de certaines
        contraintes décrites dans la fonction 'respect_constraints' ci-dessus.

        :param seatingplan:
            Plan de classe.
        :type seatingplan: SeatingPlan
        :param students_list:
            Liste d'élèves à positionner dans le plan de classe.
        :type students_list: list
        :param solution:
            Solution de placement proposée.
        :type solutions: dict

        :return:
            Disposition des élèves dans le plan de classe.
        :rtype: generator
        """
        # Liste des places
        seats_list = list(seatingplan.mapping.keys())

        # Quantités de places et d'élèves à traiter
        number_of_seats = len(seats_list)
        number_of_students = len(students_list)

        # On stocke nos associations 'place - élève' dans un dictionnaire
        solution = {}

        # Indexes de départ dans nos listes de places et d'élèves
        idx_seat = 0
        idx_student = 0

        # Retour sur trace (backtracking)
        backtrack = False
        # Fin du parcours
        end = False

        # On commence notre recherche
        while not end:
            # On ne revient pas encore en arrière
            while not backtrack:
                # Place à traiter
                current_seat = seats_list[idx_seat]
                # Élève à traiter
                current_student = students_list[idx_student]

                # L'association 'place - élève' est-elle satisfaisante ?
                if self.respect_constraints(current_seat,
                                            current_student,
                                            seatingplan,
                                            solution):
                    # Oui, alors associons l'élève à cette place
                    solution[current_seat] = current_student

                    # Est-ce qu'on a traité tous les élèves dans
                    # notre parcourt ?
                    if (idx_student == number_of_students-1):
                        # Oui, alors renvoyons notre solution
                        yield {p: s for p, s in solution.items()}
                        del solution[current_seat]

                        # A-t'on traité toutes les places ?
                        if (idx_seat != number_of_seats-1):
                            # Non, on passe à la suivante
                            idx_seat = idx_seat + 1
                        else:
                            # Oui, on revient en arrière
                            backtrack = True
                    else:
                        # Non, on passe au suivant en recommençant à la
                        # première place
                        idx_seat = 0
                        idx_student = idx_student + 1

                # Les contraintes n'ont pas été satisfaites,
                # il nous reste des places à traiter
                elif (idx_seat != number_of_seats-1):
                    # On passe à la suivante
                    idx_seat = idx_seat + 1

                else:
                    # Si non, on revient en arrière
                    backtrack = True

            # Sommes-nous remonté jusqu'au premier élève ?
            end = (idx_student == 0)

            # On revient sur nos pas...
            while (backtrack and not end):
                # Prenons l'élève précédent
                idx_student = idx_student - 1
                current_student = students_list[idx_student]
                # On récupère (et on enlève des solutions) la place qui lui
                # est associée
                current_seat = list(solution.keys())[list(solution.values())
                                                     .index(current_student)]
                solution.pop(current_seat)
                idx_seat = seats_list.index(current_seat)

                # Il nous reste des places
                if (idx_seat != number_of_seats-1):
                    # Prenons la place suivante et stoppons notre retour
                    # en arrière
                    idx_seat = idx_seat + 1
                    backtrack = False
                # Ou nous sommes revenu au premier élève, on stop là
                elif idx_student == 0:
                    end = True


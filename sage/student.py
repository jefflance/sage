"""
Name: student.py
Author: Jeff LANCE <jeff.lance@mala.fr>
Date: 29/03/2018

Définiton d'une classe 'Student'.

Contient les éléments néćessaire à la création, manipulation d'élèves.
"""


class Student:
    """Élève.

    Un élève d'une classe a pour attributs: un nom,  un niveau de bavardage,
    une liste d'amis.
    """

    def __init__(self, name, chat_lvl=0, friends=[]):
        """Instancie un objet plan de classe.

        :param name:
            Nom de l'élève.
        :type name: str
        :param chat_lvl:
            Coefficient ou niveau de bavardage.
        :type chat_lvl: int
        :param friends:
             Liste d'amis.
        :type friends: list
        """
        self.name = name
        self.chat_lvl = chat_lvl
        self.friends = friends

    def has_safe_neighbour(self, neighbour, delta_chat_lvl):
        """Indique si deux élèves constituent de bons voisins.
        C'est-à-dire si la différence de leur coefficient de bavardage
        est d'une certaine valeur.

        :param neighbour:
            Élève.
        :type neighbour: Student
        :param delta_chat_lvl:
            Différence entre les coefficients de bavardage.
        :type delta_chat_lvl: int

        :rtype: bool
        """
        return bool(abs(self.chat_lvl - neighbour.chat_lvl)
                    >= delta_chat_lvl)
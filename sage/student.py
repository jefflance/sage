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

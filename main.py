#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name: main.py
Author: Jeff LANCE <jeff.lance@mala.fr>
Date: 29/03/2018

Générateur de plan de classe.

Cette application nécessite une liste d'élèves donnée sous forme d'un ficher
CSV d'en-tête "ID";"NAME";"CHAT LEVEL", avec:

ID: Numéro d'identification arbitraire de l'élève.
NAME: Nom de l'élève.
CHAT LEVEL: Coefficient de bavardage de l'élève.
"""


# Imports de modules
import random
from itertools import islice
from sage import SeatingPlan, Engine, interface


# Instanciation des objets
seatingplan = SeatingPlan()
engine = Engine()


# Fonctions du menu
def mainmenu_option1():
    """ Option 1 du menu principal.

    Redimensionne le plan de classe selon le nombre de rangées et de colonnes
    demandés à l'utilisateur.

    :return:
        Rien.
    """
    # on demande les nouvelles dimensions du plan de classe
    row, col = interface.console_ask_seatingplan_size()

    if row is not None and col is not None:
        # on redimensionne le plan de classe
        seatingplan.resize(row, col)


def mainmenu_option2():
    """Option 2 du menu principal.

    Demande à l'utilisateur le fichier contenant la liste des élèves à
    intégrer dans le plan de classe.

    :return:
        Rien ou la liste des élèves.
    :rtype: list
    """
    filepath = interface.dialog_ask_file()
    # L'utilisateur a-t'il annulé sa recherche de fichier ?
    if filepath:
        # Non, on renvoie le fichier ouvert
        dataframe = interface.open_file(filepath)
        students_list = interface.load_users(dataframe, seatingplan)
        return students_list
    else:
        # Oui
        print('Opération annulée')


def mainmenu_option3(students_list):
    """Option 3 du menu principal.

    Affiche la liste des élèves dans la console, si celle-ci n'est pas vide.

    :param students_list:
        Liste des élèves.
    :type students_list: list

    :return:
        Rien.
    """
    if students_list:
        # on affiche la liste des élèves
        interface.console_display_students(students_list)
    else:
        print("Votre liste d'élèves est vide")


def mainmenu_option4(students_list):
    """Option 4 du menu principal.

    Demande à l'utilisateur l'identifiant d'un élève ainsi que les coordonnées
    d'une place dans le plan de classe.
    Positionne cet élève à la place indiquée.

    :param students_list:
        Liste des élèves.
    :type students_list: list

    :return:
        Rien.
    """
    # Si la liste contient des élèves
    if students_list:
        # On demande l'ID de l'élève
        student_id = interface.console_ask_student_id()
        # Si on a pu récupérer une valeur
        if student_id is not None:
            # On récupère l'élève associé à l'ID
            student = students_list[student_id]
            # On demande le siège où l'asseoir
            student_seat = interface.console_ask_student_seat(seatingplan)
            # Si on a pu récupérer une valeur
            if seatingplan.is_a_seat(student_seat):
                # On positionne l'élève
                seatingplan.place_student(student, student_seat)
    else:
        print("Votre liste d'élèves est vide")


def mainmenu_option5(students_list):
    """Option 5 du menu principal.

    Demande à l'utilisateur l'identifiant d'un élève.
    Retire cet élève du plan de classe.

    :param students_list:
        Liste des élèves.
    :type students_list: list

    :return:
        Rien.
    """
    # Si la liste contient des élèves
    if students_list:
        # on demande l'ID de l'élève
        student_id = interface.console_ask_student_id()
        # Si on a pu récupérer une valeur
        if student_id is not None:
            # On récupère l'élève associé à l'ID
            student = students_list[student_id]
            # Et on le retire de sa place
            seatingplan.remove_student(student)
    else:
        print("Votre liste d'élèves est vide")


def mainmenu_option6(students_list):
    """Option 6 du menu principal.

    Demande à l'utilisateur les identifiants de deux élèves.
    Échange les places de ces élèves.

    :param students_list:
        Liste des élèves.
    :type students_list: list

    :return:
        Rien.
    """
    # On demande l'ID du 1er élève
    print('1er élève')
    id1 = interface.console_ask_student_id()
    # Si on a pu récupérer une valeur
    if id1 is not None:
        # On demande l'ID du 2nd élève
        print('2ème élève')
        id2 = interface.console_ask_student_id()
        # Si on a pu récupérer une valeur
        if id2 is not None:
            # On échange les deux élèves de place
            seatingplan.swap_students(students_list[id1], students_list[id2])


def mainmenu_option7(students_list):
    """Option 7 du menu principal.

    Démarre une recherche des agencements possibles des élèves dans le plan
    de classe.

    :param students_list:
        Liste des élèves.
    :type students_list: list

    :return:
        Plan de classe possible.
    :rtype: iterator
    """
    number_of_proposals = input('Nombre maximal de propositions à faire (5 par défaut) : ')
    number_of_proposals = int(number_of_proposals or "5")
    print('Presser Ctrl-C pour interrompre...')
    try:
        return iter(list(islice(engine.solve(seatingplan, students_list),
                                number_of_proposals)))
        # return iter(list(engine.solve(seatingplan, students_list)))
    except KeyboardInterrupt:
        pass
    else:
        print('Appuyer sur "n" pour afficher la disposition suivante...')


def mainmenu_option8():
    """Option 8 du menu principal.

    Efface le contenu du plan de classe courant.

    :return: None
    """
    print('Effacement du plan de classe...')
    # engine.flush_seatingplan(seatingplan)
    seatingplan.flush()


def mainmenu_option_next(solution):
    """Option n du menu principal.

    Affiche l'agencement de plan de classe possible suivant.

    :param solution:
        Agencement de plan de classe.
    :type solution: dict

    :return:
        Rien.
    """
    if solution:
        try:
            # engine.flush_seatingplan(seatingplan)
            seatingplan.flush()
            # engine.write_solution_to_seatingplan(next(solution), seatingplan)
            seatingplan.write_solution(next(solution))
        except StopIteration:
            print("Il n'y a plus de propositions de placement")
    else:
        print("Vous devez le calcul de solutions d'abord")


def mainmenu_option9():
    """Option 9 du menu principal.

    

    :return: None
    """
    print('Teste plan de classe...')
    print(engine.verify_solution(seatingplan))


def settingsmenu():
    """ Menu paramètres.

    Affiche le menu paramètres dans la console.

    :return:
        Rien.
    """
    while True:
        interface.console_display_settingsmenu(engine)
        command = input('>>> ')

        if (command == 'b'):
            return None
        elif not command:
            print('Choisissez une option')
        else:
            interface.console_set_engine_levels(engine, command)


def mainmenu():
    """ Menu principal.

    Affiche le menu principal dans la console.

    :return:
        Rien.
    """
    while True:
        # affichage de l'interface et du prompt
        interface.console_display(seatingplan)
        command = input('>>> ')

        if (command == '1'):
            mainmenu_option1()

        elif (command == '2'):
            students_list = mainmenu_option2()

        elif (command == '3'):
            mainmenu_option3(students_list)

        elif (command == '4'):
            mainmenu_option4(students_list)

        elif (command == '5'):
            mainmenu_option5(students_list)

        elif (command == '6'):
            mainmenu_option6(students_list)

        elif (command == '7'):
            proposals = mainmenu_option7(students_list)
            # On affiche la première solution
            mainmenu_option_next(proposals)

        elif (command == '8'):
            mainmenu_option8()

        elif (command == '9'):
            mainmenu_option9()

        elif (command == 'n'):
            mainmenu_option_next(proposals)

        elif (command == 'DEBUG'):
            def f(s):
                if s is not None:
                    return s.name
                return s

            # DEBUG: print solutions
            try:
                for s in engine.solve(seatingplan, students_list):
                    print({p: f(s) for p, s in s.items()})
            except KeyboardInterrupt:
                pass
            # DEBUG

        elif (command == 's'):
            settingsmenu()

        elif (command == 'q'):
            exit(0)


mainmenu()

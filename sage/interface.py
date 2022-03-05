"""
Name: interface.py
Author: Jeff LANCE <jeff.lance@mala.fr>
Date: 29/03/2018

Module d'interface de l'application.

Contient les éléments permettant de communiquer avec l'utilisateur.
"""


# Import de modules
import os
from tkinter import filedialog
from tkinter import *

import pandas as pd
from pandas import errors

from terminaltables import AsciiTable
from colorclass import Color

from .student import Student


#########################
# Interface application #
#########################
def console_display(seatingplan):
    """Affiche le menu et le plan de classe dans la console.

    :param seatingplan:
        Plan de classe à afficher.
    :type seatingplan: SeatingPlan

    :return:
        Rien.
    """
    console_display_mainmenu(seatingplan)
    console_display_seatingplan(seatingplan)


#########
# Menus #
#########
def console_display_mainmenu(seatingplan):
    """Affiche le menu principal de l'application dans la console.

    :param seatingplan:
        Plan de classe à afficher.
    :type seatingplan: SeatingPlan

    :return:
        Rien.
    """

    input('\nAppuyer sur une touche pour continuer...')
    # On efface l'écran (cls: win, clear: unix)
    os.system('cls' if os.name == 'nt' else 'clear')

    print('')
    print('Bienvenue !')
    print('')
    print("=> Entrez le numéro de l'action à effectuer :")
    print('- 1. pour définir les dimensions du plan de classe: {}x{} '
          'actuellement'.format(seatingplan.row, seatingplan.col))
    print("- 2. pour ouvrir et charger une liste d'élèves depuis "
          'un fichier .csv')
    print('- 3. pour afficher la liste des élèves chargés précédemment')
    print("- 4. pour placer un élève à une place précise:\n"
          '     • la place en bas à gauche a pour coordonnées (1,1)\n'
          '     • la place en haut à droite a pour coordonnées ({},{})\n'
          '     (nécessite son ID)'
          .format(seatingplan.row, seatingplan.col))
    print("- 5. pour enlever un élève du plan de classe (nécessite son ID)")
    print('- 6. pour intervertir les places de deux élèves (nécessite les ID)')
    print('- 7. pour obtenir une liste de plans de classe possibles')
    print('- 8. pour vider le plan de classe')
    print('')
    print("- s. pour paramétrer l'application")
    print('- q. pour quitter')
    print('')


def console_display_settingsmenu(engine):
    """Affiche le menu de paramétrage du de l'application dans la console.

    :param engine:
        Moteur de calcul.
    :type engine: Engine

    :return:
        Rien.
    """

    input('\nAppuyer sur une touche pour continuer...')
    # On efface l'écran (cls: win, clear: unix)
    os.system('cls' if os.name == 'nt' else 'clear')

    print('')
    print('Paramètres actuels')
    print('')
    print('Delta pour coefficient de bavardage\n'
          'Max 1 = {} | Max 2 = {} | Max 3 = {} | Max 4 = {} | Max 5 = {}'
          .format(engine.DELTA_FOR_MAX_CHAT_LVL_1,
                  engine.DELTA_FOR_MAX_CHAT_LVL_2,
                  engine.DELTA_FOR_MAX_CHAT_LVL_3,
                  engine.DELTA_FOR_MAX_CHAT_LVL_4,
                  engine.DELTA_FOR_MAX_CHAT_LVL_5))
    print('')
    print('- Entrez le numéro du niveau à ajuster\n')
    print('- b. pour revenir au menu principal')
    print('')


##################
# Plan de classe #
##################
def console_display_seatingplan(seatingplan):
    """Affiche le plan de classe dans la console.

    :param seatingplan:
        Plan de classe à afficher.
    :type seatingplan: SeatingPlan

    :return:
        Rien.
    """
    # On transforme le plan de classe en table
    rendered_seatingplan = _seatingplan_to_table(seatingplan)

    # Quelques ajustements visuels...
    for i in range(seatingplan.col):
        rendered_seatingplan.justify_columns[i] = 'center'
    rendered_seatingplan.padding_left = 2
    rendered_seatingplan.padding_right = 2
    rendered_seatingplan.inner_heading_row_border = False
    rendered_seatingplan.inner_row_border = True
    # On affiche notre jolie tableau
    print(rendered_seatingplan.table, '\n')


def _seatingplan_to_table(seatingplan):
    """Embellit le plan de classe pour affichage.

    :param seatingplan:
        Plan de classe à afficher.
    :type seatingplan: SeatingPlan

    :return:
        Plan de classe sous forme de tableau.
    :rtype: AsciiTable
    """
    # On crée un tableau vide de dimensions égales à celle du plan de classe
    seatingplan_as_table = [[None for j in range(seatingplan.col)]
                            for i in range(seatingplan.row)]

    # Parcourons le plan de classe
    for place in seatingplan.mapping:
        # On récupère les coordonnées de la place en cours...
        x, y = place[0], place[1]
        # ...on prend son contenu que l'on formate (coloration,...)
        content = _console_render_student(seatingplan.get_student(place))

        # Si la place est occupée
        if not seatingplan.is_empty_seat(place):
            # On rajoute des informations au contenu (id, chat level)
            addon = 'I: {} - L: {}' \
                    .format(seatingplan.get_student(place).id,
                            seatingplan.get_student(place).chat_lvl)
            content = content + '\n' + addon

        # On place le contenu dans notre table
        seatingplan_as_table[seatingplan.row-1-x][y] = content

    # On transforme et on renvoit notre table en tant qu'objet formaté
    # à l'aide du modul terminaltables
    return AsciiTable(seatingplan_as_table)


###################
# Options du menu #
###################
#
# Option 1
#
def console_ask_seatingplan_size():
    """Demande à l'utilisateur de définir la taille du plan de classe.

    :return:
        Dimensions du plan de classe.
    :rtype: tuple or None
    :raises: ValueError
    """
    # On demande le nombre de rangées
    # row va contenir une chaîne de caractère
    row = input('\nVeuillez entrer le nombre de rangées: ')
    # La valeur entrée est-elle valide (un entier > 0) ?
    try:
        # row est convertit en entier, sinon on intercepte une exception
        row = int(row)
        # Si pas d'exception...
        # si row est négative ou nulle, on lève une exception
        if row <= 0:
            raise ValueError('Le numéro de rangées doit être strictement \
                             supérieur à zéro')

        # Autrement tout va bien, on passe aunombre de colonnes
        col = input('\nVeuillez entrer le nombre de colonnes: ')
        # La valeur entrée est-elle valide (un entier > 0) ?
        try:
            # col est convertit en entier, sinon on intercepte une exception
            col = int(col)
            # Si pas d'exception...
            # si col est négative ou nulle, on lève une exception
            if col <= 0:
                raise ValueError('Le numéro de colonnes doit être strictement \
                                 supérieur à zéro')
        # Interception de l'exception pour col
        except ValueError:
            print('La valeur de colonne est invalide')
            col = None

    # Interception de l'exception pour row
    except ValueError:
        print('La valeur de rangée est invalide')
        row, col = None, None

    return row, col


#
# Option 2
#
def dialog_ask_file():
    """Affiche une boite de dialogue permettant de sélectionner
    un fichier csv contenant la liste des utilisateurs à affecter
    dans le plan de classe.

    :return:
        Chemin absolu du fichier sélectionné.
    :rtype: str
    """
    root = Tk()
    # On ne veut pas voir la fenêtre Tkinter
    root.withdraw()
    # Affiche une boite de dialogue demandant de sélectionner un fichier
    # Renvoie le chemin du path qui est stocké dans 'filename'
    filepath = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    return filepath


def open_file(filename):
    """ Ouvre un fichier de données csv.

    :param filename:
        Chemin du fichier à ouvrir.
    :type filename: str

    :return:
        DataFrame pandas
    :rtype: dict
    :raises: pd.errors.EmptyDataError
    """
    # On gère l'erreur liée au fait que le fichier soit vide
    try:
        dataframe = pd.read_csv(filename, sep=';',
                                header=0, index_col=None).to_dict('records')
        print('Ouverture du fichier:', filename)
        return dataframe
    except pd.errors.EmptyDataError:
        print('Fichier vide')


def load_users(dataframe, seatingplan):
    """Instancie des élèves à partir d'un dataframe.

    Les objets 'student' sont instanciés à partir du dictionnaire
    'dataframe', contenant :
    - un id(entifiant) pour l'élève
    - nom de l'élève
    - niveau de bavardage de l'élève

    :param dataframe:
        "Liste" d'élèves.
    :type dataframe: dict
    :param seatingplan:
        Plan de classe.
    :type seatingplan: SeatingPlan

    :return:
        Liste d'élèves instanciés.
    :rtype: list
    """
    students_list = []
    for i, user in enumerate(dataframe):
        students_list.append(Student(user['NAME']))
        students_list[i].id = user['ID']
        students_list[i].chat_lvl = user['CHAT LEVEL']
    return students_list


#
# Option 3
#
def console_display_students(students_list):
    """Affiche la liste des élèves dans la console.

    :param students_list:
        Liste d'élèves.
    :type students_list: list

    :return: None
    """
    students_table = [['ID', 'NAME', 'CHAT LEVEL']]
    for student in students_list:
        students_table.append([student.id,
                               _console_render_student(student),
                               student.chat_lvl])
    rendered_students_table = AsciiTable(students_table)
    print(rendered_students_table.table)


def _console_render_student(student):
    """Formate le nom de l'élève 'student' pour l'affichage en mode
    console du plan de classe.

    :param student:
        Élève.
    :type student: Student

    :return:
        Nom de l'élève en couleur.
    :rtype: str
    """
    name = '.'
    # Est-on bien en présence d'un élève (objet Student) et
    # pas d'une place vide (None) ?
    if isinstance(student, Student):
        # En fonction du coefficient de bavardage de l'élève, on colorie son
        # nom
        if 0 <= student.chat_lvl <= 1:
            name = Color('{green}' + student.name + '{/green}')
        elif 2 <= student.chat_lvl <= 3:
            name = Color('{yellow}' + student.name + '{/yellow}')
        elif 4 <= student.chat_lvl <= 5:
            name = Color('{red}' + student.name + '{/red}')
        #
        # On remplace l'espcace entre le nom et le prénom par un saut de ligne
        # "incompatible" avec la coloration: provoque une coloration de ligne
        # name = student.name.replace(' ', '\n', 1)
        #
    return name


#
# Option 4 et 5
#
def console_ask_student_id():
    """Demande à l'utilisateur l'identifiant d'un élève.

    :return:
        Identifiant d'un élève.
    :rtype: int
    :raises: ValueError
    """
    id = input("Veuillez entrer l'ID de l'élève: ")
    # La valeur entrée est-elle un entier > 0 ?
    try:
        # On s'assure que la valeur entrée est entière en la convertissant
        # sinon, on intercepte une exception
        id = int(id)
        # Si la valeur est entière mais négative stricte
        if id < 0:
            # On lève une exception
            raise ValueError("La valeur d'ID doit être supérieure ou égale "
                             "à zéro")
    except ValueError:
        print('La valeur saisie est invalide')
    else:
        return id


#
# Option 4
#
def console_ask_student_seat(seatingplan):
    """Demande à l'utilisateur les coordonnées d'une place
    dans le plan de classe.

    :return:
        Coordonnées d'une place.
    :rtype: tuple
    :raises: ValueError
    """
    student_row = input('\nVeuillez entrer le numéro de rangée où vous'
                        " souhaitez placer l'élève: ")
    # La valeur entrée est-elle un entier > 0 ?
    try:
        # On s'assure que la valeur entrée est entière en la convertissant
        # sinon, on intercepte une exception
        student_row = int(student_row)
        # Si la valeur est entière mais négative
        if student_row < 1 or student_row > seatingplan.row:
            # On lève une exception
            raise ValueError('Mauvais range')

        # Tout va bien, on passe au numéro de colonne
        student_col = input('\nVeuillez entrer le numéro de colonne où vous'
                            " souhaitez placer l'élève: ")
        # La valeur entrée est-elle un entier > 0 ?
        try:
            # On s'assure que la valeur entrée est entière en la convertissant
            # sinon, on intercepte une exception
            student_col = int(student_col)
            # Si la valeur est entière mais négative
            if student_row < 1 or student_col > seatingplan.col:
                # On lève une exception
                raise ValueError('Mauvais range')

        except ValueError:
            print('La valeur saisie pour le numéro de colonne est invalide')
            student_col = None

    except ValueError:
        print('La valeur saisie pour le numéro de rangée est invalide')
        student_row, student_col = None, None

    # On renvoit les valeurs entrées mais ajustées à l'indexation
    # du plan de classe
    return student_row-1, student_col-1


#
# Option s
#
def console_set_engine_levels(engine, level):
    """Option Level du menu paramètres.

    Propose à l'utilisateur de modifier les contraintes sur les niveaux de
    bavardage.

    :param engine:
        Moteur de calculs.
    :type engine: Engine
    :param level:
        Niveau à modifier.
    :type level: int

    :return:
        Rien.
    """
    # La valeur passée en paramètres est-elle un entier compris entre 1 et 5 ?
    try:
        # On s'assure que la valeur entrée est bien entière
        level = int(level)
        # Si elle n'est pas comprise entre 1 et 5
        if (level < 1 or level > 5):
            # On lève une exception
            raise ValueError('La valeur doit être comprise entre 1 et 5')

        # Autrement, on continue en demandant la valeur du coefficient
        coeff = input('Ajuster coefficient maximal {}: '.format(level))
        # Cette valeur est-elle un entier positif ou nul ?
        try:
            # On s'assure que la valeur entrée est bien entière
            coeff = int(coeff)
            # Si elle est strictement négative
            if coeff < 0:
                # On lève une exception
                raise ValueError('La valeur doit être positive ou nulle')
        except ValueError:
            print('La valeur saisie est invalide')
        else:
            print(coeff)
            if level == 1:
                engine.DELTA_FOR_MAX_CHAT_LVL_1 = coeff
            elif level == 2:
                engine.DELTA_FOR_MAX_CHAT_LVL_2 = coeff
            elif level == 3:
                engine.DELTA_FOR_MAX_CHAT_LVL_3 = coeff
            elif level == 4:
                engine.DELTA_FOR_MAX_CHAT_LVL_4 = coeff
            elif level == 5:
                engine.DELTA_FOR_MAX_CHAT_LVL_5 = coeff

    except ValueError:
        print('Saisie est invalide')

# -*-coding:utf-8 -*
import os
import platform
import re
from datetime import datetime
from tinydb.table import Document
from typing import Generator

pattern_date = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
format_date = '%Y-%m-%d'

pattern_date_heure = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
format_date_heure = '%Y-%m-%dT%H:%M:%S'


def clear_command(name):
    return 'cls' if name == 'Windows' else 'clear'


def clear_console():
    os.system(clear_command(platform.system()))


def controle_date(chaine, pattern, format):
    if re.match(pattern, chaine):
        try:
            datetime.strptime(chaine, format)
            result = True
        except ValueError:
            result = False
    else:
        result = False
    return result


def is_date_valid(chaine):
    return controle_date(chaine, pattern_date, format_date)


def decode_date(chaine):
    if is_date_valid(chaine):
        return datetime.strptime(chaine, format_date)
    else:
        print("abend dans decode_date, chaine :", chaine)


def encode_date(date_time):
    return date_time.strftime(format_date)


def is_date_heure_valid(chaine):
    return controle_date(chaine, pattern_date_heure, format_date_heure)


def decode_date_heure(chaine):
    if is_date_heure_valid(chaine):
        return datetime.strptime(chaine, format_date_heure)
    else:
        print("abend dans decode_date_heure, chaine :", chaine)


def encode_date_heure(date_time):
    return date_time.strftime(format_date_heure)


def is_chaine_alpha_valide(chaine):
    pattern_nom_prenom = r"^[A-Z][A-Za-z\é\è\ê\ë\ç\ï\ô\-]+$"
    controle_01 = isinstance(chaine, str)
    controle_02 = len(chaine) > 1
    controle_03 = re.match(pattern_nom_prenom, chaine)
    return controle_01 and controle_02 and controle_03


def left_justified(liste_de_chaines):
    length_max = max(len(chaine) for chaine in liste_de_chaines)
    for chaine in liste_de_chaines:
        chaine = chaine.ljust(length_max, " ")
        yield chaine


def document(object):
    if isinstance(object, dict):
        return Document(object, object['id'])
    else:
        dico = dict((attr[1:], value) for (attr, value)
                    in object.__dict__.items() if not isinstance(value, list))
        return Document(dico, object.id)


def gen_to_list(object):
    """
    Transforme les attributs de type 'generator' en 'list'
    Afin que l'utilisateur de l'instance object puisse utiliser
    les méthodes de listes sur les attributs censés être des listes
    """
    for attr, value in object.__dict__.items():
        if isinstance(value, Generator):
            setattr(object, attr, list(value))
    return object


def list_attr(attr, list_of_objects):
    """
    renvoie la liste des valeurs d'un attribut dans une liste d'objets
    """
    return [object.__getattribute__(attr) for object in list_of_objects]


def list_valeurs(cle, list_of_objects):
    """
    renvoie la liste des valeurs d'une cle dans une liste d'objets
    """
    return [object[cle] for object in list_of_objects]


def dico_data_frame(entete, list_of_objects):
    """
    Transforme une liste d'objets en dictionnaire à transformer en objet
    de type pandas.DataFrame
    """
    if list_of_objects:
        object = list_of_objects[0]
        dico = dict()
        if hasattr(object, '__dict__'):
            for attr in entete:
                dico[attr] = [object.__getattribute__(attr) for object
                              in list_of_objects]
        elif isinstance(object, dict):
            for attr in entete:
                dico[attr] = list_valeurs(attr, list_of_objects)
        else:
            dico = dict()
    else:
        dico = dict()
    return dico

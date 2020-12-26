# -*-coding:utf-8 -*
import os
import platform
import re
from datetime import datetime


pattern_date = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
format_date = '%Y-%m-%d'

pattern_date_heure = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
format_date_heure = '%Y-%m-%dT%H:%M:%S'

def clear_command(name):
    print("platform.system", name)
    return 'cls' if name == 'Windows' else 'clear'

def clear_console():
    os.system(clear_command(platform.system()))

def controle_date(chaine, pattern, format):
    if re.match(pattern, chaine):
        try:
            date = datetime.strptime(chaine, format)
            del (date)
            result = True
        except ValueError as ex:
            print(f"la chaine de caractères {chaine} n'est pas au format {format}")
            result = False
    else:
        print(f"la chaine de caractères {chaine} ne correspond pas au pattern {pattern}")
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
    pattern_nom_prenom = "^[A-Z][A-Za-z\é\è\ê\ë\ç\ï\ô\-]+$"
    return (isinstance(chaine, str) and len(chaine) > 1 and re.match(pattern_nom_prenom, chaine))

def left_justified(liste_de_chaines):
    length_max = max(len(chaine) for chaine in liste_de_chaines)
    for chaine in liste_de_chaines:
        chaine = chaine.ljust(length_max, " ")
        yield chaine

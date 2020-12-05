# -*-coding:utf-8 -*

from datetime import datetime
import re

def is_date_valid(chaine):
    pattern_date = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
    if re.match(pattern_date, chaine):
        try:
            date = datetime.strptime(chaine, '%Y-%m-%d')
            del(date)
            result = True
        except ValueError as ex:
            print(f"la chaine de caractères {chaine} n'est pas au format date '%Y-%m-%d'")
            result = False
    else:
        print(f"la chaine de caractères {chaine} ne correspond pas au pattern {pattern_date}")
        result = False
    return result

def decode_date(chaine):
    if is_date_valid(chaine):
        return datetime.strptime(chaine, '%Y-%m-%d')
    else:
        print("abend dans decode_date, chaine :", chaine)

def encode_date(date_time):
    return date_time.strftime('%Y-%m-%d')

def is_chaine_alpha_valide(chaine):
    pattern_nom_prenom = "^[A-Z][A-Za-z\é\è\ê\ë\ç\ï\ô\-]+$"
    return (isinstance(chaine, str) and len(chaine) > 1 and re.match(pattern_nom_prenom, chaine))

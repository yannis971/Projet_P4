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
            result = False
    else:
        result = False
    return result

def decode_date(chaine):
    if is_date_valid(chaine):
        return datetime.strptime(chaine, '%Y-%m-%d')
# -*-coding:utf-8 -*
"""
Module generic_views
"""
from app.utils import util


class DetailView:
    """
    classe DetailView
    """

    def __init__(self, title, data):
        self._title = title
        self._data = data
        util.clear_console()

    def display(self):
        print(self._title)
        cles = util.left_justified([cle for cle in self._data.keys()])
        valeurs = (valeur for valeur in self._data.values())
        for cle, valeur in zip(cles, valeurs):
            print(f"\t - {cle} : {valeur}")


class ListView:

    def __init__(self, title, liste_items):
        self._title = title
        self._liste_items = liste_items
        print("\n")

    def display(self):
        print(self._title)
        for i, item in enumerate(self._liste_items):
            print(f"{i + 1} -  {item}")
# -*-coding:utf-8 -*
"""
Module menu
"""
from app.utils import util


class Menu:
    """
    Classe Menu chargé d'afficher un menu :
        Titre
        Liste de choix
    """
    def __init__(self, titre, liste_de_choix):
        self._choix = ""
        self._liste_de_choix = liste_de_choix
        self._indice_max = len(liste_de_choix) - 1
        self._titre = titre
        util.clear_console()

    def get_choix(self):
        print(f"\n{self._titre}\n")
        for (i, libelle_choix) in enumerate(self._liste_de_choix):
            print(f"{i} - {libelle_choix}")
        try:
            message = f"\nentrer votre choix de 0 à {self._indice_max} : "
            self._choix = int(input(message).strip())
            assert self._choix >= 0 and self._choix <= self._indice_max
        except ValueError:
            return self.get_choix()
        except AssertionError:
            return self.get_choix()
        else:
            return self._choix

# -*-coding:utf-8 -*

from app.utils import util


class Menu:


    def __init__(self, liste_de_choix):
        self._choix = ""
        self._liste_de_choix = liste_de_choix
        util.clear_console()

    def get_choix(self):
        for (i, libelle_choix) in enumerate(self._liste_de_choix):
            print(f"{i} - {libelle_choix}")
        try:
            self._choix = int(input(f"entrer votre choix de 0 à {len(self._liste_de_choix)-1}: "))
            assert self._choix >= 0 and self._choix < len(self._liste_de_choix)
        except ValueError:
            return self.get_choix()
        except AssertionError:
            return self.get_choix()
        else:
            return self._choix

if __name__ == "__main__":
    m = Menu()
    print("mon choix est", m.get_choix())
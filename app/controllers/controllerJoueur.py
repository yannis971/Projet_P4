# -*-coding:utf-8 -*
# import sys
# on modifie le sys.path pour y inclure les dossiers
# contenant les classes à importer
# sys.path.append(".")




from app.views.menu import Menu
from app.views.formulaire import JoueurForm
from app.views.rapport import ListView
from app.models.joueur import Joueur
from app.models import exception


class ControllerJoueur:
    __liste_de_choix = ('Créer un joueur',
                        'Afficher la liste des joueurs', 'Quitter')

    def __init__(self):
        self._menu = Menu(ControllerJoueur.__liste_de_choix)
        self._choix = self._menu.get_choix()
        self._liste_joueurs = Joueur.read_all()

    def creer_joueur_handler(self):
        try:
            joueur = Joueur(**JoueurForm().creer_joueur())
            self._liste_joueurs.append(joueur)
            joueur.create()
        except exception.JoueurException as ex:
            print(ex)
            return self.creer_joueur_handler()
        except exception.JoueurDAOException as ex:
            print(ex)
            print(f"création joueur KO - {joueur}")
        else:
            print(f"création joueur OK - {joueur}")

    def afficher_liste_joueurs_handler(self):
        ListView("Liste de joueurs", self._liste_joueurs).display()

    def quitter(self):
        print("Fin du programme joueur")
        exit()

    __handlers = {'0': creer_joueur_handler,
                  '1': afficher_liste_joueurs_handler,
                  '2': quitter}

    def start(self):
        while ControllerJoueur.__liste_de_choix[self._choix]:
            ControllerJoueur.__handlers[str(self._choix)](self)
            self._choix = self._menu.get_choix()

if __name__ == "__main__":
    ControllerJoueur().start()

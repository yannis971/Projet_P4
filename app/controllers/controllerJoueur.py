# -*-coding:utf-8 -*

from app.views.menu import Menu
from app.views.formulaire import JoueurForm
from app.views.rapport import DetailView
from app.views.rapport import ListView
from app.models.joueur import Joueur
from app.models import exception


class ControllerJoueur:

    __liste_de_choix = ("Créer un joueur",
                        "Modifier le classement d'un joueur",
                        "Afficher la liste des joueurs",
                        "Quitter")

    def __init__(self):
        self._menu = Menu(ControllerJoueur.__liste_de_choix)
        self._choix = self._menu.get_choix()

    def creer_joueur_handler(self):
        try:
            joueur = Joueur(**JoueurForm().creer_joueur())
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
        ListView("Liste de joueurs", Joueur.read_all()).display()

    def recuperer_joueur(self):
        methode_acces = JoueurForm().recuperer_methode_acces()
        print("methode_acces =", methode_acces)
        try:
            if methode_acces == "id":
                joueur = Joueur.read(JoueurForm().recuperer_id_joueur())
            else:
                joueur = Joueur.read_by_index(**JoueurForm().recuperer_identifiants_joueur())
        except exception.JoueurException as ex:
            print(ex)
            return self.recuperer_joueur()
        except exception.JoueurDAOException as ex:
            print(ex)
            return self.recuperer_joueur()
        else:
            return joueur

    def modifier_classement_joueur(self):
        joueur = self.recuperer_joueur()
        data = dict((attr[1:], value) for (attr, value) in joueur.__dict__.items())
        DetailView("Affichage du joueur", data).display()
        try:
            joueur.classement = JoueurForm().get_classement()
            joueur.update()
        except exception.JoueurException as ex:
            print(ex)
            return self.modifier_classement_joueur()
        except exception.JoueurDAOException as ex:
            print(ex)
            print(f"modification joueur KO - {joueur}")
        else:
            print(f"modification joueur OK - {joueur}")

    def quitter(self):
        print("Fin du sous-programme joueur")
        exit()

    __handlers = {'0': creer_joueur_handler,
                  '1': modifier_classement_joueur,
                  '2': afficher_liste_joueurs_handler,
                  '3': quitter}

    def start(self):
        while ControllerJoueur.__liste_de_choix[self._choix]:
            ControllerJoueur.__handlers[str(self._choix)](self)
            self._choix = self._menu.get_choix()

if __name__ == "__main__":
    ControllerJoueur().start()

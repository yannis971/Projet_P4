# -*-coding:utf-8 -*
"""
Module controlleur_joueur définissant la classe ControllerJoueur
"""
import sys
from operator import attrgetter

from app.views.menu import Menu
from app.views.formulaire import JoueurForm
from app.views.generic_views import DetailView
from app.views.generic_views import ListView
from app.models.joueur import Joueur
from app.models import exception


class ControllerJoueur:
    """
    Classe ControllerJoueur permettant de gérer des actions sur des joueurs
    """
    __liste_de_choix = ("Créer un joueur",
                        "Modifier le classement d'un joueur",
                        "Afficher la liste des joueurs",
                        "Quitter")

    def __init__(self):
        self._menu = Menu("MENU DU PROGRAMME JOUEUR",
                          ControllerJoueur.__liste_de_choix)
        self._choix = self._menu.get_choix()

    def creer_joueur_handler(self):
        """
        Méthode permettant de créer un joueur
        """
        try:
            joueur = Joueur(**JoueurForm().creer_joueur())
            joueur.create()
        except exception.JoueurException as ex:
            print(ex)
            return self.creer_joueur_handler()
        except exception.JoueurDAOException as ex:
            print(ex)
            print(f"création joueur KO - {joueur}")
            return 1
        else:
            print(f"création joueur OK - {joueur}")
            return 0

    def afficher_liste_joueurs_handler(self):
        """
        Méthode permetannt d'afficher la liste des joueurs
        """
        liste_de_joueurs = list(Joueur.read_all())
        liste_de_joueurs.sort(key=attrgetter('id'))
        ListView("Liste des joueurs", liste_de_joueurs).display()

    def recuperer_joueur(self):
        """
        Methode permettant de récupérer un joueur à partir de son id ou
        à partir de ses nom, prénom et date de naissance
        """
        methode_acces = JoueurForm().recuperer_methode_acces()
        try:
            if methode_acces == "id":
                joueur = Joueur.read(JoueurForm().recuperer_id_joueur())
            else:
                index = JoueurForm().recuperer_identifiants_joueur()
                joueur = Joueur.read_by_index(**index)
        except exception.JoueurException as ex:
            print(ex)
            return self.recuperer_joueur()
        except exception.JoueurDAOException as ex:
            print(ex)
            return self.recuperer_joueur()
        else:
            return joueur

    def modifier_classement_joueur_handler(self):
        """
        Methode permettant de modifier le classement d'un joueur
        """
        joueur = self.recuperer_joueur()
        data = dict((attr[1:], value) for (attr, value)
                    in joueur.__dict__.items())
        DetailView("Affichage du joueur", data).display()
        try:
            joueur.classement = JoueurForm().get_classement()
            joueur.update()
        except exception.JoueurException as ex:
            print(ex)
            return self.modifier_classement_joueur_handler()
        except exception.JoueurDAOException as ex:
            print(ex)
            print(f"modification joueur KO - {joueur}")
            return 1
        else:
            print(f"modification joueur OK - {joueur}")
            return 0

    def quitter_handler(self):
        """
        Methode permettant de quitter le programme
        """
        print("Fin du sous-programme joueur")
        sys.exit(0)

    __handlers = {'0': creer_joueur_handler,
                  '1': modifier_classement_joueur_handler,
                  '2': afficher_liste_joueurs_handler,
                  '3': quitter_handler}

    def start(self):
        """
        Methode permettant de lancer le controller
        En fonction du choix saisi par l'utilisateur un "handler" ou
        gestionnaire est appelé pour effectuer la fonction choisie
        """
        while ControllerJoueur.__liste_de_choix[self._choix]:
            ControllerJoueur.__handlers[str(self._choix)](self)
            self._choix = self._menu.get_choix()

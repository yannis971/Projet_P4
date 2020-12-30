# -*-coding:utf-8 -*
"""
Module controlleur_rapport définissant la classe ControllerRapport
"""

import sys
from operator import attrgetter
from operator import itemgetter

from app.views.menu import Menu
from app.views.generic_views import ListView
from app.views.formulaire import RapportForm
from app.views.formulaire import TournoiForm
from app.models.joueur import Joueur
from app.models.tournoi import Tournoi
from app.models import exception


class ControllerRapport:
    """
    Classe ControllerRapport permettant de générer plusieurs listes
    """
    __liste_de_choix = ("Liste de tous les acteurs",
                        "Liste de tous les joueurs d'un tournoi",
                        "Liste de tous les tournois",
                        "Liste de tous les tours d'un tournoi",
                        "Liste de tous les matchs d'un tournoi",
                        "Quitter")

    def __init__(self):
        self._menu = Menu("MENU DU PROGRAMME RAPPORT",
                          ControllerRapport.__liste_de_choix)
        self._choix = self._menu.get_choix()

    def lister_acteurs_handler(self):
        """
        Méthode permettant de lister tous les acteurs (joueurs)
        """
        criteres_de_tri = RapportForm().recuperer_criteres_de_tri()
        liste_des_acteurs = sorted(Joueur.read_all(),
                                   key=attrgetter(*criteres_de_tri))
        ListView("Liste de tous les acteurs", liste_des_acteurs).display()

    def recuperer_tournoi(self):
        """
        Méthode pour récuperer un tournoi à partir de son id ou de
        de son index constitué des nom, lieu et date de début
        """
        methode_acces = TournoiForm().recuperer_methode_acces()
        try:
            if methode_acces == "id":
                tournoi = Tournoi.read(TournoiForm().recuperer_id_tournoi())
            else:
                index = TournoiForm().recuperer_identifiants_tournoi()
                tournoi = Tournoi.read_by_index(**index)
        except exception.TournoiException as ex:
            print(ex)
            return self.recuperer_tournoi()
        except exception.TournoiDAOException as ex:
            print(ex)
            return self.recuperer_tournoi()
        else:
            return tournoi

    def lister_joueurs_tournoi_handler(self):
        """
        Méthode permettant de lister tous les joueurs d'un tournoi
        """
        tournoi = self.recuperer_tournoi()
        criteres_de_tri = RapportForm().recuperer_criteres_de_tri()
        if len(criteres_de_tri) == 1 and criteres_de_tri[0] == 'classement':
            criteres_de_tri[0] = 'rang'
        liste_des_joueurs_du_tournoi = sorted(tournoi.liste_de_participants,
                                              key=attrgetter(*criteres_de_tri))
        ListView(f"Liste de tous les joueurs du tournoi {tournoi}",
                 liste_des_joueurs_du_tournoi).display()

    def lister_tournois_handler(self):
        """
        Méthode permettant de lister tous les tournois
        """
        ListView("Liste de tous les tournois", list(Tournoi.read_all(

        ))).display()

    def lister_tours_tournoi_handler(self):
        """
        Méthode permettant de lister tous les tours d'un tournoi
        """
        tournoi = self.recuperer_tournoi()
        liste_des_tours_du_tournoi = tournoi.liste_de_tours
        ListView(f"Liste de tous les tours du tournoi {tournoi}",
                 liste_des_tours_du_tournoi).display()

    def lister_matchs_tournoi_handler(self):
        """
        Methode permettant de lister tous les matchs d'un tournoi
        """
        tournoi = self.recuperer_tournoi()
        liste_des_tours_du_tournoi = tournoi.liste_de_tours
        for tour in liste_des_tours_du_tournoi:
            liste_de_matchs = list()
            for match in tour.liste_de_matchs:
                data = dict()
                data['id'] = match.id
                data['match'] = match.paire_de_joueurs[0].nom + ' - ' + \
                                match.paire_de_joueurs[1].nom
                data['score'] = f"{match.score[0]} - {match.score[1]}"
                liste_de_matchs.append(data)
            liste_de_matchs.sort(key=itemgetter('id'))
            titre = f"Liste des matchs du tour : {tour.nom}"
            ListView(titre, liste_de_matchs).display()

    def quitter_handler(self):
        """
        Méthode permettant de quitter le programme
        """
        print("Fin du sous-programme rapport")
        sys.exit(0)

    __handlers = {'0': lister_acteurs_handler,
                  '1': lister_joueurs_tournoi_handler,
                  '2': lister_tournois_handler,
                  '3': lister_tours_tournoi_handler,
                  '4': lister_matchs_tournoi_handler,
                  '5': quitter_handler}

    def start(self):
        """
        Methode permettant de lancer le controller
        En fonction du choix saisi par l'utilisateur un "handler" ou
        gestionnaire est appelé pour effectuer la fonction choisie
        """
        while ControllerRapport.__liste_de_choix[self._choix]:
            ControllerRapport.__handlers[str(self._choix)](self)
            self._choix = self._menu.get_choix()

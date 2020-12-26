# -*-coding:utf-8 -*

from operator import attrgetter

from app.views.menu import Menu

from app.views.rapport import ListView
from app.views.formulaire import RapportForm
from app.models.joueur import Joueur
from app.models.tournoi import Tournoi
from app.models import exception


class ControllerRapport:

    __liste_de_choix = ("Liste de tous les acteurs", "Liste de tous les joueurs d'un tournoi",
                        "Liste de tous les tournois", "Liste de tous les tours d'un tournoi",
                        "Liste de tous les matchs d'un tournoi", "Quitter")

    def __init__(self):
        self._menu = Menu(ControllerRapport.__liste_de_choix)
        self._choix = self._menu.get_choix()

    def lister_tous_les_acteurs(self):
        criteres_de_tri = RapportForm().recuperer_criteres_de_tri()
        liste_des_acteurs = sorted(Joueur.read_all(), key=attrgetter(*criteres_de_tri))
        ListView("Liste de tous les acteurs", liste_des_acteurs).display()

    def recuperer_tournoi(self):
        index_tournoi = RapportForm().recuperer_identifiants_tournoi()
        try:
            tournoi = Tournoi.read_by_index(**index_tournoi)
        except exception.TournoiException as ex:
            print(ex)
            return self.recuperer_tournoi()
        else:
            return tournoi

    def lister_tous_les_joueurs_d_un_tournoi(self):
        tournoi = self.recuperer_tournoi()
        criteres_de_tri = RapportForm().recuperer_criteres_de_tri()
        liste_des_joueurs_du_tournoi = sorted(tournoi.liste_de_participants, key=attrgetter(*criteres_de_tri))
        ListView(f"Liste de tous les joueurs du tournoi {tournoi}", liste_des_joueurs_du_tournoi).display()


    def lister_tous_les_tournois(self):
        ListView("Liste de tous les tournois", Tournoi.read_all()).display()

    def lister_tous_les_tours_d_un_tournoi(self):
        tournoi = self.recuperer_tournoi()
        liste_des_tours_du_tournoi = tournoi.liste_de_tours
        ListView(f"Liste de tous les tours du tournoi {tournoi}", liste_des_tours_du_tournoi).display()

    def lister_tous_les_matchs_d_un_tournoi(self):
        tournoi = self.recuperer_tournoi()
        liste_des_tours_du_tournoi = tournoi.liste_de_tours

    def quitter(self):
        print("Fin du sous-programme rapport")
        exit()

    __handlers = {'0': lister_tous_les_acteurs,
                  '1': lister_tous_les_joueurs_d_un_tournoi,
                  '2': lister_tous_les_tournois,
                  '3': lister_tous_les_tours_d_un_tournoi,
                  '4': lister_tous_les_matchs_d_un_tournoi,
                  '5': quitter}

    def start(self):
        while ControllerRapport.__liste_de_choix[self._choix]:
            ControllerRapport.__handlers[str(self._choix)](self)
            self._choix = self._menu.get_choix()

# -*-coding:utf-8 -*

from app.views.menu import Menu
from app.views.formulaire import JoueurForm, TournoiForm, TourForm, MatchForm
from app.views.rapport import ListView
from app.models.joueur import Joueur
from app.models.tournoi import Tournoi
from app.models.tour import Tour
from app.models.match import Match
from app.models import exception


class ControllerTournoi:
    __liste_de_choix = ('Créer un joueur', 'Créer un tournoi', 'Ajouter 8 joueurs',
                        'Générer des paires de joueurs', 'Entrer les résultats',
                        'Afficher la liste des joueurs',
                        'Afficher les rapports', 'Enregistrer', 'Quitter')

    def __init__(self):
        self._menu = Menu(ControllerTournoi.__liste_de_choix)
        self._choix = self._menu.get_choix()
        self._liste_joueurs = Joueur.read_all()
        self._liste_tournois = Tournoi.read_all()
        self._tournoi = None

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

    def creer_tournoi_handler(self):
        try:
            self._tournoi = Tournoi(**TournoiForm().creer_tournoi())
            print(self._tournoi.__dict__)
        except exception.TournoiException as ex:
            print(ex)
            return self.creer_tournoi_handler()
        else:
            self._liste_tournois.append(self._tournoi)
            print(f"création tournoi ok - {self._tournoi}")

    def ajouter_n_joueurs(self):

        ListView("Liste de joueurs", self._liste_joueurs).display()
        liste_indices_joueurs_inscrits = JoueurForm().ajouter_n_joueurs(8)

        for indice in liste_indices_joueurs_inscrits:
            try:
                assert indice >= 0 and indice < len(self._liste_joueurs)
            except AssertionError:
                print(f"au moins un indice non valide dans la liste : {liste_indices_joueurs_inscrits}")
                self._tournoi._liste_indices_joueurs_inscrits = list()
                self._tournoi._nombre_joueurs_inscrits = 0
                return self.ajouter_n_joueurs()
            else:
                self._tournoi.ajouter_joueur(indice)
                self._tournoi.ajouter_participant(self._liste_joueurs[indice])

        self._tournoi.initialiser_rang_participants()

    def generer_des_paires_de_joueurs(self):
        try:
            if self._tournoi is None or not isinstance(self._tournoi, Tournoi):
                raise exception.TournoiException("Option impossible : vous devez d'abord créer un tournoi")
            elif len(self._tournoi.liste_de_tours) >= self._tournoi.nombre_de_tours:
                raise exception.TournoiException(f"Option impossible : {self._tournoi.nombre_de_tours} sont déjà créés.")
            elif len(self._tournoi.liste_de_tours) > 0 and self._tournoi.liste_de_tours[-1].statut == "en cours":
                raise exception.TournoiException(f"Option impossible : tour {self._tournoi.liste_de_tours[-1].nom} est en cours")
            elif self._tournoi.nombre_joueurs_inscrits == 0:
                raise exception.TournoiException(f"Option impossible : vous devez d'abord ajouter des joueurs au tournoi")
            else:
                self._tournoi.creer_tour(len(self._tournoi.liste_de_tours))
        except exception.TournoiException as ex:
            print(ex)
        else:
            print("generer_paires_joueurs ok")
            tour = self._tournoi.liste_de_tours[-1]
            print(tour)
            #afficher la liste des matchs du tour en cours
            for match in tour.liste_de_matchs:
                print(match)

    def mettre_a_jour_score_du_match(self, match):
        try:
            score_premier_joueur, score_deuxieme_joueur = MatchForm(match).mettre_a_jour_score()
            match.update_score(score_premier_joueur, score_deuxieme_joueur)
        except exception.MatchException as ex:
            print(ex)
            return self.mettre_a_jour_score_du_match(match)
        else:
            print(f"mise à jour du score : {match}")

    def confirmer_resultats_du_tour(self, tour):
        ListView(f"Liste des matchs du {tour.nom}", tour.liste_de_matchs).display()
        if TourForm().iscompleted():
            tour.cloturer()
        print(f"tour {tour}")
        ListView("Classement des joueurs participants au tournoi", self._tournoi.liste_de_participants).display()


    def entrer_les_resultats(self):
        tour = self._tournoi.liste_de_tours[-1]
        for match in tour.liste_de_matchs:
            self.mettre_a_jour_score_du_match(match)
        # afficher la liste des matchs du tour en cours
        ListView(f"Liste des matchs du {tour.nom}", tour.liste_de_matchs).display()
        self.confirmer_resultats_du_tour(tour)


    __handlers = {'0': creer_joueur_handler, '1': creer_tournoi_handler,
                  '2': ajouter_n_joueurs, '3': generer_des_paires_de_joueurs,
                  '4': entrer_les_resultats, '5': afficher_liste_joueurs_handler}

    def start(self):
        while ControllerTournoi.__liste_de_choix[self._choix] != 'Quitter':
            ControllerTournoi.__handlers[str(self._choix)](self)
            self._choix = self._menu.get_choix()


if __name__ == "__main__":
    ControllerTournoi().start()

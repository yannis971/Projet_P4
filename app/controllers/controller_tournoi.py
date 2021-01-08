# -*-coding:utf-8 -*
"""
Module controlleur_tournoi définissant la classe ControllerTournoi
"""
import sys
import logging as log
from operator import attrgetter
from app.views.menu import Menu
from app.views.formulaire import JoueurForm, TournoiForm, TourForm, MatchForm
from app.views.generic_views import DetailView
from app.views.generic_views import ListView
from app.models.joueur import Joueur
from app.models.tournoi import Tournoi
from app.models import exception


class ControllerTournoi:
    """
    Classe ControllerTournoi permettant de gérer des actions sur un tournoi
    """
    __liste_de_choix = ("Créer un tournoi",
                        "Ajouter 8 joueurs",
                        "Générer des paires de joueurs",
                        "Entrer les résultats",
                        "Enregistrer",
                        "Charger les données d'un tournoi",
                        "Quitter")

    def __init__(self):
        self._menu = Menu("MENU DU PROGRAMME TOURNOI",
                          ControllerTournoi.__liste_de_choix)
        self._choix = self._menu.get_choix()
        self._liste_joueurs = list(Joueur.read_all())
        self._liste_joueurs.sort(key=attrgetter('id'))
        self._tournoi = None
        self._jeton = None
        log.basicConfig(level=log.INFO)

    def controles_avant_creer_tournoi(self):
        if (isinstance(self._tournoi, Tournoi) and self._jeton is None) or \
                self._jeton == "vérouillé":
            self._jeton = "vérouillé"
            message = "Enregistrer le tournoi en cours au préalable"
            raise exception.TournoiException(message)
        else:
            self._jeton = None

    def creer_tournoi_handler(self):
        """
        Méthode permettant de créer un tournoi
        """
        try:
            self.controles_avant_creer_tournoi()
        except exception.TournoiException as ex:
            log.warning(ex)
        else:
            try:
                self._tournoi = Tournoi(**TournoiForm().creer_tournoi())
            except exception.TournoiException as ex:
                log.warning(ex)
                return self.creer_tournoi_handler()
            else:
                log.info(f"création tournoi ok - {self._tournoi}")

    def controles_avant_ajout_joueurs(self):
        """
        Contrôles avant d'ajouter des joueurs à un tournoi
        """
        if self._tournoi is None or not isinstance(self._tournoi, Tournoi):
            message = "Vous devez d'abord créer un tournoi"
            raise exception.TournoiException(message)
        if len(self._tournoi.liste_de_tours) > 0 and \
                self._tournoi.liste_de_tours[-1].statut == "en cours":
            message = f"Tour {self._tournoi.liste_de_tours[-1].nom} est en " \
                      f"cours"
            raise exception.TournoiException(message)
        elif len(self._tournoi.liste_de_tours) == \
                self._tournoi.nombre_de_tours:
            message = f"{self._tournoi.nombre_de_tours} tours sont créés"
            raise exception.TournoiException(message)

    def ajouter_n_joueurs_handler(self):
        """
        Méthode permettant d'ajouter des joueurs à un tournoi
        """
        try:
            self.controles_avant_ajout_joueurs()
            if len(self._tournoi.liste_de_participants) > 0:
                message = "participants déjà inscrits au tournoi"
                raise exception.TournoiException(message)
        except exception.TournoiException as ex:
            log.warning(ex)
        else:
            entete = ['id', 'nom', 'prenom', 'date_de_naissance', 'sexe',
                      'classement']
            ListView("Liste de joueurs", entete,
                     self._liste_joueurs).display()
            liste_indices_joueurs_inscrits = JoueurForm().ajouter_n_joueurs(8)
            for i in liste_indices_joueurs_inscrits:
                try:
                    assert i >= 0 and i < len(self._liste_joueurs)
                except AssertionError:
                    self._tournoi._nombre_de_joueurs_inscrits = 0
                    return self.ajouter_n_joueurs()
                else:
                    self._tournoi.ajouter_participant(self._liste_joueurs[i])
            self._tournoi.initialiser_rang_participants()
            log.info("ajout 8 joueurs ok")

    def controles_avant_generer_paires(self):
        """
        Contrôles avant de générer les paires de joueurs
        """
        self._controles_ok = False
        try:
            self.controles_avant_ajout_joueurs()
        except exception.TournoiException as ex:
            raise ex
        if self._tournoi.nombre_de_joueurs_inscrits == 0:
            message = "Vous devez d'abord ajouter des joueurs au tournoi"
            raise exception.TournoiException(message)
        else:
            self._controles_ok = True
        return self._controles_ok

    def generer_paires_joueurs_handler(self):
        """
        Méthode permettant de générer des paires des de joueurs
        """
        try:
            if self.controles_avant_generer_paires():
                self._tournoi.creer_tour(len(self._tournoi.liste_de_tours))
        except exception.TournoiException as ex:
            log.warning(ex)
        else:
            log.info("generer_paires_joueurs ok")
            tour = self._tournoi.liste_de_tours[-1]
            titre = f"Liste des matchs du tour {tour.nom}"
            entete = []
            ListView(titre, entete, tour._liste_de_matchs).display()

    def mettre_a_jour_score_du_match(self, match):
        """
        Méthode permettant de mettre à jour le score d'un match
        """
        try:
            score_01, score_02 = MatchForm(match).mettre_a_jour_score()
            match.update_score(score_01, score_02)
        except exception.MatchException as ex:
            log.warning(ex)
            return self.mettre_a_jour_score_du_match(match)
        else:
            log.info("mise à jour score du match ok")

    def confirmer_resultats_du_tour(self, tour):
        """
        Méthode permettant de confirmer les résultats d'un tour puis de le
        cloturer
        """
        titre = f"Liste des matchs du tour {tour.nom}"
        entete = []
        ListView(titre, entete, tour._liste_de_matchs).display()
        if TourForm().iscompleted():
            tour.cloturer()
            try:
                self._tournoi.update_nombre_de_points(tour._liste_de_matchs)
            except exception.TournoiException as ex:
                log.error(ex)
                sys.exit(1)
            else:
                message = f"confirmation résultats : tour {tour.nom} terminé"
                log.info(message)
        else:
            for match in tour.liste_de_matchs:
                match.reset_score()
        if len(self._tournoi.liste_de_tours) >= self._tournoi.nombre_de_tours:
            self._tournoi.cloturer()
            self.enregistrer_handler()
            titre = f"Classement final du tournoi {self._tournoi.nom}"
        else:
            tour = self._tournoi.liste_de_tours[-1]
            titre = f"Classement du tournoi {self._tournoi.nom} "
            titre += f"à l'issue du tour {tour.nom}"
        entete = ['id', 'nom', 'prenom', 'date_de_naissance', 'sexe',
                  'classement', 'nombre_de_points', 'rang']
        ListView(titre, entete, self._tournoi.liste_de_participants).display()

    def controles_avant_entrer_resultats(self):
        """
        Contrôles avant d'entrer des resultats
        """
        if self._tournoi is None or not isinstance(self._tournoi, Tournoi):
            message = "Vous devez d'abord créer un tournoi"
            raise exception.TournoiException(message)
        elif len(self._tournoi.liste_de_tours) == 0:
            message = "Vous devez d'abord générer des paires de joueurs"
            raise exception.TournoiException(message)
        elif self._tournoi.liste_de_tours[-1].statut == "terminé":
            message = f"tour {self._tournoi.liste_de_tours[-1].nom} terminé"
            raise exception.TournoiException(message)

    def entrer_resultats_handler(self):
        """
        Méthode permettant d'entrer les scores des match d'un tour
        """
        try:
            self.controles_avant_entrer_resultats()
        except exception.TournoiException as ex:
            log.warning(ex)
        else:
            tour = self._tournoi.liste_de_tours[-1]
            for match in tour.liste_de_matchs:
                self.mettre_a_jour_score_du_match(match)
            self.confirmer_resultats_du_tour(tour)

    def enregistrer_handler(self):
        """
        Méthode permettant de sauvegarder le tournoi en cours
        """
        if self._tournoi is None or not isinstance(self._tournoi, Tournoi):
            log.warning("Vous devez d'abord créer ou charger un tournoi")
        else:
            self._tournoi.update()
            log.info("enregistrement tournoi ok")
            if self._jeton == "vérouillé":
                self._jeton = "libre"

    def charger_tournoi_handler(self):
        """
        Méthode de récupérer les données d'un tournoi depuis sa dernière
        sauvegarde en base à partir de son id ou
        """
        try:
            self.controles_avant_creer_tournoi()
        except exception.TournoiException as ex:
            log.warning(ex)
        else:
            try:
                methode_acces = TournoiForm().recuperer_methode_acces()
                if methode_acces == "id":
                    id_tournoi = TournoiForm().recuperer_id_tournoi()
                    tournoi = Tournoi.read(id_tournoi)
                else:
                    index = TournoiForm().recuperer_identifiants_tournoi()
                    tournoi = Tournoi.read_by_index(**index)
                    tournoi._liste_de_tours.sort(key=attrgetter('id'))
            except exception.TournoiException as ex:
                log.warning(ex)
                return self.charger_tournoi_handler()
            except exception.TournoiDAOException as ex:
                log.warning(ex)
            else:
                self._tournoi = tournoi
                data = dict((attr[1:], value) for (attr, value)
                            in tournoi.__dict__.items()
                            if not isinstance(value, list))
                log.info("chargement tournoi ok")
                DetailView("Le tournoi suivant est chargé en mémoire",
                           data).display()

    def quitter_handler(self):
        """
        Methode permettant de quitter le programme
        """
        log.info("Fin du sous-programme tournoi")
        sys.exit(0)

    __handlers = {'0': creer_tournoi_handler,
                  '1': ajouter_n_joueurs_handler,
                  '2': generer_paires_joueurs_handler,
                  '3': entrer_resultats_handler,
                  '4': enregistrer_handler,
                  '5': charger_tournoi_handler,
                  '6': quitter_handler}

    def start(self):
        """
        Methode permettant de lancer le controller
        En fonction du choix saisi par l'utilisateur un "handler" ou
        gestionnaire est appelé pour effectuer la fonction choisie
        """
        while ControllerTournoi.__liste_de_choix[self._choix]:
            ControllerTournoi.__handlers[str(self._choix)](self)
            self._choix = self._menu.get_choix()

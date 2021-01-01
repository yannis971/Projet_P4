# -*-coding:utf-8 -*
"""
Module rapport définissant les différentes classes Rapport
"""
from abc import ABC, abstractmethod
import pandas as pd


class AbstractRapport(ABC):
    """
    classe asbstraite Rapport
    """
    def __init__(self, titre):
        self._titre = titre
        self._data_frame = None

    @abstractmethod
    def set_data_frame(self, list_of_objects):
        pass

    def display(self):
        """
        Methode d'affichage des données stockées sous forme de DataFrame
        """
        if self._data_frame is None:
            print("Il n' y a rien à afficher")
        else:
            print(f"\n{self._titre}\n")
            print(self._data_frame)


class JoueurRapport(AbstractRapport):
    """
    classe permettant d'afficher une liste de joueurs
    """
    def set_data_frame(self, liste_de_joueurs):
        """
        Redéfinition de la méthode set_data_frame pour une liste de joueurs
        """
        data = {
            'id': [joueur.id for joueur in liste_de_joueurs],
            'nom': [joueur.nom for joueur in liste_de_joueurs],
            'prenom': [joueur.prenom for joueur in liste_de_joueurs],
            'sexe': [joueur.sexe for joueur in liste_de_joueurs],
            'classement': [joueur.classement for joueur in liste_de_joueurs]
        }
        if hasattr(liste_de_joueurs[0], 'nombre_de_points'):
            data['nombre_de_points'] = [joueur.nombre_de_points for joueur
                                        in liste_de_joueurs]
        if hasattr(liste_de_joueurs[0], 'rang'):
            data['rang'] = [joueur.rang for joueur in liste_de_joueurs]
        self._data_frame = pd.DataFrame(data)


class TournoiRapport(AbstractRapport):
    """
    classe permettant d'afficher une liste de tournois
    """
    def set_data_frame(self, liste_de_tournois):
        """
        Redéfinition de la méthode set_data_frame pour une liste de tournois
        """
        data = {
            'id': [tournoi.id for tournoi in liste_de_tournois],
            'nom': [tournoi.nom for tournoi in liste_de_tournois],
            'lieu': [tournoi.lieu for tournoi in liste_de_tournois],
            'nombre_de_joueurs_inscrits': [tournoi.nombre_de_joueurs_inscrits
                                           for tournoi in liste_de_tournois],
            'nombre_de_tours': [tournoi.nombre_de_tours for tournoi in
                                liste_de_tournois],
            'statut': [tournoi.statut for tournoi in liste_de_tournois],
            'controle_du_temps': [tournoi.controle_du_temps for tournoi in
                                  liste_de_tournois],
            'date_de_debut': [tournoi.date_de_debut for tournoi in
                              liste_de_tournois],
            'date_de_fin': [tournoi.date_de_fin for tournoi in
                            liste_de_tournois],
            'description': [tournoi.description for tournoi in
                            liste_de_tournois]
        }
        self._data_frame = pd.DataFrame(data)


class TourRapport(AbstractRapport):
    """
    classe permettant d'afficher une liste des tours d'un tournoi
    """
    def set_data_frame(self, liste_de_tours):
        """
        Redéfinition de la méthode set_data_frame pour une liste de tours
        """
        data = {
            'id': [tour.id for tour in liste_de_tours],
            'nom': [tour.nom for tour in liste_de_tours],
            'date_heure_debut': [tour.date_heure_debut for tour in
                                 liste_de_tours],
            'date_heure_fin': [tour.date_heure_fin for tour in liste_de_tours],
            'statut': [tour.statut for tour in liste_de_tours]
        }
        self._data_frame = pd.DataFrame(data)


class MatchRapport(AbstractRapport):
    """
    classe permettant d'afficher une liste des matchs d'un tour
    """
    def set_data_frame(self, liste_de_matchs):
        """
        Redéfinition de la méthode set_data_frame pour une liste de matchs
        """
        data = {
            'id': [match.id for match in liste_de_matchs],
            'match': [f"{match.paire_de_joueurs[0].nom} - " +
                      f"{match.paire_de_joueurs[1].nom}"
                      for match in liste_de_matchs],
            'score': [f"{match.score[0]} - {match.score[1]}" for match in
                      liste_de_matchs]
        }
        self._data_frame = pd.DataFrame(data)

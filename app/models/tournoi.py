# -*-coding:utf-8 -*
"""
Module tournoi décrivant la classe Tournoi
"""
from datetime import datetime
from operator import attrgetter
from typing import Generator

from app.dao.tournoi_dao import TournoiDAO
from app.models.exception import TournoiException
from app.models.joueur import Joueur
from app.models.tour import Tour
from app.models.match import Match
from app.utils import util


class Tournoi:
    """
    Classe décrivant un tournoi d'échecs
    """
    __list_attrs = ['_nom', '_lieu', '_date_de_debut', '_date_de_fin',
                    '_nombre_de_tours', '_controle_du_temps', '_description']

    def __init__(self, **tournoi_properties):
        for (attr_name, attr_value) in tournoi_properties.items():
            setattr(self, attr_name, attr_value)
        self.check_attrs()
        self._liste_de_tours = list()
        self._nombre_de_joueurs_inscrits = 0
        self._liste_de_participants = list()
        if not hasattr(self, '_statut'):
            self._statut = "en cours"
        if not hasattr(self, '_matchs_deja_joues'):
            self._matchs_deja_joues = dict()

    def __str__(self):
        return f"Tournoi : {self._nom} {self._lieu} {self._date_de_debut} " \
               f" {self._date_de_fin}"

    def check_attrs(self):
        """
        Methode vérifiant que l'instance de Tournoi contient tous les attributs
        définissant un un objet de type Tournoi
        """
        for attr in Tournoi.__list_attrs:
            if not hasattr(self, attr):
                message = f"objet de type Tournoi sans propriété : {attr[1:]}"
                raise TournoiException(message)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int) and value > 0:
            self._id = value
        else:
            raise TournoiException(f"id du tournoi invalide : {value}")

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        if isinstance(value, str) and len(value) > 1:
            self._nom = value
        else:
            raise TournoiException(f"nom du tournoi invalide : {value}")

    @property
    def lieu(self):
        return self._lieu

    @lieu.setter
    def lieu(self, value):
        if isinstance(value, str) and len(value) > 1:
            self._lieu = value
        else:
            raise TournoiException(f"lieu du tournoi invalide : {value}")

    @property
    def date_de_debut(self):
        return self._date_de_debut

    @date_de_debut.setter
    def date_de_debut(self, value):
        if isinstance(value, str) and util.is_date_valid(value):
            self._date_de_debut = value
        else:
            message = f"date de début du tournoi  invalide : {value}"
            raise TournoiException(message)

    @property
    def date_de_fin(self):
        return self._date_de_fin

    @date_de_fin.setter
    def date_de_fin(self, value):
        if isinstance(value, str) and util.is_date_valid(value):
            if value >= self._date_de_debut:
                self._date_de_fin = value
            else:
                message = f"date de fin du tournoi {value} inférieure à la "
                message += f"date de début {self._date_de_fin}"
                raise TournoiException(message)
        else:
            message = f"date de début du tournoi invalide : {value}"
            raise TournoiException(message)

    @property
    def liste_de_tours(self):
        return self._liste_de_tours

    @property
    def nombre_de_tours(self):
        return self._nombre_de_tours

    @nombre_de_tours.setter
    def nombre_de_tours(self, value):
        if isinstance(value, int) and value > 0:
            self._nombre_de_tours = value
        else:
            raise TournoiException(f"nombre de tours invalide : {value}")

    @property
    def controle_du_temps(self):
        return self._controle_du_temps

    @controle_du_temps.setter
    def controle_du_temps(self, value):
        if isinstance(value, str) \
                and value in ("bullet", "blitz", "coup rapide"):
            self._controle_du_temps = value
        else:
            raise TournoiException(f"controle du temps invalide : {value}")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, str) and len(value) > 8:
            self._description = value
        else:
            message = "description invalide ou inférieure à 8 caractères : "
            message += f"{value}"
            raise TournoiException(message)

    @property
    def nombre_de_joueurs_inscrits(self):
        return self._nombre_de_joueurs_inscrits

    @nombre_de_joueurs_inscrits.setter
    def nombre_de_joueurs_inscrits(self, value):
        if isinstance(value, int) and value >= 0:
            self._nombre_de_joueurs_inscrits = value
        else:
            message = f"nombre_de_joueurs_inscrits invalide : {value}"
            raise TournoiException(message)

    @property
    def liste_de_participants(self):
        self.trier_liste_de_participants()
        return self._liste_de_participants

    @property
    def statut(self):
        return self._statut

    @statut.setter
    def statut(self, value):
        if isinstance(value, str) and value in ["en cours", "terminé"]:
            self._statut = value
        else:
            raise TournoiException(f"statut du tournoi invalide : {value}")

    @property
    def matchs_deja_joues(self):
        return self._matchs_deja_joues

    @matchs_deja_joues.setter
    def matchs_deja_joues(self, value):
        if isinstance(value, dict):
            self._matchs_deja_joues = value
        else:
            raise TournoiException(f"matches_deja_joues invalide : {value}")

    def ajouter_participant(self, joueur):
        """
        Méthode ajoutant un joueur à la liste des participants au tournoi
        """
        if isinstance(joueur, Joueur):
            if joueur not in self._liste_de_participants:
                joueur.rang = 0
                joueur.nombre_de_points = 0
                self._liste_de_participants.append(joueur)
                self._nombre_de_joueurs_inscrits += 1
            else:
                message = f"joueur {joueur} déjà inscrit au tournoi"
                raise TournoiException(message)
        else:
            message = f"ajouter_participant bad argument : {joueur}"
            raise TournoiException(message)

    def initialiser_rang_participants(self):
        """
        Cette méthode est appelée par le controleur de Tournoi après avoir
        inscrit les N joueurs paricipants
        Cette méthode initialise le rang des participants au tournoi
        """
        self._liste_de_participants.sort(key=attrgetter('classement'))
        rang = 1
        for joueur in self._liste_de_participants:
            joueur.rang = rang
            rang += 1

    def finaliser_rang_participants(self):
        """
        Methode appelée lorsque l'on cloture un tournoi
        afin d'établir le classement final du tournoi
        """
        if self._statut == "en cours":
            message = f"{self._nom} en cours : impossible de finaliser"
            message += " le classement"
            raise TournoiException(message)
        else:
            self.trier_liste_de_participants()
            rang = 1
            for joueur in self._liste_de_participants:
                joueur.rang = rang
                rang += 1

    def trier_liste_de_participants(self):
        """
        Méthode qui va trier la liste des participants au tournoi
        sur le nombre de points décroissant
        En cas d'égalité sur le nombre de points, on trie sur le rang
        dans l'ordre ascendant
        """
        # tri par rang croissant
        liste_triee_par_rang = sorted(self._liste_de_participants,
                                      key=attrgetter('rang'))
        # tri par nombre de points décroissant
        self._liste_de_participants = \
            sorted(liste_triee_par_rang,
                   key=attrgetter('nombre_de_points'),
                   reverse=True)

    def is_match_deja_joue(self, paire_de_joueurs):
        """
        Methode qui teste si un macth a déjà été joué au cours du tournoi
        """
        cle = f"{paire_de_joueurs[0].id} {paire_de_joueurs[1].id}"
        try:
            return self._matchs_deja_joues[cle]
        except KeyError:
            cle_inverse = f"{paire_de_joueurs[1].id} {paire_de_joueurs[0].id}"
            try:
                return self._matchs_deja_joues[cle_inverse]
            except KeyError:
                return False

    def intervertir_participants(self, indice):
        """
        Methode qui intervertit un joueur de la première moitié du classement
        avec un joueur de la deuxième moitié du classement
        en partant des joueurs les moins biens classés
        """
        i_min = int(self._nombre_de_joueurs_inscrits / 2) - indice
        i_max = -1 - indice
        (self._liste_de_participants[i_min],
         self._liste_de_participants[i_max]) = \
            (self._liste_de_participants[i_max],
             self._liste_de_participants[i_min])

    def paires_premier_tour(self):
        """
        Génération des paires de joueurs au premier tour
        """
        indice_milieu = int(self._nombre_de_joueurs_inscrits / 2)
        joueurs_tableau_01 = self._liste_de_participants[:indice_milieu]
        joueurs_tableau_02 = self._liste_de_participants[indice_milieu:]
        return [list(item) for item
                in zip(joueurs_tableau_01, joueurs_tableau_02)]

    def paires_autres_tours(self):
        """
        Génération des paires de joueurs sur les tours autres que le
        premier tour
        """
        liste_participants = list(self._liste_de_participants)
        indice_inversion = 0
        indice_milieu = int(self._nombre_de_joueurs_inscrits / 2)
        liste_de_paires_de_joueurs = list()
        while liste_participants:
            for i in range(1, len(liste_participants), 1):
                paire_de_joueurs = [liste_participants[0],
                                    liste_participants[i]]
                if not self.is_match_deja_joue(paire_de_joueurs):
                    liste_de_paires_de_joueurs.append(paire_de_joueurs)
                    liste_participants.pop(i)
                    liste_participants.pop(0)
                    break
                elif len(liste_participants) == 2 \
                        and indice_inversion < indice_milieu:
                    self.intervertir_participants(indice_inversion)
                    liste_de_paires_de_joueurs = list()
                    liste_participants = list(self._liste_de_participants)
                    indice_inversion += 1
        return liste_de_paires_de_joueurs

    def generer_paires_de_joueurs(self, indice_de_tour):
        """
        Methode permettant de générer des paires de joueurs
        """
        self.trier_liste_de_participants()
        return self.paires_premier_tour() if indice_de_tour == 0 \
            else self.paires_autres_tours()

    def creer_tour(self, indice_de_tour):
        """
          Méthode permettant de créer un tour
        """
        nom = f"Round {indice_de_tour + 1}"
        dico = {'nom': nom,
                'date_heure_debut': util.encode_date_heure(datetime.now()),
                'date_heure_fin': '9999-12-31T12:00:00'}
        tour = Tour(**dico)
        tour.liste_de_matchs = [Match(*paire_de_joueurs)
                                for paire_de_joueurs in
                                self.generer_paires_de_joueurs(indice_de_tour)]
        self._liste_de_tours.append(tour)
        for match in tour.liste_de_matchs:
            cle = f"{match.paire_de_joueurs[0].id} "
            cle += f"{match.paire_de_joueurs[1].id}"
            self._matchs_deja_joues[cle] = 1

    def cloturer(self):
        """
          Méthode permettant de cloturer un tour
        """
        self._date_de_fin = util.encode_date(datetime.now())
        self._statut = "terminé"
        self.finaliser_rang_participants()

    def create(self):
        """
        Crée le tournoi dans la base de données
        """
        TournoiDAO().create(self)

    @classmethod
    def read_all(cls):
        """
        Renvoie la liste des tournois stockés dans la base de données
        sous forme d'objet generator
        """
        return TournoiDAO().read_all()

    @classmethod
    def read(cls, id_tournoi):
        """
        Recherche le tournoi dans la base de données à partir de son id
        Et renvoie l'instance de tournoi correspondante
        """
        tournoi = TournoiDAO().read(id_tournoi)
        tournoi.gen_to_list()
        return tournoi

    @classmethod
    def read_by_index(cls, nom, lieu, date_de_debut):
        """
        Recherche le tournoi dans la base de données à partir de son index
        nom + lieu + date_de_debut
        Et renvoie l'instance de tournoi correspondante
        """
        tournoi = TournoiDAO().read_by_index(nom, lieu, date_de_debut)
        tournoi.gen_to_list()
        return tournoi

    def update(self):
        """
        Met à jour le tournoi dans la base de données
        """
        TournoiDAO().update(self)

    def gen_to_list(self):
        """
        Transforme les attributs de type 'generator' en 'list'
        Afin que l'utilisateur de l'instance du tournoi puisse utiliser
        les méthodes de listes sur les attributs censés être des listes
        """
        if isinstance(self._liste_de_participants, Generator):
            self._liste_de_participants = list(self._liste_de_participants)
        if isinstance(self._liste_de_tours, Generator):
            self._liste_de_tours = list(self._liste_de_tours)

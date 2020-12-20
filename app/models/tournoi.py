# -*-coding:utf-8 -*

from datetime import datetime
from operator import attrgetter
from app.models.exception import TournoiException
from app.models.joueur import Joueur
from app.models.tour import Tour
from app.models.match import Match
from app.utils import util


class Tournoi:
    __list_attrs = ['_nom', '_lieu', '_date_de_debut', '_date_de_fin',
                    '_nombre_de_tours', '_controle_du_temps', '_description']

    def __init__(self, **tournoi_properties):
        for (attr_name, attr_value) in tournoi_properties.items():
            setattr(self, attr_name, attr_value)
        self.check_attrs()
        self._liste_de_tours = list()
        self._liste_indices_joueurs_inscrits = list()
        self._nombre_joueurs_inscrits = 0
        self._liste_de_participants = list()

    def __str__(self):
        return f"Tournoi : {self._nom} {self._lieu} {self._date_de_debut} {self._date_de_fin}"

    def check_attrs(self):
        for attr in Tournoi.__list_attrs:
            if not hasattr(self, attr):
                raise TournoiException(f"objet de type Tournoi sans propriété : {attr[1:]}")

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
            date_du_jour = util.encode_date(datetime.now())
            if value >= date_du_jour:
                self._date_de_debut = value
            else:
                raise TournoiException(f"date de début du tournoi {value} inférieure à la date du jour {date_du_jour}")
        else:
            raise TournoiException(f"date de début du tournoi invalide : {value}")

    @property
    def date_de_fin(self):
        return self._date_de_fin

    @date_de_fin.setter
    def date_de_fin(self, value):
        if isinstance(value, str) and util.is_date_valid(value):
            if value >= self._date_de_debut:
                self._date_de_fin = value
            else:
                raise TournoiException(
                    f"date de fin du tournoi {value} inférieure à la date de début {self._date_de_fin}")
        else:
            raise TournoiException(f"date de début du tournoi invalide : {value}")

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
        if isinstance(value, str) and value in ("bullet", "blitz", "coup rapide"):
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
            raise TournoiException(f"description invalide ou inférieure à 8 caractères : {value}")

    @property
    def nombre_joueurs_inscrits(self):
        return self._nombre_joueurs_inscrits

    @property
    def liste_de_participants(self):
        self.trier_liste_de_participants()
        return self._liste_de_participants

    def ajouter_joueur(self, indice_joueur):
        if isinstance(indice_joueur, int) and indice_joueur >= 0:
            if indice_joueur in self._liste_indices_joueurs_inscrits:
                raise TournoiException(f"joueur indice {indice_joueur} déjà inscrit au tournoi")
            else:
                self._liste_indices_joueurs_inscrits.append(indice_joueur)
                self._nombre_joueurs_inscrits += 1
        else:
            raise TournoiException(f"indice_joueur invalide : {indice_joueur}")

    def ajouter_participant(self, joueur):
        if isinstance(joueur, Joueur):
            if joueur in self._liste_de_participants:
                raise TournoiException(f"joueur {joueur} déjà inscrit au tournoi")
            else:
                joueur.rang = 0
                joueur.nombre_de_points = 0
                self._liste_de_participants.append(joueur)
        else:
            raise TournoiException(f"ajouter_participant attend une instance de joueur en paramètre: {joueur}")

    def initialiser_rang_participants(self):
        self._liste_de_participants.sort(key=attrgetter('classement'))
        rang = 1
        for joueur in self._liste_de_participants:
            joueur.rang = rang
            rang += 1

    def trier_liste_de_participants(self):
        """
        Méthode qui va trier la liste des participants au tournoi sur le nombre de points décroissant
        En cas d'égalité sur le nombre de points, on trie sur le rang dans l'ordre ascendant
        """
        # tri par rang croissant
        liste_triee_par_rang = sorted(self._liste_de_participants, key=attrgetter('rang'))
        # tri par nombre de points décroissant
        self._liste_de_participants = sorted(liste_triee_par_rang, key=attrgetter('nombre_de_points'), reverse=True)

    # mettre liste_matchs_deja_jouers à mettre en attribut de tournoi
    # a incrémenter après chaque génération de paires

    def match_deja_joue(self, paire_de_joueurs, liste_matchs_deja_joues):
        # cette methode est à revoir
        return paire_de_joueurs in liste_matchs_deja_joues or reversed(paire_de_joueurs) in liste_matchs_deja_joues

    def generer_paires_de_joueurs(self, indice_de_tour):
        self.trier_liste_de_participants()
        liste_de_paires_de_joueurs = list()

        if indice_de_tour == 0:
            indice_separateur = int(self._nombre_joueurs_inscrits/2)
            joueurs_du_premier_tableau = self._liste_de_participants[:indice_separateur]
            joueurs_du_deuxieme_tableau = self._liste_de_participants[indice_separateur:]
            liste_de_paires_de_joueurs = [list(item) for item in zip(joueurs_du_premier_tableau,
                                                                     joueurs_du_deuxieme_tableau)]
        else:
            # faire un dictionnaire avec clé un tuple contenant les id des joueurs
            liste_matchs_deja_joues = [match.paire_de_joueurs for tour in self._liste_de_tours for match in tour.liste_de_matchs]
            if indice_de_tour == 3:
                print("liste de matchs deja joues")
                for item in liste_matchs_deja_joues:
                    print(f"{item[0].nom} - {item[1].nom}")
            liste_participants = list(self._liste_de_participants)
            while liste_participants:
                #print("len(liste_participants) =", len(liste_participants))
                for i in range(1, len(liste_participants), 1):
                    paire_de_joeurs = [liste_participants[0], liste_participants[i]]
                   #print(f"{paire_de_joueurs[0].nom} - {paire_de_joueurs[1].nom}")
                    if not self.match_deja_joue(paire_de_joueurs, liste_matchs_deja_joues):
                        print("0", i, "append", f"{paire_de_joueurs[0].nom} - {paire_de_joueurs[1].nom}")
                        liste_de_paires_de_joueurs.append(paire_de_joueurs)
                        liste_participants.pop(i)
                        liste_participants.pop(0)
                        break

        return liste_de_paires_de_joueurs

    def creer_tour(self, indice_de_tour):
        nom = f"Round {indice_de_tour + 1}"
        dico = {'nom': nom, 'date_heure_debut': util.encode_date_heure(datetime.now()), 'date_heure_fin': '9999-12-31T12:00:00'}
        tour = Tour(**dico)
        tour.liste_de_matchs = [Match(*paire_de_joueurs) for paire_de_joueurs in
                                self.generer_paires_de_joueurs(indice_de_tour)]
        self._liste_de_tours.append(tour)

    def create(self):
        pass

    @classmethod
    def read_all(cls):
        return []
    # return TournoiDAO().read_all()

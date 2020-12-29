# -*-coding:utf-8 -*
"""
Module tour décrivant la classe Tour
"""
from datetime import datetime
from app.models.exception import TourException
from app.models.match import Match
from app.utils import util


class Tour:
    """
    Classe décrivant un tour dans un tournoi d'échecs
    """
    __list_attrs = ['_nom', '_date_heure_debut', '_date_heure_fin']

    def __init__(self, **joueur_properties):
        for (attr_name, attr_value) in joueur_properties.items():
            setattr(self, attr_name, attr_value)
        self.check_attrs()
        self._liste_de_matchs = list()
        if not hasattr(self, '_statut'):
            self._statut = "en cours"

    def __str__(self):
        return f"Tour: {self._nom} {self._date_heure_debut} \
                {self._date_heure_fin} {self.statut}"

    def check_attrs(self):
        """
        Methode vérifiant que l'instance de Tour contient tous les attributs
        définissant un un objet de type Tour
        """
        for attr in Tour.__list_attrs:
            if not hasattr(self, attr):
                message = f"objet de type Tour sans propriété : {attr[1:]}"
                raise TourException(message)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int) and value >= 0:
            self._id = value
        else:
            raise TourException(f"id du tour invalide : {value}")

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        if isinstance(value, str):
            self._nom = value
        else:
            raise TourException(f"libelle du tour invalide : {value}")

    @property
    def date_heure_debut(self):
        return self._date_heure_debut

    @date_heure_debut.setter
    def date_heure_debut(self, value):
        if isinstance(value, str) and util.is_date_heure_valid(value):
            self._date_heure_debut = value
        else:
            raise TourException(f"date_heure_debut invalide : {value}")

    @property
    def date_heure_fin(self):
        return self._date_heure_fin

    @date_heure_fin.setter
    def date_heure_fin(self, value):
        if isinstance(value, str) and util.is_date_heure_valid(value):
            date_heure_debut = util.decode_date_heure(self._date_heure_debut)
            if util.decode_date_heure(value) >= date_heure_debut:
                self._date_heure_fin = value
            else:
                message = f"date_heure_fin ({value}) < date_heure_debut "
                message += f"{self._date_heure_debut}"
                raise TourException(message)
        else:
            raise TourException(f"date_heure_fin invalide : {value}")

    @property
    def liste_de_matchs(self):
        return self._liste_de_matchs

    @liste_de_matchs.setter
    def liste_de_matchs(self, values):
        self._liste_de_matchs = []
        for value in values:
            self.ajouter_match(value)

    @property
    def statut(self):
        return self._statut

    @statut.setter
    def statut(self, value):
        if isinstance(value, str) and value in ["en cours", "terminé"]:
            self._statut = value
        else:
            raise TourException(f"statut du tour invalide : {value}")

    def ajouter_match(self, value):
        """
        Méthode permettant d'ajouter un match à la liste des matchs du tour
        """
        if isinstance(value, Match):
            if value not in self._liste_de_matchs:
                self._liste_de_matchs.append(value)
            else:
                message = f"instance de match {value} en double "
                message += f"dans un tour {self}"
                raise TourException(message)
        else:
            message = f"l'objet ajouté n'est pas de type Match : {value}"
            raise TourException(message)

    def cloturer(self):
        """
        Méthode permetant de cloturer un tour
        """
        self._date_heure_fin = util.encode_date_heure(datetime.now())
        self._statut = "terminé"

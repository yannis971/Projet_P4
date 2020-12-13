# -*-coding:utf-8 -*

from app.models.exception import TourException
from app.models.match import Match
from app.utils import util


class Tour:

    __list_attrs = ['_nom', '_date_heure_debut', 'date_heure_de_fin' ]

    def __init__(self, **joueur_properties):
        for (attr_name, attr_value) in joueur_properties.items():
            setattr(self, attr_name, attr_value)
        self.check_attrs()
        self._liste_de_matchs = list()

    def __str__(self):
        return (f"Tour: {self._nom} {self._date_heure_debut} {self._date_heure_fin}")

    def check_attrs(self):
        for attr in Tour.__list_attrs:
            if not hasattr(self, attr):
                raise TourException(f"objet de type Tour sans propriété : {attr[1:]}")

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
            if util.decode_date_heure(value) >= util.decode_date_heure(self._date_heure_debut):
                self._date_heure_fin = value
            else:
                raise TourException(f"date_heure_fin ({value}) < date_heure_debut ({self._date_heure_debut}) ")
        else:
            raise TourException(f"date_heure_fin invalide : {value}")

    def ajouter_match(self, value):
        if isinstance(value, Match):
            if value not in self._liste_de_matchs:
                self._liste_de_matchs.append(value)
            else:
                raise TourException(f"instance de match {value} en double dans un tour {self}")
        else:
            raise TourException(f"la méthode ajouter_match attend un objet de type Match en paramètre, or on a {value}")

    @property
    def liste_de_matchs(self):
        return self._liste_de_matchs

    @liste_de_matchs.setter
    def liste_de_matchs(self, values):
        self._liste_de_matchs = []
        for value in values:
            self.ajouter_match(value)
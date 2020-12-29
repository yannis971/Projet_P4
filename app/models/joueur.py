# -*-coding:utf-8 -*
"""
Module joueur décrivant la classe Joueur
"""

from datetime import datetime
from datetime import timedelta

from app.dao.joueur_dao import JoueurDAO
from app.models.exception import JoueurException
from app.utils import util


class Joueur:
    """
    Class describing a chess player
    """
    __list_attrs = ['_nom', '_prenom', '_date_de_naissance',
                    '_sexe', '_classement']

    def __init__(self, **joueur_properties):
        for (attr_name, attr_value) in joueur_properties.items():
            setattr(self, attr_name, attr_value)
        self.check_attrs()

    def __str__(self):
        chaine = f"Joueur : {self._nom} {self._prenom} "
        chaine += f"{self._date_de_naissance} {self._sexe} {self._classement}"
        if hasattr(self, 'rang'):
            chaine += f" {self.rang}"
        if hasattr(self, 'nombre_de_points'):
            chaine += f" {self.nombre_de_points}"
        return chaine

    def check_attrs(self):
        """
        Methode vérifiant que l'instance de Joueur contient tous les attributs
        définissant un un objet de type Joueur
        """
        for attr in Joueur.__list_attrs:
            if not hasattr(self, attr):
                message = f"objet de type Joueur sans propriété : {attr[1:]}"
                raise JoueurException(message)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int) and value > 0:
            self._id = value
        else:
            raise JoueurException(f"id du joueur invalide : {value}")

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        if isinstance(value, str):
            self._nom = value
        else:
            raise JoueurException(f"nom du joueur invalide : {value}")

    @property
    def prenom(self):
        return self._prenom

    @prenom.setter
    def prenom(self, value):
        if isinstance(value, str):
            self._prenom = value
        else:
            raise JoueurException(f"prenom du joueur invalide : {value}")

    @property
    def sexe(self):
        return self._sexe

    @sexe.setter
    def sexe(self, value):
        if isinstance(value, str) and value.strip().upper() in ['F', 'M']:
            self._sexe = value
        else:
            raise JoueurException(f"sexe du joueur invalide : {value}")

    @property
    def date_de_naissance(self):
        return self._date_de_naissance

    @date_de_naissance.setter
    def date_de_naissance(self, value):
        if isinstance(value, str) and util.is_date_valid(value):
            date_moins_6_ans = datetime.now() - timedelta(days=2191, hours=12)
            if util.decode_date(value) < date_moins_6_ans:
                self._date_de_naissance = value
            else:
                raise JoueurException(f"le joueur a moins de 6 ans : {value}")
        else:
            raise JoueurException(f"date de naissance invalide : {value}")

    @property
    def classement(self):
        return self._classement

    @classement.setter
    def classement(self, value):
        if isinstance(value, int) and value > 0:
            self._classement = value
        else:
            raise JoueurException(f"classement du joueur invalide : {value}")

    def create(self):
        """
        Crée le joueur dans la base de données
        """
        JoueurDAO().create(self)

    @classmethod
    def read_all(cls):
        """
        Renvoie la liste des joueurs stockés dans la base de données
        """
        return JoueurDAO().read_all()

    @classmethod
    def read(cls, id_joueur):
        """
        Recherche le joueur dans la base de données à partir de son id
        Et renvoie l'instance de joueur correspondante
        """
        return JoueurDAO().read(id_joueur)

    @classmethod
    def read_by_index(cls, nom, prenom, date_de_naissance):
        """
        Recherche le joueur dans la base de données à partir de son index
        nom + prenom + date_de_naissance
        Et renvoie l'instance de tournoi correspondante
        """
        return JoueurDAO().read_by_index(nom, prenom, date_de_naissance)

    def update(self):
        """
        Met à jour le joueur dans la base de données
        """
        JoueurDAO().update(self)

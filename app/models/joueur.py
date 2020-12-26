# -*-coding:utf-8 -*

from datetime import datetime, timedelta
from app.models.exception import JoueurException
from app.utils import util
from app.dao.joueurDAO import JoueurDAO


class Joueur:

    __list_attrs = ['_nom', '_prenom', '_date_de_naissance', '_sexe', '_classement']

    def __init__(self, **joueur_properties):
        for (attr_name, attr_value) in joueur_properties.items():
            setattr(self, attr_name, attr_value)
        self.check_attrs()

    def __str__(self):
        description_joueur = f"Joueur : {self._nom} {self._prenom} {self._date_de_naissance} {self._sexe} {self._classement}"
        if hasattr(self, 'nombre_de_points'):
            description_joueur += f" {self.nombre_de_points}"
        return description_joueur

    def check_attrs(self):
        for attr in Joueur.__list_attrs:
            if not hasattr(self, attr):
                raise JoueurException(f"objet de type Joueur sans propriété : {attr[1:]}")

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
        JoueurDAO().create(self)

    @classmethod
    def read_all(cls):
        return JoueurDAO().read_all()

    @classmethod
    def read(cls, id):
        return JoueurDAO().read(id)

    @classmethod
    def read_by_index(cls, nom, prenom, date_de_naissance):
        return JoueurDAO().read_by_index(nom, prenom, date_de_naissance)

    def update(self):
        JoueurDAO().update(self)

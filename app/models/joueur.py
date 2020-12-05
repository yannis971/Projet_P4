# -*-coding:utf-8 -*

from datetime import datetime, timedelta
from app.models.exception import JoueurException
from app.utils import util


class Joueur:

    __id = 0
    __list_attrs = ['_nom', '_prenom', '_date_de_naissance', '_sexe', '_classement']

    def __init__(self, **joueur_properties):
        for (attr_name, attr_value) in joueur_properties.items():
            setattr(self, attr_name, attr_value)
        self.check_attrs()
        Joueur.__id += 1
        if not hasattr(self, '_id'):
            self._id = Joueur.__id

    def __str__(self):
        return f"Joueur : {self._id } {self._nom} {self._prenom} {self._date_de_naissance} {self._sexe} {self._classement}"

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

if __name__ == "__main__":
    #running controller function
    dico = dict()
    dico['nom'] = "saliniere"
    dico['prenom'] = "yannis"
    dico['date_de_naissance'] = "1977-05-03"
    dico['sexe'] = "M"
    dico['classement'] = 1
    a = Joueur(**dico)
    print(a)
    print(a.nom)
    print(a.date_de_naissance)
    a.classement = 2
    print(a)

    b = Joueur(classemen=3, prenom="jason", nom="statham", date_de_naissance="1977-05-03", sexe="M")
    print(b)
    dico = {'classement': 4, 'prenom': "jean", 'nom': "dico", 'date_de_naissance': "1977-05-03", 'sexe': "M"}
    c = Joueur(**dico)
    print(c)
    c.date_de_naissance = "1977-05-31"
    c.id = 5
    print(c)

    d = Joueur(id=12, classement=3, prenom="jason", nom="statham", date_de_naissance="1977-05-03", sexe="M")
    print(d)

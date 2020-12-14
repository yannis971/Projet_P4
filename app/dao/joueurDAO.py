# -*-coding:utf-8 -*

from tinydb import TinyDB, Query
import app.models.joueur as jx
from app.models.exception import JoueurDAOException

class JoueurDAO:

    _db = TinyDB('db.json')
    _table_joueurs = _db.table("table_joueurs")

    def __init__(self):
        pass

    def create(self, joueur):
        if self.joueur_exists(joueur):
            raise JoueurDAOException(f"Le joueur existe déjà dans la base de données : {joueur}")
        else:
            joueur.id = JoueurDAO._table_joueurs._get_next_id()
            data_storage = dict((attr[1:], value) for (attr, value) in joueur.__dict__.items())
            JoueurDAO._table_joueurs.insert(data_storage)

    def read_all(self):
        return [jx.Joueur(**item) for item in JoueurDAO._table_joueurs.all()]

    def read(self, id):
        return jx.Joueur(JoueurDAO._table_joueurs.get(doc_id=id))

    def read_by_index(self, nom, prenom, date_de_naissance):
        joueur = Query()
        table = JoueurDAO._table_joueurs
        item = table.search((joueur.nom == nom) & (joueur.prenom == prenom) & (joueur.date_de_naissance == date_de_naissance))
        if item:
            return jx.Joueur(**item[0])
        else:
            return None

    def update(self, joueur):
        pass

    def joueur_exists(self, joueur):
        instance_joueur = self.read_by_index(joueur.nom, joueur.prenom, joueur.date_de_naissance)
        if instance_joueur:
            joueur.id = instance_joueur.id
            return True
        else:
            return False
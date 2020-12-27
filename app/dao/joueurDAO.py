# -*-coding:utf-8 -*

from tinydb import TinyDB, Query
import app.models.joueur as jx
from app.models.exception import JoueurDAOException
from app.utils import util

class JoueurDAO:

    _db = TinyDB('db.json', sort_keys=True, indent=4)
    _table_joueurs = _db.table("table_joueurs")

    def __init__(self):
        pass

    def create(self, joueur):
        if self.joueur_exists(joueur):
            raise JoueurDAOException(f"Le joueur existe déjà dans la base de données : {joueur}")
        else:
            joueur.id = JoueurDAO._table_joueurs._get_next_id()
            JoueurDAO._table_joueurs.insert(util.document(joueur))

    def read_all(self):
        return [jx.Joueur(**item) for item in JoueurDAO._table_joueurs.all()]

    def read(self, id):
        return jx.Joueur(**JoueurDAO._table_joueurs.get(doc_id=id))

    def read_by_index(self, nom, prenom, date_de_naissance):
        joueur = Query()
        table = JoueurDAO._table_joueurs
        item = table.search((joueur.nom == nom) & (joueur.prenom == prenom) & (joueur.date_de_naissance == date_de_naissance))
        if item:
            return jx.Joueur(**item[0])
        else:
            raise JoueurDAOException(f"Le joueur n'existe pas dans la base de données : {nom} {prenom} {date_de_naissance}")

    def update(self, joueur):
        try:
            self.read_by_index(joueur.nom, joueur.prenom, joueur.date_de_naissance)
        except JoueurDAOException:
            self.create(joueur)
        else:
            requete = Query()
            JoueurDAO._table_joueurs.update(util.document(joueur), (requete.nom == joueur.nom)
                                            & (requete.prenom == joueur.prenom)
                                            & (requete.date_de_naissance == joueur.date_de_naissance))

    def joueur_exists(self, joueur):
        try:
            instance_joueur = self.read_by_index(joueur.nom, joueur.prenom, joueur.date_de_naissance)
            assert isinstance(instance_joueur, jx.Joueur)
        except JoueurDAOException:
            return False
        except AssertionError:
            return False
        else:
            joueur.id = instance_joueur.id
            return True

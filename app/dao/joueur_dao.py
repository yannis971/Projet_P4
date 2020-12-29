# -*-coding:utf-8 -*
"""
Module joueur_dao décrivant la classe JoueurDAO
"""

from tinydb import TinyDB
from tinydb import Query
import app.models.joueur as jx
from app.models.exception import JoueurDAOException
from app.utils import util


class JoueurDAO:
    """
    Classe JoueurDAO permettant d'accéder aux données Joueur
    """

    _db = TinyDB('db.json', sort_keys=True, indent=4)
    _table_joueurs = _db.table("table_joueurs")

    def __init__(self):
        pass

    def create(self, joueur):
        """
        Méthode permettant de créer un joueur dans la table : "table_joueurs"
        """
        if self.joueur_exists(joueur):
            message = f"Le joueur existe déjà en base : {joueur}"
            raise JoueurDAOException(message)
        else:
            joueur.id = JoueurDAO._table_joueurs._get_next_id()
            JoueurDAO._table_joueurs.insert(util.document(joueur))

    def read_all(self):
        """
        Méthode génératrice de la liste des joueurs
        """
        for document in JoueurDAO._table_joueurs.all():
            yield jx.Joueur(**document)

    def read(self, id):
        """
        Méthode renvoyant une instance de joueur à partir de son id
        """
        document = JoueurDAO._table_joueurs.get(doc_id=id)
        if document:
            return jx.Joueur(**document)
        else:
            message = f"Joueur non trouvé - id : {id}"
            raise JoueurDAOException(message)

    def read_by_index(self, nom, prenom, date_de_naissance):
        """
        Méthode de recherche d'un joueur à partir de ses nom, prénom et
        date de naissance
        """
        joueur = Query()
        table = JoueurDAO._table_joueurs
        item = table.search((joueur.nom == nom) & (joueur.prenom == prenom)
                            & (joueur.date_de_naissance == date_de_naissance))
        if item:
            return jx.Joueur(**item[0])
        else:
            message = "Le joueur n'existe pas dans la base de données : "
            message += f"{nom} {prenom} {date_de_naissance}"
            raise JoueurDAOException(message)

    def update(self, joueur):
        """
        Méthode permettant de mettre à jour un joueur dans la table :
        "table_joueurs"
        """
        try:
            self.read_by_index(joueur.nom, joueur.prenom,
                               joueur.date_de_naissance)
        except JoueurDAOException:
            self.create(joueur)
        else:
            JoueurDAO._table_joueurs.update(util.document(joueur),
                                            doc_ids=[joueur.id])

    def joueur_exists(self, joueur):
        """
        Méthode qui teste si un joueur existe en base
        """
        try:
            instance_joueur = self.read_by_index(joueur.nom,
                                                 joueur.prenom,
                                                 joueur.date_de_naissance)
            assert isinstance(instance_joueur, jx.Joueur)
        except JoueurDAOException:
            return False
        except AssertionError:
            return False
        else:
            joueur.id = instance_joueur.id
            return True

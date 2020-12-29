# -*-coding:utf-8 -*
"""
Module match_dao décrivant la classe MatchDAO
"""
from tinydb import TinyDB
from tinydb import Query
import app.models.match as mx
from app.dao.joueur_dao import JoueurDAO
from app.models.exception import MatchDAOException
from app.utils import util


class MatchDAO:
    """
    Classe MatchDAO permettant d'accéder aux données Match
    """
    _db = TinyDB('db.json', sort_keys=True, indent=4)
    _liens_match_tour = _db.table("liens_match_tour")

    def __init__(self):
        pass

    def create(self, id_tour, match):
        """
        Méthode permettant de créer un match dans la table : "liens_match_tour"
        """
        if self.match_exists(id_tour, match):
            message = f"Le match existe déjà en base de données : {match}"
            raise MatchDAOException(message)
        else:
            match.id = MatchDAO._liens_match_tour._get_next_id()
            document = util.document(self.data_match_tour(id_tour, match))
            MatchDAO._liens_match_tour.insert(document)

    def read_all(self):
        """
        Méthode génératrice de la liste des matchs
        """
        for document in MatchDAO._liens_match_tour.all():
            yield self.generer_instance_match(**document)

    def read(self, id):
        """
        Méthode renvoyant une instance de match à partir de son id
        """
        document = MatchDAO._liens_match_tour.get(doc_id=id)
        if document:
            return self.generer_instance_match(**document)
        else:
            message = f"Match non trouvé - id : {id}"
            raise MatchDAOException(message)

    def read_by_index(self, id_tour, id_joueur_1, id_joueur_2):
        """
        Méthode de recherche d'un match à partir de l'id du tour, de l'id du
        joueur 1 et de l'id du joueur 2
        """
        match = Query()
        table = MatchDAO._liens_match_tour
        item = table.search((match.id_tour == id_tour)
                            & (match.id_joueur_1 == id_joueur_1)
                            & (match.id_joueur_2 == id_joueur_2))
        if item:
            return self.generer_instance_match(**item[0])
        else:
            message = f"Match non trouvé : {id_tour} {id_joueur_1}"
            message += f" {id_joueur_2}"
            raise MatchDAOException(message)

    def read_by_id_tour(self, id_tour):
        match = Query()
        table = MatchDAO._liens_match_tour
        liste_documents = table.search((match.id_tour == id_tour))
        if liste_documents:
            for document in liste_documents:
                yield self.generer_instance_match(**document)
        else:
            return []

    def update(self, id_tour, match):
        try:
            self.read_by_index(id_tour, match.paire_de_joueurs[0].id,
                               match.paire_de_joueurs[1].id)
        except MatchDAOException:
            self.create(id_tour, match)
        else:
            document = util.document(self.data_match_tour(id_tour, match))
            MatchDAO._liens_match_tour.update(document, doc_ids=[match.id])

    def match_exists(self, id_tour, match):
        """
        Méthode qui teste si un match existe en base
        """
        try:
            instance_match = self.read_by_index(id_tour,
                                                match.paire_de_joueurs[0].id,
                                                match.paire_de_joueurs[1].id)
            assert isinstance(instance_match, mx.Match)
        except MatchDAOException:
            return False
        except AssertionError:
            return False
        else:
            return True

    def generer_instance_match(self, **document):
        """
        Méthode qui génère une instance de match à partir d'un document
        """
        premier_joueur = JoueurDAO().read(document['id_joueur_1'])
        premier_joueur.nombre_de_points = 0.0
        deuxieme_joueur = JoueurDAO().read(document['id_joueur_2'])
        deuxieme_joueur.nombre_de_points = 0.0
        paires_de_joueurs = [premier_joueur, deuxieme_joueur]
        match = mx.Match(*paires_de_joueurs)
        match.id = document['id']
        match.update_score(document['score_joueur_1'],
                           document['score_joueur_2'])
        return match

    def data_match_tour(self, id_tour, match):
        """
        Méthode qui génère un dictionnaire à stocker dans la
        table "liens_match_tour"
        """
        data = dict()
        data['id'] = match.id
        data['id_tour'] = id_tour
        data['id_joueur_1'] = match.paire_de_joueurs[0].id
        data['score_joueur_1'] = match.score[0]
        data['id_joueur_2'] = match.paire_de_joueurs[1].id
        data['score_joueur_2'] = match.score[1]
        return data

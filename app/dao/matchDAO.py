# -*-coding:utf-8 -*

from tinydb import TinyDB, Query
import app.models.match as mx
from app.dao.joueurDAO import JoueurDAO
from app.models.exception import MatchDAOException
from app.utils import util

class MatchDAO:

    _db = TinyDB('db.json', sort_keys=True, indent=4)
    _liens_match_tour = _db.table("liens_match_tour")

    def __init__(self):
        pass

    def create(self, id_tour, match):
        if self.match_exists(id_tour, match):
            raise MatchDAOException(f"Le match existe déjà dans la base de données : {match}")
        else:
            match.id = MatchDAO._liens_match_tour._get_next_id()
            MatchDAO._liens_match_tour.insert(util.document(self.data_match_tour(id_tour, match)))

    def read_all(self):
        return [self.generer_instance_match(**document) for document in MatchDAO._liens_match_tour.all()]

    def read(self, id):
        return self.generer_instance_match(**MatchDAO._liens_match_tour.get(doc_id=id))

    def read_by_index(self, id_tour, id_joueur_1, id_joueur_2):
        match = Query()
        table = MatchDAO._liens_match_tour
        item = table.search((match.id_tour == id_tour) & (match.id_joueur_1 == id_joueur_1) & (match.id_joueur_2 == id_joueur_2))
        if item:
            return self.generer_instance_match(**item[0])
        else:
            raise MatchDAOException(f"Le match n'existe pas dans la base de données : {id_tour} {id_joueur_1} {id_joueur_2}")

    def read_by_id_tour(self, id_tour):
        match = Query()
        table = MatchDAO._liens_match_tour
        liste_documents = table.search((match.id_tour == id_tour))
        return [self.generer_instance_match(**document) for document in liste_documents]

    def update(self, id_tour, match):
        try:
            self.read_by_index(id_tour, match.paire_de_joueurs[0].id, match.paire_de_joueurs[1].id)
        except MatchDAOException:
            self.create(id_tour, match)
        else:
            requete = Query()
            MatchDAO._liens_match_tour.update(util.document(self.data_match_tour(id_tour, match)),
                                              (requete.id == match.id) & (requete.id_tour == id_tour))

    def match_exists(self, id_tour, match):
        try:
            instance_match = self.read_by_index(id_tour, match.paire_de_joueurs[0].id, match.paire_de_joueurs[1].id)
            assert isinstance(instance_match, mx.Match)
        except MatchDAOException:
            return False
        except AssertionError:
            return False
        else:
            return True

    def generer_instance_match(self, **document):
        premier_joueur = JoueurDAO().read(document['id_joueur_1'])
        premier_joueur.nombre_de_points = 0.0
        deuxieme_joueur = JoueurDAO().read(document['id_joueur_2'])
        deuxieme_joueur.nombre_de_points = 0.0
        paires_de_joueurs = [premier_joueur, deuxieme_joueur]
        match = mx.Match(*paires_de_joueurs)
        match.update_score(document['score_joueur_1'], document['score_joueur_2'])
        return match

    def data_match_tour(self, id_tour, match):
        data = dict()
        data['id'] = match.id
        data['id_tour'] = id_tour
        data['id_joueur_1'] = match.paire_de_joueurs[0].id
        data['score_joueur_1'] = match.score[0]
        data['id_joueur_2'] = match.paire_de_joueurs[1].id
        data['score_joueur_2'] = match.score[1]
        return data
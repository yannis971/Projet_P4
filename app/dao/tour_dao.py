# -*-coding:utf-8 -*
"""
Module tour_dao décrivant la classe TourDAO
"""
from tinydb import TinyDB, Query
import app.models.tour as tx
from app.dao.match_dao import MatchDAO
from app.models.exception import TourDAOException
from app.utils import util


class TourDAO:
    """
    Classe TourDAO permettant d'accéder aux données Tour
    """
    _db = TinyDB('db.json', sort_keys=True, indent=4)
    _liens_tour_tournoi = _db.table("liens_tour_tournoi")

    def __init__(self):
        pass

    def create(self, id_tournoi, tour):
        """
        Méthode permettant de créer un tour dans la table "liens_tour_tournoi"
        """
        if self.tour_exists(id_tournoi, tour.nom):
            message = f"Le tour existe déjà dans la base de données : {tour}"
            raise TourDAOException(message)
        else:
            tour.id = TourDAO._liens_tour_tournoi._get_next_id()
            tour._id_tournoi = id_tournoi
            TourDAO._liens_tour_tournoi.insert(util.document(tour))
            for match in tour.liste_de_matchs:
                MatchDAO().create(tour.id, match)

    def read_all(self):
        """
        Méthode génératrice de la liste des tours
        """
        for document in TourDAO._liens_tour_tournoi.all():
            yield self.generer_instance_tour(**document)

    def read(self, id):
        """
        Méthode renvoyant une instance de tour à partir de son id
        """
        document = TourDAO._liens_tour_tournoi.get(doc_id=id)
        if document:
            return self.generer_instance_tour(**document)
        else:
            message = f"Tour non trouvé - id : {id}"
            raise TourDAOException(message)

    def read_by_id_tournoi(self, id_tournoi):
        """
        Méthode génératrice de la liste des tours d'un tournoi
        """
        tour = Query()
        table = TourDAO._liens_tour_tournoi
        liste_documents = table.search(tour.id_tournoi == id_tournoi)
        if liste_documents:
            for document in liste_documents:
                yield self.generer_instance_tour(**document)
        else:
            return []

    def read_by_index(self, id_tournoi, nom):
        """
        Méthode qui recherche un tour d'un tournoi à partir de son nom
        """
        tour = Query()
        table = TourDAO._liens_tour_tournoi
        item = table.search((tour.nom == nom)
                            & (tour.id_tournoi == id_tournoi))
        if item:
            return self.generer_instance_tour(**item[0])
        else:
            message = f"Tour non trouvé : {id_tournoi} {nom}"
            raise TourDAOException(message)

    def update(self, id_tournoi, tour):
        """
        Méthode qui met à jour un tour dans un tournoi
        """
        try:
            self.read_by_index(id_tournoi, tour.nom)
        except TourDAOException:
            self.create(id_tournoi, tour)
        else:
            tour._id_tournoi = id_tournoi
            document = util.document(tour)
            TourDAO._liens_tour_tournoi.update(document, doc_ids=[tour.id])
            for match in tour.liste_de_matchs:
                MatchDAO().update(tour.id, match)

    def tour_exists(self, id_tournoi, nom):
        """
        Méthode qui teste si un tour existe en base
        """
        try:
            instance_tour = self.read_by_index(id_tournoi, nom)
            assert isinstance(instance_tour, tx.Tour)
        except TourDAOException:
            return False
        except AssertionError:
            return False
        else:
            return True

    def generer_instance_tour(self, **document):
        """
        Méthode qui génère une instance de tour à partir d'un document
        """
        document.pop('id_tournoi')
        tour = tx.Tour(**document)
        tour.liste_de_matchs = MatchDAO().read_by_id_tour(tour.id)
        return tour

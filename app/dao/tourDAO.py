# -*-coding:utf-8 -*

from tinydb import TinyDB, Query
import app.models.tour as tx
from app.dao.matchDAO import MatchDAO
from app.models.exception import TourDAOException


class TourDAO:
    _db = TinyDB('db.json', sort_keys=True, indent=4)
    _liens_tour_tournoi = _db.table("liens_tour_tournoi")

    def __init__(self):
        pass

    def create(self, id_tournoi, tour):
        if self.tour_exists(id_tournoi, tour.nom):
            raise TourDAOException(f"Le tour existe déjà dans la base de données : {tour}")
        else:
            tour.id = TourDAO._liens_tour_tournoi._get_next_id()
            data_storage = dict(
                (attr[1:], value) for (attr, value) in tour.__dict__.items() if not isinstance(value, list))
            data_storage['id_tournoi'] = id_tournoi
            TourDAO._liens_tour_tournoi.insert(data_storage)
            for match in tour.liste_de_matchs:
                MatchDAO().create(tour.id, match)

    def read_all(self):
        return [self.generer_instance_tour(**document) for document in TourDAO._liens_tour_tournoi.all()]

    def read(self, id):
        return self.generer_instance_tour(**TourDAO._liens_tour_tournoi.get(doc_id=id))

    def read_by_id_tournoi(self, id_tournoi):
        tour = Query()
        table = TourDAO._liens_tour_tournoi
        liste_documents = table.search(tour.id_tournoi == id_tournoi)
        return [self.generer_instance_tour(**document) for document in liste_documents]

    def read_by_index(self, id_tournoi, nom):
        tour = Query()
        table = TourDAO._liens_tour_tournoi
        item = table.search((tour.nom == nom) & (tour.id_tournoi == id_tournoi))
        if item:
            return self.generer_instance_tour(**item[0])
        else:
            raise TourDAOException(f"Le tour n'existe pas dans la base de données : {id_tournoi} {nom}")

    def update(self, id_tournoi, tour):
        try:
            self.read_by_index(id_tournoi, tour.nom)
        except TourDAOException:
            self.create(id_tournoi, tour)
        else:
            requete = Query()
            data_storage = dict(
                (attr[1:], value) for (attr, value) in tour.__dict__.items() if not isinstance(value, list))
            data_storage['id_tournoi'] = id_tournoi
            TourDAO._liens_tour_tournoi.update(data_storage, (requete.id_tournoi == id_tournoi)
                                               & (requete.nom == tour.nom))
            for match in tour.liste_de_matchs:
                MatchDAO().update(tour.id, match)

    def tour_exists(self, id_tournoi, nom):
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
        document.pop('id_tournoi')
        tour = tx.Tour(**document)
        tour.liste_de_matchs = MatchDAO().read_by_id_tour(tour.id)
        return tour

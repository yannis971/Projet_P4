# -*-coding:utf-8 -*

from tinydb import TinyDB, Query
import app.models.tournoi as tx
from app.dao.tourDAO import TourDAO
from app.dao.joueurDAO import JoueurDAO
from app.models.exception import TournoiDAOException

class TournoiDAO:

    _db = TinyDB('db.json', sort_keys=True, indent=4)
    _table_tournois = _db.table("table_tournois")
    _liens_participant_tournoi = _db.table("liens_participant_tournoi")


    def __init__(self):
        pass

    def create(self, tournoi):
        if self.tournoi_exists(tournoi):
            raise TournoiDAOException(f"Le tournoi existe déjà dans la base de données : {tournoi}")
        else:
            print("_next_id :", TournoiDAO._table_tournois._next_id)
            tournoi.id = TournoiDAO._table_tournois._get_next_id()
            print("_next_id :", TournoiDAO._table_tournois._next_id, "tournoi.id :", tournoi.id )
            data_storage = dict((attr[1:], value) for (attr, value) in tournoi.__dict__.items()
                                #if not isinstance(value, list) and not isinstance(value, dict))
                                if not isinstance(value, list))
            TournoiDAO._table_tournois.insert(data_storage)
            #matchs_deja_joues
            #data_storage = tournoi.matchs_deja_joues
            #data_storage['id_tournoi'] = tournoi.id
            #TournoiDAO._matchs_deja_joues.insert(data_storage)
            #liens_participants_tournoi
            for joueur in tournoi.liste_de_participants:
                document = dict()
                document['id'] = joueur.id
                document['id_tournoi'] = tournoi.id
                document['nombre_de_points'] = joueur.nombre_de_points
                TournoiDAO._liens_participant_tournoi.insert(document)
            #liste des tours
            for tour in tournoi.liste_de_tours:
                TourDAO().create(tournoi.id, tour)

    def read_all(self):
        for document in TournoiDAO._table_tournois.all():
            yield self.generer_instance_tournoi(**document)


    def read(self, id):
        document = TournoiDAO._table_tournois.get(doc_id=id)
        if document:
            return self.generer_instance_tournoi(**document)
        else:
            raise TournoiDAOException(f"Le tournoi n'existe pas dans la base de données. id = {id}")

    def read_by_index(self, nom, lieu, date_de_debut):
        tournoi = Query()
        table = TournoiDAO._table_tournois
        item = table.search((tournoi.nom == nom) & (tournoi.lieu == lieu) & (tournoi.date_de_debut == date_de_debut))
        if item:
            print("tournoiDAO.read_by_index - item :", item)
            print("tournoiDAO.read_by_index - item[0] :", item[0])
            return self.generer_instance_tournoi(**item[0])
        else:
            raise TournoiDAOException(f"Le tournoi n'existe pas dans la base de données : {nom} {lieu} {date_de_debut}")

    def update(self, tournoi):
        try:
            print(f"tournoiDAO.update {tournoi.nom} {tournoi.lieu} {tournoi.date_de_debut}")
            self.read_by_index(tournoi.nom, tournoi.lieu, tournoi.date_de_debut)
        except TournoiDAOException:
            self.create(tournoi)
        else:
            requete = Query()
            data_storage = dict((attr[1:], value) for (attr, value) in tournoi.__dict__.items()
                                #if not isinstance(value, list) and not isinstance(value, dict))
                                if not isinstance(value, list))
            print("data_storage", data_storage)
            TournoiDAO._table_tournois.update(data_storage, (requete.nom == tournoi.nom)
                                              & (requete.lieu == tournoi.lieu)
                                              & (requete.date_de_debut == tournoi.date_de_debut))
            #matchs_deja_joues
            #matchs_deja_joues = Query()
            #data_storage = tournoi.matchs_deja_joues
            #data_storage['id_tournoi'] = tournoi.id
            #TournoiDAO._matchs_deja_joues.update(data_storage,(matchs_deja_joues.id_tournoi == tournoi.id))
            #liens_participants_tournoi
            for joueur in tournoi.liste_de_participants:
                requete = Query()
                document = dict()
                document['id'] = joueur.id
                document['id_tournoi'] = tournoi.id
                document['nombre_de_points'] = joueur.nombre_de_points
                TournoiDAO._liens_participant_tournoi.update(document, (requete.id == joueur.id)
                                                             & (requete.id_tournoi == tournoi.id))
            #liste des tours
            for tour in tournoi.liste_de_tours:
                TourDAO().update(tournoi.id, tour)


    def tournoi_exists(self, tournoi):
        try:
            instance_tournoi = self.read_by_index(tournoi.nom, tournoi.lieu, tournoi.date_de_debut)
            assert isinstance(instance_tournoi, tx.Tournoi)
        except TournoiDAOException:
            return False
        except AssertionError:
            return False
        else:
            tournoi.id = instance_tournoi.id
            return True

    def recuperer_participants_tournoi(self, id_tournoi):
        participant = Query()
        table = TournoiDAO._liens_participant_tournoi
        liste_de_documents = table.search(participant.id_tournoi == id_tournoi)
        liste_de_participants = list()
        for document in liste_de_documents:
            print("document['id'] = ", document['id'])
            joueur = JoueurDAO().read(document['id'])
            joueur.nombre_de_points = document['nombre_de_points']
            liste_de_participants.append(joueur)
        return liste_de_participants

    def generer_instance_tournoi(self, **document):
        print("tournoiDAO.generer_instance_tournoi", document)
        tournoi = tx.Tournoi(**document)
        tournoi._liste_de_tours = TourDAO().read_by_id_tournoi(tournoi.id)
        tournoi._liste_de_participants = self.recuperer_participants_tournoi(tournoi.id)
        return tournoi
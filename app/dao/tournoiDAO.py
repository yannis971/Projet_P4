# -*-coding:utf-8 -*

from tinydb import TinyDB, Query
import app.models.tournoi as tx
from app.dao.tourDAO import TourDAO
from app.dao.joueurDAO import JoueurDAO
from app.models.exception import TournoiDAOException
from app.utils import util

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
            tournoi.id = TournoiDAO._table_tournois._get_next_id()
            TournoiDAO._table_tournois.insert(util.document(tournoi))
            #création des liens_participant_tournoi
            for joueur in tournoi.liste_de_participants:
                data = self.data_participant_tournoi(tournoi.id, joueur)
                TournoiDAO._liens_participant_tournoi.insert(util.document(data))
            #création des tours
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
            TournoiDAO._table_tournois.update(util.document(tournoi), (requete.nom == tournoi.nom)
                                              & (requete.lieu == tournoi.lieu)
                                              & (requete.date_de_debut == tournoi.date_de_debut))
            #liens_participants_tournoi
            for joueur in tournoi.liste_de_participants:
                requete = Query()
                data = self.data_participant_tournoi(tournoi.id, joueur)
                TournoiDAO._liens_participant_tournoi.update(util.document(data), (requete.id == joueur.id)
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
            joueur = JoueurDAO().read(document['id'])
            joueur.nombre_de_points = document['nombre_de_points']
            joueur.rang = document['rang']
            liste_de_participants.append(joueur)
        return liste_de_participants

    def generer_instance_tournoi(self, **document):
        tournoi = tx.Tournoi(**document)
        tournoi._liste_de_tours = TourDAO().read_by_id_tournoi(tournoi.id)
        tournoi._liste_de_participants = self.recuperer_participants_tournoi(tournoi.id)
        return tournoi

    def data_participant_tournoi(self, id_tournoi, joueur):
        data = dict()
        data['id'] = joueur.id
        data['id_tournoi'] = id_tournoi
        data['rang'] = joueur.rang
        data['nombre_de_points'] = joueur.nombre_de_points
        return data
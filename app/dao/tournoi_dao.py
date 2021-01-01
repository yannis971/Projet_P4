# -*-coding:utf-8 -*
"""
Module tournoi_dao décrivant la classe TournoiDAO
"""
from tinydb import TinyDB, Query
import app.models.tournoi as tx
from app.dao.tour_dao import TourDAO
from app.dao.joueur_dao import JoueurDAO
from app.models.exception import TournoiDAOException
from app.utils import util


class TournoiDAO:
    """
    Classe TournoiDAO permettant d'accéder aux données Tournoi
    """
    _db = TinyDB('db.json', sort_keys=True, indent=4)
    _table_tournois = _db.table("table_tournois")
    _liens_participant_tournoi = _db.table("liens_participant_tournoi")

    def __init__(self):
        pass

    def create(self, tournoi):
        """
        Méthode permettant de créer un tournoi dans la table "table_tournois"
        """
        if self.tournoi_exists(tournoi):
            message = f"Le tournoi existe déjà en table : {tournoi}"
            raise TournoiDAOException(message)
        else:
            tournoi.id = TournoiDAO._table_tournois._get_next_id()
            TournoiDAO._table_tournois.insert(util.document(tournoi))
            for joueur in tournoi.liste_de_participants:
                data = self.data_participant_tournoi(tournoi.id, joueur)
                data['id'] = \
                    TournoiDAO._liens_participant_tournoi._get_next_id()
                document = util.document(data)
                TournoiDAO._liens_participant_tournoi.insert(document)
            for tour in tournoi.liste_de_tours:
                TourDAO().create(tournoi.id, tour)

    def read_all(self):
        """
        Méthode génératrice de la liste des tournois
        """
        for document in TournoiDAO._table_tournois.all():
            yield self.generer_instance_tournoi(**document)

    def read(self, id):
        """
        Méthode renvoyant une instance de tournoi à partir de son id
        """
        document = TournoiDAO._table_tournois.get(doc_id=id)
        if document:
            return self.generer_instance_tournoi(**document)
        else:
            message = f"Tournoi non trouvé - id : {id}"
            raise TournoiDAOException(message)

    def read_by_index(self, nom, lieu, date_de_debut):
        """
        Méthode renvoyant une instance de tournoi à partir de l'index
        constitué du nom, du lieu et de la date de début
        """
        tournoi = Query()
        table = TournoiDAO._table_tournois
        item = table.search((tournoi.nom == nom) & (tournoi.lieu == lieu)
                            & (tournoi.date_de_debut == date_de_debut))
        if item:
            return self.generer_instance_tournoi(**item[0])
        else:
            message = f"Tournoi non trouvé : {nom} {lieu} {date_de_debut}"
            raise TournoiDAOException(message)

    def update(self, tournoi):
        """
        Méthode de mise à jour d'un tournoi
        """
        try:
            self.read_by_index(tournoi.nom, tournoi.lieu,
                               tournoi.date_de_debut)
        except TournoiDAOException:
            self.create(tournoi)
        else:
            TournoiDAO._table_tournois.update(util.document(tournoi),
                                              doc_ids=[tournoi.id])
            for joueur in tournoi.liste_de_participants:
                requete = Query()
                data = self.data_participant_tournoi(tournoi.id, joueur)
                TournoiDAO._liens_participant_tournoi.upsert(
                    data, (requete.id_joueur == joueur.id)
                    & (requete.id_tournoi == tournoi.id))
            for tour in tournoi.liste_de_tours:
                TourDAO().update(tournoi.id, tour)

    def tournoi_exists(self, tournoi):
        """
        Méthode qui teste si un tournoi existe en base
        """
        try:
            instance_tournoi = self.read_by_index(tournoi.nom,
                                                  tournoi.lieu,
                                                  tournoi.date_de_debut)
            assert isinstance(instance_tournoi, tx.Tournoi)
        except TournoiDAOException:
            return False
        except AssertionError:
            return False
        else:
            tournoi.id = instance_tournoi.id
            return True

    def recuperer_participants_tournoi(self, id_tournoi):
        """
        Méthode qui récupère la liste des participants
        """
        participant = Query()
        table = TournoiDAO._liens_participant_tournoi
        liste_de_documents = table.search(participant.id_tournoi == id_tournoi)
        for document in liste_de_documents:
            joueur = JoueurDAO().read(document['id_joueur'])
            joueur.nombre_de_points = document['nombre_de_points']
            joueur.rang = document['rang']
            yield joueur

    def generer_instance_tournoi(self, **document):
        """
        Méthode permettant de générer une instance de tournoi à partir
        d'un dictionnaire ou document
        """
        tournoi = tx.Tournoi(**document)
        tournoi._liste_de_tours = TourDAO().read_by_id_tournoi(tournoi.id)
        tournoi._liste_de_participants =  \
            self.recuperer_participants_tournoi(tournoi.id)
        return tournoi

    def data_participant_tournoi(self, id_tournoi, joueur):
        """
        Méthode permetant de formater le dictionnaire à stocker dans la table
        "liens_participant_tournoi"
        """
        data = dict()
        data['id_joueur'] = joueur.id
        data['id_tournoi'] = id_tournoi
        data['rang'] = joueur.rang
        data['nombre_de_points'] = joueur.nombre_de_points
        return data

# -*-coding:utf-8 -*
"""
Module exception décrivant les différentes exception
"""


class JoueurException(Exception):
    """
    classe JoueurExeption pour lever ou intercepter une exception lors du
    traitement d'un objet de type Joueur
    """
    def __init__(self, message):
        self.message = message


class MatchException(Exception):
    """
    classe MatchExeption pour lever ou intercepter une exception lors du
    traitement d'un objet de type Match
    """
    def __init__(self, message):
        self.message = message


class TourException(Exception):
    """
    classe TourExeption pour lever ou intercepter une exception lors du
    traitement d'un objet de type Tour
    """
    def __init__(self, message):
        self.message = message


class TournoiException(Exception):
    """
    classe TournoiExeption pour lever ou intercepter une exception lors du
    traitement d'un objet de type Tournoi
    """
    def __init__(self, message):
        self.message = message


class JoueurDAOException(Exception):
    """
    classe JoueurDAOExeption pour lever ou intercepter une exception lors du
    traitement d'un objet de type Joueur dans la couche DAO
    """
    def __init__(self, message):
        self.message = message


class MatchDAOException(Exception):
    """
    classe MatchDAOExeption pour lever ou intercepter une exception lors du
    traitement d'un objet de type Match dans la couche DAO
    """
    def __init__(self, message):
        self.message = message


class TourDAOException(Exception):
    """
    classe TourDAOExeption pour lever ou intercepter une exception lors du
    traitement d'un objet de type Tour dans la couche DAO
    """
    def __init__(self, message):
        self.message = message


class TournoiDAOException(Exception):
    """
    classe TournoiDAOExeption pour lever ou intercepter une exception lors du
    traitement d'un objet de type Tournoi dans la couche DAO
    """
    def __init__(self, message):
        self.message = message

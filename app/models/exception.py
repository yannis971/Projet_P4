# -*-coding:utf-8 -*

class JoueurException(Exception):
    def __init__(self, message):
        self.message = message

class JoueurDAOException(Exception):
    def __init__(self, message):
        self.message = message

class MatchException(Exception):
    def __init__(self, message):
        self.message = message

class TourException(Exception):
    def __init__(self, message):
        self.message = message

class TournoiException(Exception):
    def __init__(self, message):
        self.message = message

class TournoiDAOException(Exception):
    def __init__(self, message):
        self.message = message

class TourDAOException(Exception):
    def __init__(self, message):
        self.message = message

class MatchDAOException(Exception):
    def __init__(self, message):
        self.message = message
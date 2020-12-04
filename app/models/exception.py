# -*-coding:utf-8 -*

class JoueurException(Exception):
    def __init__(self, message):
        self.message = message

class TournoiException(Exception):
    def __init__(self, message):
        self.message = message

# -*-coding:utf-8 -*
"""
Module match décrivant la classe Match
"""

from app.models.exception import MatchException
from app.models.joueur import Joueur


class Match:
    """
    Class describing a match between 2 chess players
    """
    __scores_autorises = [(0.0, 1.0), (0.5, 0.5), (1.0, 0.0), (0.0, 0.0)]

    def __init__(self, *paire_de_joueurs):
        self._paire_de_joueurs = [item for item in paire_de_joueurs
                                  if isinstance(item, Joueur)]
        self._score = [0.0, 0.0]
        try:
            assert len(paire_de_joueurs) == 2 and len(
                self._paire_de_joueurs) == 2
        except AssertionError:
            message = "L'argument de Match.__init__ n'est pas une liste de 2"
            message += " joueurs"
            raise MatchException(message) from AssertionError

    def __str__(self):
        chaine = f"{self._paire_de_joueurs[0].nom} - "
        chaine += f"{self._paire_de_joueurs[1].nom} : {self._score[0]} - "
        chaine += f"{self._score[1]}"
        return chaine

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int) and value >= 0:
            self._id = value
        else:
            raise MatchException(f"id du match invalide : {value}")

    @property
    def paire_de_joueurs(self):
        return self._paire_de_joueurs

    @property
    def score(self):
        return self._score

    @id.setter
    def id(self, value):
        if isinstance(value, int) and value > 0:
            self._id = value
        else:
            raise MatchException(f"id du match invalide : {value}")

    def update_score(self, score_joueur_01, score_joueur_02):
        """
        Methode permettant de mettre à jour le score du match
        """
        try:
            assert isinstance(score_joueur_01, float) \
                   and isinstance(score_joueur_02, float)
        except AssertionError:
            message = "les scores passés en paramètres : "
            message += f"{score_joueur_01}, {score_joueur_02} ne sont pas"
            message += " de type float"
            raise MatchException(message) from AssertionError
        else:
            if (score_joueur_01, score_joueur_02) in Match.__scores_autorises:
                self._score[0] = score_joueur_01
                self._paire_de_joueurs[0].nombre_de_points += score_joueur_01
                self._score[1] = score_joueur_02
                self._paire_de_joueurs[1].nombre_de_points += score_joueur_02
            else:
                message = f"le score du match est invalide : {score_joueur_01}"
                message += f",{score_joueur_02}"
                raise MatchException(message)

# -*-coding:utf-8 -*
from app.models.exception import MatchException
from app.models.joueur import Joueur

class Match:

    __scores_autorises = [(0.0, 1.0), (0.5, 0.5), (1.0, 0.0)]

    def __init__(self, *paires_de_joueurs):
        self._paires_de_joueurs = [item for item in paires_de_joueurs if isinstance(item, Joueur)]
        self._score = [0.0, 0.0]
        try:
            assert len(paires_de_joueurs) == 2 and len(self._paires_de_joueurs) == 2
        except AssertionError:
            raise MatchException(f"Impossible de créer une instance de Match avec autre chose qu'une liste de 2 Joueurs {paires_de_joueurs}")

    def __repr__(self):
        return ([self._paires_de_joueurs[0], self._score[0]],[[self._paires_de_joueurs[1], self._score[1]]])

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int) and value > 0:
            self._id = value
        else:
            raise MatchException(f"id du match invalide : {value}")

    def update_score(self, score_premier_joueur, score_deuxieme_joueur):
        try:
            assert isinstance(score_premier_joueur, float) and isinstance(score_deuxieme_joueur, float)
        except AssertionError:
            raise MatchException(f"les scores passés en paramètres doivent être de type float {score_premier_joueur}, {score_deuxieme_joueur}")
        else:
            if (score_premier_joueur, score_deuxieme_joueur) in Match.__scores_autorises:
                self._score[0] = score_premier_joueur
                self._paires_de_joueurs[0] += score_premier_joueur
                self._score[1] = score_deuxieme_joueur
                self._paires_de_joueurs[1] += score_deuxieme_joueur
            else:
                raise MatchException(f"le score du match {score_premier_joueur}, {score_deuxieme_joueur} doit faire partie des scores autorisés : {Match.__scores_autorises}")

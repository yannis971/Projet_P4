# -*-coding:utf-8 -*

from datetime import datetime
from operator import attrgetter
from app.models.exception import TournoiException
from app.models.joueur import Joueur
from app.utils import util

class JoueurInscrit(Joueur):
	def __init__(self):
		self.rang = 0
		self.nombre_de_points = 0


class Tournoi:

	__id = 0
	__list_attrs = ['_nom', '_lieu', '_date_de_debut', '_date_de_fin', 
    				'_nombre_de_tours', '_controle_du_temps', '_description']


	def __init__(self, **tournoi_properties):
		for (attr_name, attr_value) in tournoi_properties.items():
			setattr(self, attr_name, attr_value)
		self.check_attrs()
		self._liste_tours = list()
		self._liste_indices_joueurs_inscrits = list()
		self._nombre_joueurs_inscrits = 0

		if not hasattr(self, '_id'):
			Tournoi.__id += 1
			self._id = Tournoi.__id

	def __str__(self):
		return f"Tournoi : {self._id } {self._nom} {self._lieu} {self._date_de_debut} {self._date_de_fin}"

	def check_attrs(self):
		for attr in Tournoi.__list_attrs:
			if not hasattr(self, attr):
				raise TournoiException(f"objet de type Tournoi sans propriété : {attr[1:]}")

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, value):
		if isinstance(value, int) and value > 0:
			self._id = value
		else:
			raise TournoiException(f"id du tournoi invalide : {value}")

	@property
	def nom(self):
		return self._nom

	@nom.setter
	def nom(self, value):
		if isinstance(value, str) and len(value) > 1:
			self._nom = value
		else:
			raise TournoiException(f"nom du tournoi invalide : {value}")

	@property
	def lieu(self):
		return self._lieu

	@lieu.setter
	def lieu(self, value):
		if isinstance(value, str) and len(value) > 1:
			self._lieu = value
		else:
			raise TournoiException(f"lieu du tournoi invalide : {value}")

	@property
	def date_de_debut(self):
		return self._date_de_debut

	@date_de_debut.setter
	def date_de_debut(self, value):
		if isinstance(value, str) and util.is_date_valid(value):
			date_du_jour = util.encode_date(datetime.now())
			if value >= date_du_jour:
				self._date_de_debut = value
			else:
				raise TournoiException(f"date de début du tournoi {value} inférieure à la date du jour {date_du_jour}")
		else:
			raise TournoiException(f"date de début du tournoi invalide : {value}")

	@property
	def date_de_fin(self):
		return self._date_de_fin

	@date_de_fin.setter
	def date_de_fin(self, value):
		if isinstance(value, str) and util.is_date_valid(value):
			if value >= self._date_de_debut:
				self._date_de_fin = value
			else:
				raise TournoiException(f"date de fin du tournoi {value} inférieure à la date de début {self._date_de_fin}")
		else:
			raise TournoiException(f"date de début du tournoi invalide : {value}")

	@property
	def nombre_de_tours(self):
		return self._nombre_de_tours

	@nombre_de_tours.setter
	def nombre_de_tours(self, value):
		if isinstance(value, int) and value > 0:
			self._nombre_de_tours = value
		else:
			raise TournoiException(f"nombre de tours invalide : {value}")

	@property
	def controle_du_temps(self):
		return self._controle_du_temps
	
	@controle_du_temps.setter
	def controle_du_temps(self, value):
		if isinstance(value, str) and value in ("bullet", "blitz", "coup rapide"):
			self._controle_du_temps = value
		else:
			raise TournoiException(f"controle du temps invalide : {value}")

	@property
	def description(self):
		return self._description
	
	@description.setter
	def description(self, value):
		if isinstance(value, str) and len(value) > 8:
			self._description = value
		else:
			raise TournoiException(f"description invalide ou inférieure à 8 caractères : {value}")

	@property
	def nombre_joueurs_inscrits(self):
		return self._nombre_joueurs_inscrits

	def ajouter_joueur(self, indice_joueur):
		if isinstance(indice_joueur, int) and indice_joueur >=0:
			if indice_joueur in self._liste_indices_joueurs_inscrits:
				raise TournoiException(f"joueur indice {indice_joueur} déjà inscrit au tournoi")
			else:
				self._liste_indices_joueurs_inscrits.append(indice_joueur)
				self._nombre_joueurs_inscrits += 1
		else:
			raise TournoiException(f"indice_joueur invalide : {indice_joueur}")

	def create(self):
		pass

	@classmethod
	def read_all(cls):
		return []
		#return TournoiDAO().read_all()
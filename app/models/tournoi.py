# -*-coding:utf-8 -*

class Tournoi:

	__id = 0
	__list_attrs = ['_nom', '_lieu', '_date_de_debut', '_date_de_fin', 
    				'_nombre_de_tours', '_controle_du_temps', '_description']


	def __init__(self, **tournoi_properties):
		for (attr_name, attr_value) in tournoi_properties.items():
			setattr(self, attr_name, attr_value)
		self.check_attrs()
		self._liste_des_tours = list()
		self._liste_des_id_des_joueurs_inscrits = list()
		Tournoi.__id += 1
		if not hasattr(self, '_id'):
			self._id = Tournoi.__id

	def __str__(self):
		return f"Tournoi : {self._id } {self._nom} {self._lieu} {self._date_de_debut} {self._date_de_fin}"

	def check_attrs(self):
		for attr in Tournoi.__list_attrs:
			if not hasattr(self, attr):
				raise exception.TournoiException(f"objet de type Tournoi sans propriété : {attr[1:]}")

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, value):
		if isinstance(value, int) and value > 0:
			self._id = value
		else:
			raise exception.TournoiException(f"id du tournoi invalide : {value}")

"""
    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        if isinstance(value, str) and len(value) > 1:
            self._nom = value
        else:
            raise exception.TournoiException(f"nom du tournoi invalide : {value}")
"""
# -*-coding:utf-8 -*
#import sys
# on modifie le sys.path pour y inclure les dossiers
# contenant les classes à importer
#sys.path.append(".")

import os
import sys

current_path = os.path.dirname(__file__)
project_path = os.path.dirname(current_path)
print(f"project path is {project_path}")
sys.path.insert(0, project_path)
print(f"project path added to PYTHONPATH, current sys.path is now : {sys.path}")

from app.views.menu import Menu
from app.views.formulaire import JoueurForm, TournoiForm
from app.views.rapport import ListView
from app.models.joueur import Joueur
from app.models.tournoi import Tournoi
from app.models import exception


class Controller:

	__liste_de_choix = ('Créer un joueur', 'Créer un tournoi', 'Ajouter 8 joueurs',
                        'Générer des paires de joueurs', 'Entrer les résultats',
                        'Afficher la liste des joueurs',
                        'Afficher les rapports', 'Enregistrer', 'Quitter')

	def __init__(self):
		self._menu = Menu(Controller.__liste_de_choix)
		self._choix = self._menu.get_choix()
		self._liste_joueurs = Joueur.read_all()
		self._liste_tournois = Tournoi.read_all()


	def creer_joueur_handler(self):
		try:
			joueur = Joueur(**JoueurForm().creer_joueur())
			self._liste_joueurs.append(joueur)
			joueur.create()
		except exception.JoueurException as ex:
			print(ex)
			return self.creer_joueur_handler()
		except exception.JoueurDAOException as ex:
			print(ex)
			print(f"création joueur KO - {joueur}")
		else:
			print(f"création joueur OK - {joueur}")

	def afficher_liste_joueurs_handler(self):
		ListView("Liste de joueurs", self._liste_joueurs).display()

	def creer_tournoi_handler(self):
		try:
			tournoi = Tournoi(**TournoiForm().creer_tournoi())
			print(tournoi.__dict__)
		except exception.TournoiException as ex:
			print(ex)
			return self.creer_tournoi_handler()
		else:
			self._liste_tournois.append(tournoi)
			print(f"création tournoi ok - {tournoi}")



	def ajouter_n_joueurs(self):

		ListView("Liste de joueurs", self._liste_joueurs).display()
		liste_indices_joueurs_inscrits = JoueurForm().ajouter_n_joueurs(3)
		for i in liste_indices_joueurs_inscrits:
			try: 
				assert i >=0 and i < len(self._liste_joueurs)
			except AssertionError:
				print(f"au moins un indice non valide dans la liste : {liste_indices_joueurs_inscrits}")
				self._tournoi._liste_indices_joueurs_inscrits = list()
				self._tournoi._nombre_joueurs_inscrits = 0
				return self.ajouter_n_joueurs()
			else:
				self._tournoi.ajouter_joueur(i)

	__handlers = {'0': creer_joueur_handler, '1': creer_tournoi_handler, 
					'2' : ajouter_n_joueurs,
					'5': afficher_liste_joueurs_handler}


	def start(self):
		while Controller.__liste_de_choix[self._choix] != 'Quitter':
			Controller.__handlers[str(self._choix)](self)
			self._choix = self._menu.get_choix()	



if __name__ == "__main__":
	Controller().start()





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
		self._liste_joueurs = list()
		self._tournoi = None


	def creer_joueur_handler(self):
		try:
			joueur = Joueur(**JoueurForm().creer_joueur())
		except exception.JoueurException as ex:
			print(ex)
			return creer_joueur_handler()
		else:
			self._liste_joueurs.append(joueur)

	def afficher_liste_joueurs_handler(self):
		ListView("Liste de joueurs", self._liste_joueurs).display()

	def creer_tournoi_handler(self):
		try:
			tournoi = Tournoi(**TournoiForm().creer_tournoi())
		except exception.TournoiException as ex:
			print(ex)
			return creer_tournoi_handler()
		else:
			self._tournoi = tournoi


	__handlers = {'0': creer_joueur_handler, '1': creer_tournoi_handler, 
					'5': afficher_liste_joueurs_handler}


	def start(self):
		while Controller.__liste_de_choix[self._choix] != 'Quitter':
			Controller.__handlers[str(self._choix)](self)
			self._choix = self._menu.get_choix()	



if __name__ == "__main__":
	Controller().start()





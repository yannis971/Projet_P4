# -*-coding:utf-8 -*

from app.utils import util

class ListView:

	def __init__(self, title, liste_items):
		self._title = title
		self._liste_items = liste_items
		util.clear_console()

	def display(self):
		print(self._title)
		for i, item in enumerate(self._liste_items):
			print(f"indice : {i} - item : {item}")
		#input("appuyer la touche entrer  pour revenir au menu ... ")
		#util.clear_console()
# -*-coding:utf-8 -*

class ListView:
	def __init__(self, title, liste_items):
		self._title = title
		self._liste_items = liste_items
	def display(self):
		print(self._title)
		for i, item in enumerate(self._liste_items):
			print(f"indice : {i} - item : {item}")

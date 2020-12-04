# -*-coding:utf-8 -*

class ListView:
	def __init__(self, title, liste_items):
		self._title = title
		self._liste_items = liste_items
	def display(self):
		
		for item in self._liste_items:
			print(item)

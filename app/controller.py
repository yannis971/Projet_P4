# -*-coding:utf-8 -*
from app.views.menu import Menu
from app.views.formulaire import JoueurForm
from app.models.joueur import Joueur
from app.models import exception

menu = Menu()
choix = menu.get_choix()

print("choix", choix)
if choix == 0:
    while True:
        dico = JoueurForm().creer_joueur()
        try:
            joueur = Joueur(**dico)
            print(joueur)
            break
        except exception.JoueurException as ex:
            print(ex)

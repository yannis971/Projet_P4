# -*-coding:utf-8 -*
import sys
# on modifie le sys.path pour y inclure les dossiers
# contenant les classes à importer
sys.path.append(".")
from app.views.menu import Menu
from app.views.formulaire import JoueurForm
from app.models.joueur import Joueur
from app.models import exception

menu = Menu()
choix = menu.get_choix()

print("choix", choix)
if choix == 0:
    joueur = JoueurForm().creer_joueur()
    print(joueur)


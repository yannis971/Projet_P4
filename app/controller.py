# -*-coding:utf-8 -*
import view
import model
import exception
choix = view.afficher_menu()

if choix == "0":
    while True:
        dico = view.creer_joueur()
        try:
            joueur = model.Joueur(**dico)
            print(joueur)
            break
        except exception.JoueurException as ex:
            print(ex)

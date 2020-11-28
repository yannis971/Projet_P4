# -*-coding:utf-8 -*
import re

def afficher_menu():
    print("0 - Créer un joueur")
    print("1 - Créer un tournoi")
    print("2 - Ajouter 8 joueurs")
    choix = input("entrer votre choix : ")
    return choix

def creer_joueur():
    dico = dict()
    print("Création d'un nouveau joueur")
    dico['nom'] = input("nom : ")
    dico['prenom'] = input("prenom : ")
    pattern_date = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
    while True:
        date_de_naissance = input("date de naissance au format SIAA-MM-JJ ex 1998-12-31 : ").strip()
        if re.match(pattern_date, date_de_naissance):
            dico['date_de_naissance'] = date_de_naissance
            break
    dico['sexe'] = input("sexe M ou F : ").strip().upper()
    while True:
        try:
            dico['classement'] = int(input("classement (entier strictement supérieur à 0) : "))
            break
        except Exception as ex:
            print("vous devez saisir un entier")
    return dico
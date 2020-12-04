# -*-coding:utf-8 -*
from app.utils import util
from datetime import datetime

class JoueurForm:

    def __init__(self):
        pass

    def creer_joueur(self):
        dico = dict()
        dico['nom'] = self.get_chaine_alpha("nom")
        dico['prenom'] = self.get_chaine_alpha("prenom")
        dico['sexe'] = self.get_sexe()
        dico['date_de_naissance'] = self.get_date_de_naissance()
        dico['classement'] = self.get_classement()
        return dico

    def get_chaine_alpha(self, libelle):
        chaine = input(f"{libelle} : ").strip().capitalize()
        if not util.is_chaine_alpha_valide(chaine):
            print(f"{libelle} invalide : {chaine}")
            return self.get_chaine_alpha(libelle)
        else:
            return chaine

    def get_sexe(self):
        try:
            sexe = input("sexe M ou F : ").strip().upper()
            assert sexe in ('M', 'F')
        except AssertionError:
            return self.get_sexe()
        else:
            return sexe

    def get_date_de_naissance(self):
        date_de_naissance = input("date de naissance au format SIAA-MM-JJ ex 1998-12-31 : ").strip()
        try:
            assert (isinstance(date_de_naissance, str) and util.is_date_valid(date_de_naissance))
        except AssertionError:
            return self.get_date_de_naissance()
        else:
            return date_de_naissance

    def get_classement(self):
        try:
            classement = int(input("classement (entier strictement supérieur à 0) : "))
        except ValueError:
            return self.get_classement()
        else:
            return classement


class TournoiForm:

    def __init__():
        self._dico = dict()

    def creer_tournoi(self):
        self._dico['nom'] = self.get_chaine("nom") 
        self._dico['lieu'] = self.get_chaine("lieu")
        self._dico['date_de_debut'] = self.get_date_debut(self)
        self._dico['date_de_fin'] = self.get_date_de_fin(self)
        self._dico['nombre_de_tours'] = self.get_nombre_de_tours(self)
        self._dico['controle_du_temps'] = self.get_controle_du_temps(self)
        self._dico['description'] = self.get_chaine("description")
        return self._dico


    def get_chaine(self, libelle):
        chaine = input(f"{libelle} du tournoi : ").strip()
        if isinstance(chaine, str) and len(chaine) > 1:
            return chaine
        else:
            print(f"{libelle} du tournoi invalide : {chaine}")
            return self.get_chaine(libelle)

    def get_date_de_debut(self):
        date_du_jour = datetime.now()
        date_de_debut = input(f"date de début au format SIAA-MM-JJ ex {util.encode(date_du_jour)[:11]}: ").strip()
        try:
            assert util.is_date_valid(date_de_debut) and utils.decode(date_de_debut) >= date_du_jour
        except AssertionError:
            print(f"la date de debut {date_de_debut} est invalide ou < la date du jour {date_du_jour}")
            self.get_date_de_debut()
        else:
            return date_de_debut

    def get_date_de_fin(self):
        date_de_debut = util.decode(self._dico['date_de_debut']) 
        date_de_fin = input(f"date de fin au format SIAA-MM-JJ ex {util.encode(date_de_debut)[:11]}: ").strip()
        try:
            assert util.is_date_valid(date_de_fin) and utils.decode(date_de_fin) >= date_de_debut
        except AssertionError:
            print(f"la date de fin {date_de_fin} est invalide ou < la date de debut {date_de_debut}")
            self.get_date_de_fin()
        else:
            return date_de_fin

    def controle_du_temps(self):
        return "bullet"


        

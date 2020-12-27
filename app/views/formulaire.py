# -*-coding:utf-8 -*
from app.utils import util
from datetime import datetime

class BaseForm:

    def __init__(self):
        pass

    def get_chaine_alpha(self, libelle):
        chaine = input(f"{libelle} : ").strip().capitalize()
        if not util.is_chaine_alpha_valide(chaine):
            print(f"{libelle} invalide : {chaine}")
            return self.get_chaine_alpha(libelle)
        else:
            return chaine

    def get_chaine(self, libelle):
        chaine = input(f"{libelle} : ").strip()
        if isinstance(chaine, str) and len(chaine) > 1:
            return chaine
        else:
            print(f"{libelle} invalide : {chaine}")
            return self.get_chaine(libelle)


    def get_date(self, libelle, date_min):
        valeur_par_defaut = util.encode_date(date_min)
        date_input = input(f"{libelle} au format SIAA-MM-JJ (par défaut {valeur_par_defaut} si aucune valeur saisie) :").strip()
        if date_input == "":
            date_input = valeur_par_defaut
        try:
            assert util.is_date_valid(date_input) and date_input >= util.encode_date(date_min)
        except AssertionError:
            print(f"la {libelle} : {date_input} est invalide ou strictement inférieure à {date_min}")
            return self.get_date(libelle, date_min)
        else:
            return date_input

class JoueurForm(BaseForm):

    def __init__(self):
        pass

    def creer_joueur(self):
        util.clear_console()
        dico = dict()
        dico['nom'] = self.get_chaine_alpha("nom")
        dico['prenom'] = self.get_chaine_alpha("prenom")
        dico['sexe'] = self.get_sexe()
        dico['date_de_naissance'] = self.get_date_de_naissance()
        dico['classement'] = self.get_classement()
        return dico

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

    def ajouter_n_joueurs(self, number=8):
        try:
            liste_saisie = input(f"saisir {number} indices de joueurs distincts en les séparant d'un espace : ").strip()
            liste_saisie = set(liste_saisie.split())
            assert len(liste_saisie) == number
            liste_indices = [int(indice) for indice in liste_saisie if int(indice) >= 0]   
            assert len(liste_indices) == number         
        except AssertionError:
            print(f"il faut saisir {number} indices disctincts parmi les indices proposés")
            return self.ajouter_n_joueurs(number)
        except ValueError:
            print("au moins une valeur non numérique saisie")
            return self.ajouter_n_joueurs(number)
        else:
            return liste_indices

    def recuperer_methode_acces(self):
        print("comment souhaitez vous rechercher le joueur ?")
        print("0 - par son id ?\n1 - par l'index constitué de ses nom, prénom et date de naissance ?")
        try:
            choix = input("votre choix : ").strip()
            assert isinstance(choix, str) and choix in ["0", "1"]
        except AssertionError:
            return self.recuperer_methode_acces()
        else:
            return "id" if choix == "0" else "index"

    def recuperer_identifiants_joueur(self):
        identifiants_joueur = dict()
        print("Entrer les identifiants du joueur")
        identifiants_joueur['nom'] = self.get_chaine_alpha("nom")
        identifiants_joueur['prenom'] = self.get_chaine_alpha("prenom")
        identifiants_joueur['date_de_naissance'] = self.get_date_de_naissance()
        return identifiants_joueur

    def recuperer_id_joueur(self):
        try:
            id = int(input("Entrer l'id du joueur (entier strictement supérieur à 0) : "))
            assert id > 0
        except ValueError:
            return self.recuperer_id_joueur()
        except AssertionError:
            return self.recuperer_id_joueur()
        else:
            return id

class TournoiForm(BaseForm):

    def __init__(self):
        self._dico = dict()

    def creer_tournoi(self):
        util.clear_console()
        print("Formulaire de création de tournoi")
        self._dico['nom'] = self.get_chaine("nom") 
        self._dico['lieu'] = self.get_chaine("lieu")
        self._dico['date_de_debut'] = self.get_date("date de début", datetime.now())        
        self._dico['date_de_fin'] = self.get_date("date de fin", util.decode_date(self._dico['date_de_debut']))
        self._dico['nombre_de_tours'] = self.get_nombre_de_tours(valeur_par_defaut=4)
        self._dico['controle_du_temps'] = self.get_controle_du_temps()
        self._dico['description'] = self.get_chaine("description")
        return self._dico

    def get_nombre_de_tours(self, valeur_par_defaut):
        nombre_de_tours = input(f"nombre de tours (par défaut {valeur_par_defaut} si aucune valeur saisie) :")
        nombre_de_tours = nombre_de_tours.strip()
        if nombre_de_tours == "":
            nombre_de_tours = valeur_par_defaut
            print(f"le nombre de tours est égal à {nombre_de_tours}.")
        try:
            nombre_de_tours = int(nombre_de_tours)
        except ValueError as ex:
            print(ex)
            return self.get_nombre_de_tours(valeur_par_defaut)
        else:
            return nombre_de_tours

    def get_controle_du_temps(self):
        liste_controle_du_temps = ['bullet', 'blitz', 'coup rapide']
        print("Définir le contrôle du temps")
        for i, libelle in enumerate(liste_controle_du_temps):
            print(f"saisir {i} pour {libelle}")
        choix = input("votre choix : ").strip()
        try:
            choix = int(choix)
            assert choix >= 0 and choix < len(liste_controle_du_temps)
        except ValueError:
            print(f"saisir un entier entre 0 et {len(liste_controle_du_temps)-1}")
            return self.get_controle_du_temps()
        except AssertionError:
            print(f"choix non valide")
            return self.get_controle_du_temps()
        else:
            return liste_controle_du_temps[choix]

    def recuperer_methode_acces(self):
        print("comment souhaitez vous rechercher le tournoi ?")
        print("0 - par son id ?\n1 - par l'index constitué de ses nom, lieu et date de début ?")
        try:
            choix = input("votre choix : ").strip()
            assert isinstance(choix, str) and choix in ["0", "1"]
        except AssertionError:
            return self.recuperer_methode_acces()
        else:
            return "id" if choix == "0" else "index"

    def recuperer_identifiants_tournoi(self):
        identifiants_tournoi = dict()
        print("Entrer les identifiants du tournoi")
        identifiants_tournoi['nom'] = self.get_chaine("nom")
        identifiants_tournoi['lieu'] = self.get_chaine("lieu")
        date_min = util.decode_date("1970-01-01")
        identifiants_tournoi['date_de_debut'] = self.get_date("date de début", date_min)
        return identifiants_tournoi

    def recuperer_id_tournoi(self):
        try:
            id = int(input("Entrer l'id du tournoi (entier strictement supérieur à 0) : "))
            assert id > 0
        except ValueError:
            return self.recuperer_id_tournoi()
        except AssertionError:
            return self.recuperer_id_tournoi()
        else:
            return id



class MatchForm:

    def __init__(self, match):
        self._match = match

    def mettre_a_jour_score(self):
        print(self._match)
        try:
            score_1, score_2 = input("entrer le nouveau score ex 0.5 0.5 ou 1 0 ou 1.0 0.0 : ").strip().split()
            score_1 = float(score_1)
            score_2 = float(score_2)
        except ValueError:
            print("saisir 2 réels séparés d'un espace")
            return self.mettre_a_jour_score()
        else:
            return score_1, score_2

class TourForm:

    def __init__(self):
        pass

    def iscompleted(self):
        try:
            validation = input("vous validez la mise à jour des scores et terminer ce tour O(oui) ou N(non) ? : ").strip().upper()
            assert isinstance(validation, str) and validation in ['O', 'N']
        except AssertionError:
            print("AssertionError", validation, type(validation), len(validation))
            return self.iscompleted()
        else:
            print("return validation", validation)
            return True if validation == "O" else False

class RapportForm(BaseForm):

    def __init__(self):
        pass

    def recuperer_criteres_de_tri(self):
        print("vous souhaitez trier la liste :")
        print("0 - par ordre alphabétique")
        print("1 - par classement")
        try:
            choix = input("votre choix : 0 ou 1 ? ").strip()
            assert isinstance(choix, str) and choix in ['0', '1']
        except AssertionError:
            return self.recuperer_criteres_de_tri()
        criteres_de_tri = list()
        if choix == '0':
            criteres_de_tri.extend(['nom', 'prenom'])
        else:
            criteres_de_tri.append('classement')
        return criteres_de_tri

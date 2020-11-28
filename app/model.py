# -*-coding:utf-8 -*

from datetime import datetime, timedelta
import exception
import util


class Joueur:
    def __init__(self, nom, prenom, date_de_naissance, sexe, classement):
        if isinstance(nom, str):
            self.__nom = nom
        else:
            raise exception.JoueurException(f"nom du joueur invalide : {nom}")
        if isinstance(prenom, str):
            self.__prenom = prenom
        else:
            raise exception.JoueurException(f"prenom du joueur invalide : {prenom}")
        if isinstance(sexe, str) and sexe.strip().upper() in ['F', 'M']:
            self.__sexe = sexe
        else:
            raise exception.JoueurException(f"sexe du joueur invalide : {sexe}")
        self.__set_date_de_naissance(date_de_naissance)
        self.__set_classement(classement)

    def __str__(self):
        return f"Joueur : {self.__nom} {self.__prenom} {self.__date_de_naissance} {self.__sexe} {self.__classement}"

    @property
    def nom(self):
        return self.__nom

    @property
    def prenom(self):
        return self.__prenom

    @property
    def sexe(self):
        return self.__sexe

    def __get_date_de_naissance(self):
        return self.__date_de_naissance

    def __set_date_de_naissance(self, date_de_naissance):
        if isinstance(date_de_naissance, str) and util.is_date_valid(date_de_naissance):
            date_moins_6_ans = datetime.now() - timedelta(days=2191, hours=12)
            print(date_moins_6_ans)
            if util.decode_date(date_de_naissance) < date_moins_6_ans:
                self.__date_de_naissance = date_de_naissance
            else:
                raise exception.JoueurException(f"le joueur a moins de 6 ans : {date_de_naissance}")
        else:
            raise exception.JoueurException(f"date de naissance invalide : {date_de_naissance}")

    date_de_naissance = property(__get_date_de_naissance)

    def __get_classement(self):
        return self.__classement

    def __set_classement(self, classement):
        if isinstance(classement, int) and classement > 0:
            self.__classement = classement
        else:
            raise exception.JoueurException(f"classement du joueur invalide : {classement}")

    classement = property(__get_classement, __set_classement)


if __name__ == "__main__":
    #running controller function
    a = Joueur("saliniere", "yannis", "1977-05-03", "M", 1)
    print(a)
    print(a.nom)
    print(a.date_de_naissance)
    a.classement = 2
    print(a)

    b = Joueur(classement=3, prenom="jason", nom="statham", date_de_naissance="1977-05-03", sexe="M")
    print(b)
    dico = {'classement': 4, 'prenom': "jean", 'nom': "dico", 'date_de_naissance': "1977-05-03", 'sexe': "M"}
    c = Joueur(**dico)
    print(c)
    c.date_de_naissance = "1977-05-03"

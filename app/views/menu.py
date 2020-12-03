# -*-coding:utf-8 -*

class Menu:

    __liste_de_choix = ('Créer un joueur', 'Créer un tournoi', 'Ajouter 8 joueurs',
                        'Générer des paires de joueurs', 'Entrer les résultats',
                        'Afficher les rapports', 'Enregistrer', 'Quitter')

    def __init__(self):
        self._choix = -1


    def get_choix(self):
        for (i, libelle_choix) in enumerate(Menu.__liste_de_choix):
            print(f"{i} - {libelle_choix}")
        try:
            self._choix = int(input(f"entrer votre choix de 0 à {len(Menu.__liste_de_choix)-1}: "))
            assert self._choix >= 0 and self._choix < len(Menu.__liste_de_choix)
        except ValueError:
            return self.get_choix()
        except AssertionError:
            return self.get_choix()
        else:
            return self._choix

if __name__ == "__main__":
    m = Menu()
    print("mon choix est", m.get_choix())
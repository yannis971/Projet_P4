# -*-coding:utf-8 -*

import argparse
import os
import sys

from app.controllers.controller_joueur import ControllerJoueur
from app.controllers.controller_tournoi import ControllerTournoi
from app.controllers.controller_rapport import ControllerRapport


def configure():
    current_path = os.path.dirname(__file__)
    project_path = os.path.dirname(current_path)
    sys.path.insert(0, project_path)


def parse_arguments():
    message = """nom du programme à lancer : joueur ou tournoi ou rapport"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--program", help=message)
    return parser.parse_args()


def help():
    print("\nLogiciel Projet P4 du parcours DA Python")
    print("\nFonctionnalités du programme :")
    print("\t - gérer des tournois d'échecs")
    print("\t - gérer des joueurs")
    print("\t - générer différents rapports relatifs aux tournois")
    print("\nAuteur : Yannis Saliniere")
    print("\nLicense : GNU GPL V3")
    print("\nusage: main.py [-h] [-p PROGRAM]\n")
    print("  -h, --help \t\t show this help message and exit")
    print("  -p PROGRAM, --program PROGRAM")
    print("\t\t\t nom du programme à lancer : joueur ou tournoi ou rapport")


def main():
    configure()
    args = parse_arguments()
    if args.program == "joueur":
        ControllerJoueur().start()
    elif args.program == "tournoi":
        ControllerTournoi().start()
    elif args.program == "rapport":
        ControllerRapport().start()
    else:
        help()


if __name__ == "__main__":
    main()

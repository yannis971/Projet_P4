# -*-coding:utf-8 -*

import argparse
import os
import sys

from app.controllers.controllerJoueur import ControllerJoueur
from app.controllers.controllerTournoi import ControllerTournoi
from app.controllers.controllerRapport import ControllerRapport

def configure():
    current_path = os.path.dirname(__file__)
    project_path = os.path.dirname(current_path)
    sys.path.insert(0, project_path)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--program",
                        help="""nom du programme à lancer : joueur ou tournoi ou rapport ?""")
    return parser.parse_args()

def help():
    print("Aide du programme")

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


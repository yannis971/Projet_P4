# -*-coding:utf-8 -*

import argparse
import os
import sys

from app.controllers.controllerJoueur import ControllerJoueur
from app.controllers.controllerTournoi import ControllerTournoi

def configure():
    current_path = os.path.dirname(__file__)
    project_path = os.path.dirname(current_path)
    #print(f"project path is {project_path}")
    sys.path.insert(0, project_path)
    #print(f"project path added to PYTHONPATH, current sys.path is now : {sys.path}")
    #input("main... touch enter")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--program",
                        help="""nom du programme à lancer : joueur ou tournoi ou rapport ?""")
    return parser.parse_args()

def main():
    configure()
    args = parse_arguments()
    if args.program == "joueur":
        ControllerJoueur().start()
    elif args.program == "tournoi":
        ControllerTournoi().start()
    else:
        print("hello")

if __name__ == "__main__":
    main()


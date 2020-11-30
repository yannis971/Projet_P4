# -*-coding:utf-8 -*
import os
import sys

current_path = os.path.dirname(__file__)
project_path = os.path.dirname(current_path)
print(f"project path is {project_path}")
sys.path.insert(0, project_path)
print(f"project path added to PYTHONPATH, current sys.path is now : {sys.path}")

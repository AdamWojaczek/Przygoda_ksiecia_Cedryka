import os, sys

def get_resource_path(relative_path):
    path = ""
    if hasattr(sys, "_MEIPASS"):                                # uruchomione jako plik .exe
        path = os.path.join(sys._MEIPASS, relative_path)
    else:                                                       # uruchomione jako plik .py
        path = os.path.join(os.path.abspath("."), relative_path)
    return path

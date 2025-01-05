from tkinter import ttk, PhotoImage, messagebox, Toplevel
import tkinter as tk

from datetime import datetime 
import csv 

import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

debug = 0
if debug == 1 : print("----------------DEBUG MODE ACTIVATED-----------------")

#Tkinter main component
root = tk.Tk()             
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

import tkinter as tk
from tkinter import ttk

def afficher_page_statistics(frame_contenu, bouton_actif):
    # Nettoyer le contenu existant
    for widget in frame_contenu.winfo_children():
        widget.destroy()


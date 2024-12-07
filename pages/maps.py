import tkinter as tk
from tkintermapview import TkinterMapView

def afficher_page_maps(frame_contenu, bouton):
    # Nettoyer le contenu existant
    for widget in frame_contenu.winfo_children():
        widget.destroy()
    
    # Création d'un widget de carte
    map_widget = TkinterMapView(frame_contenu, width=800, height=600, corner_radius=0)
    map_widget.pack(fill=tk.BOTH, expand=True)
    
    # Centrer la carte sur le Maroc avec un zoom adapté
    map_widget.set_position(31.7917, -7.0926)  # Coordonnées approximatives du centre du Maroc
    map_widget.set_zoom(6)  

    # Ajouter des marqueurs pour les principales villes du Maroc
    villes = [
        {"nom": "Rabat", "coord": (34.020882, -6.841650)},
        {"nom": "Casablanca", "coord": (33.573110, -7.589843)},
        {"nom": "Marrakech", "coord": (31.629472, -7.981084)},
        {"nom": "Fès", "coord": (34.033126, -5.000548)},
       
    ]

    for ville in villes:
        map_widget.set_marker(ville["coord"][0], ville["coord"][1], text=ville["nom"])

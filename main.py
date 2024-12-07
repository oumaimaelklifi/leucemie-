
import tkinter as tk
from utils import set_window_icon
from pages.home import afficher_page_accueil
from pages.maps import afficher_page_maps
from pages.statistics import afficher_page_statistics
from pages.contact import afficher_page_contact

# Fonction pour mettre en évidence le bouton actif
def mettre_en_evidence_bouton(bouton_actif):
    style_defaut = {"bg": "#8B0000", "fg": "white"}
    style_actif = {"bg": "white", "fg": "#8B0000"}
    
    for bouton in boutons:
        bouton.config(**style_defaut)
    
    bouton_actif.config(**style_actif)

# Fonction générique pour changer de page et mettre en évidence le bouton
def changer_de_page(frame_contenu, bouton, afficher_page):
    afficher_page(frame_contenu, bouton)  
    mettre_en_evidence_bouton(bouton)

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Leucémie")
set_window_icon(root)

# Frame pour le logo
frame_logo = tk.Frame(root, bg="#8B0000", height=100)
frame_logo.pack(fill=tk.X)
label_logo = tk.Label(frame_logo, text="Leucémie au Maroc", font=("Roboto", 24, "bold"), fg="white", bg="#8B0000")
label_logo.pack(pady=20)

# Navigation
frame_nav = tk.Frame(root, bg="#8B0000", height=50)
frame_nav.pack(fill=tk.X)
frame_nav_buttons = tk.Frame(frame_nav, bg="#8B0000")
frame_nav_buttons.pack()

frame_contenu = tk.Frame(root)
frame_contenu.pack(fill=tk.BOTH, expand=True)

boutons = []

button_accueil = tk.Button(frame_nav_buttons, text="Accueil", font=("Roboto", 15), width=15, bd=0,
                           command=lambda: changer_de_page(frame_contenu, button_accueil, afficher_page_accueil))
button_accueil.pack(side=tk.LEFT, padx=15)
boutons.append(button_accueil)

button_maps = tk.Button(frame_nav_buttons, text="Maps", font=("Roboto", 15), width=15, bd=0,
                        command=lambda: changer_de_page(frame_contenu, button_maps, afficher_page_maps))
button_maps.pack(side=tk.LEFT, padx=15)
boutons.append(button_maps)

button_statistics = tk.Button(frame_nav_buttons, text="Statistique", font=("Roboto", 15), width=15, bd=0,
                              command=lambda: changer_de_page(frame_contenu, button_statistics, afficher_page_statistics))
button_statistics.pack(side=tk.LEFT, padx=15)
boutons.append(button_statistics)

button_contact = tk.Button(frame_nav_buttons, text="Contact", font=("Roboto", 15), width=15, bd=0,
                           command=lambda: changer_de_page(frame_contenu, button_contact, afficher_page_contact))
button_contact.pack(side=tk.LEFT, padx=15)
boutons.append(button_contact)

# Footer
footer_frame = tk.Frame(root, bg="#2c2c2c", height=40)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
footer_label = tk.Label(footer_frame, text="Copyright © 2025 | Géoinformation | Tous droits réservés",
                        font=("Roboto", 12, "bold"), fg="white", bg="#2c2c2c")
footer_label.pack(pady=10)

# Page d'accueil par défaut
changer_de_page(frame_contenu, button_accueil, afficher_page_accueil)
root.mainloop()


import tkinter as tk

def afficher_page_statistics(frame_contenu, bouton_actif):
        # Nettoyer le contenu existant
    for widget in frame_contenu.winfo_children():
        widget.destroy()
    
    label = tk.Label(frame_contenu,
                     text="Statistiques sur la leucémie au Maroc.",
                     font=("Montserrat", 16),
                     fg="#333")
    label.pack(padx=20, pady=20)

import tkinter as tk
from tkinter import PhotoImage

def afficher_page_accueil(frame_contenu, bouton):
    # Nettoyer le contenu existant
    for widget in frame_contenu.winfo_children():
        widget.destroy()

    content_frame = tk.Frame(frame_contenu)
    content_frame.pack(padx=20, pady=20, fill=tk.X)

    # Texte d'introduction
    label_texte = tk.Label(content_frame,
                           text="La leucémie est un type de cancer qui affecte le sang et la moelle osseuse, où sont produits les cellules sanguines. "
                                "Elle se caractérise par une production anormale et incontrôlée de globules blancs immatures ou anormaux, appelés blastes. "
                                "Ces cellules anormales empêchent les cellules sanguines normales de fonctionner correctement....\n",
                                
       
                           font=("Poppins", 14),
                           fg="#333",
                           anchor="w",
                           justify="center",
                           wraplength=600)
    label_texte.pack(side=tk.LEFT, padx=40, pady=20)

    # Affichage de l'image
    try:
        img = PhotoImage(file="assets/1.png")
        label_image = tk.Label(content_frame, image=img)
        label_image.image = img  # Conserver la référence à l'image
        label_image.pack(side=tk.LEFT, padx=30)
    except Exception as e:
        label_image = tk.Label(content_frame, text="Image non trouvée.", font=("Montserrat", 14), fg="red")
        label_image.pack(side=tk.LEFT, padx=40)

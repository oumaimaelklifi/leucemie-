import folium
import webview
import tkinter as tk
from tkinter import Label
import os  # Pour gérer les chemins de fichiers

def afficher_page_maps(frame_contenu, bouton):
    # Nettoyer le contenu existant dans frame_contenu
    for widget in frame_contenu.winfo_children():
        widget.destroy()

    # Dictionnaire avec les villes et leurs coordonnées (latitude, longitude) et facteur de risque
    cities = {
        "Casablanca": {"coordinates": [33.5736, -7.5898], "risk_factor": "Élevé"},
        "Marrakech": {"coordinates": [31.6295, -8.0037], "risk_factor": "Moyenne"},
        "Rabat": {"coordinates": [34.020882, -6.84165], "risk_factor": "Faible"},
        "Fès": {"coordinates": [34.0331, -5.0007], "risk_factor": "Moyenne"},
        "Agadir": {"coordinates": [30.4202, -9.5982], "risk_factor": "Faible"}
    }

    # Dictionnaire de couleurs pour chaque facteur de risque
    risk_colors = {
        "Élevé": "red",
        "Moyenne": "orange",
        "Faible": "green"
    }

    # Dictionnaire pour les tailles de rayon
    risk_radius = {
        "Élevé": 25,   # Plus grand rayon
        "Moyenne": 15,  # Rayon moyen
        "Faible": 10    # Plus petit rayon
    }

    # Créer la carte centrée sur le Maroc
    m = folium.Map(location=[31.7917, -7.0926], zoom_start=6)

    # Ajouter chaque ville sur la carte avec un pop-up dynamique pour le facteur de risque
    for city, data in cities.items():
        # Définir la couleur et le rayon en fonction du facteur de risque
        risk_color = risk_colors.get(data["risk_factor"], "gray")
        risk_circle_radius = risk_radius.get(data["risk_factor"], 6)

        # Ajouter un marqueur pour chaque ville
        folium.Marker(
            location=data["coordinates"],
            popup=f"{city}: Facteur de risque = {data['risk_factor']}",
            tooltip=city
        ).add_to(m)

        # Ajouter un cercle coloré pour indiquer le facteur de risque
        folium.CircleMarker(
            location=data["coordinates"],
            radius=risk_circle_radius,
            color=risk_color,
            fill=True,
            fill_color=risk_color,
            fill_opacity=0.5
        ).add_to(m)

    # Ajouter une clé explicative directement sur la carte
    key_html = """
    <div style="
        position: fixed; 
       
        margin-top:210px;
        margin-left:100px;

        width: 250px;
        font-weight:700;
        height: 230px; 
        background-color:#8B0000; 
        border: 2px solid #8B0000; 
        z-index: 999; 
        padding: 10px;
        color:white;
        font-size: 17px;
      
    ">
        <b style="display: block; text-align: center;">Clé de la carte :</b><br>
        <span style="color: red;">• Rouge :</span> Risque élevé<br>
        <span style="color: orange;">• Orange :</span> Risque moyen<br>
        <span style="color: green;">• Vert :</span> Risque faible<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(key_html))

    # Définir un chemin absolu pour le fichier HTML
    output_file = os.path.join(os.getcwd(), "carte_interactive_villes_maroc.html")

    # Sauvegarder la carte dans le fichier HTML
    m.save(output_file)

    # Vérifier si le fichier a été créé
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"Le fichier HTML '{output_file}' n'a pas été créé.")

    # Intégrer la carte dans un webview à l'intérieur de Tkinter
    webview.create_window('Maroc', output_file)
    webview.start()


import sys
import folium
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import json


class PageMaps(QWidget):
    def __init__(self, parent=None):
        super(PageMaps, self).__init__(parent)

        # Créer une carte centrée sur le Maroc
        self.carte_maroc = folium.Map(location=[31.7917, -7.0926], zoom_start=6)

        # Ajouter des villes avec des fiches d'information détaillées
        villes = [
            {
                "nom": "Rabat",
                "coord": [34.020882, -6.84165],
                "info": """
                <strong>Rabat</strong><br>
                Nombre des patients : 1000<br>
                Femmes : 42.3%<br>
                Hommes : 57.7%<br>
                Tabagisme : 13.2%
                """
            },
            {
                "nom": "Casablanca",
                "coord": [33.5731, -7.5898],
                "info": """
                <strong>Casablanca</strong><br>
                Nombre des patients : 1000<br> 
                Femmes : 43.4%<br>
                Hommes : 56.6%<br>
                Types de leucémie : Myéloide : 58.4%<br>
                                   Lymphoide : 39.4%<br>
                                   Non spécifiée : 2.2%<br>
                Environnement : Urbain : 91.6%, Rural : 8.4%<br>
                Obésité : 30%<br>
                Tabagisme (Fumeurs actifs) :<br>
                Pour Femmes : Entre 26.9% et 35.9%<br>
                Pour Hommes : Entre 0.4% et 2.2%
                """
            },
            {
                "nom": "Fès",
                "coord": [34.0331, -5.0003],
                "info": """
                <strong>Fès</strong><br>
                Nombre des patients : 1000<br> 
                Femmes : 51%<br>
                Hommes : 49%<br>
                Profession : <br>
                Sans profession : 54.71%<br>
                Agriculteur : 3.77%<br>
                Ouvrier : 20.75%<br>
                Etudiants : 5.7%<br>
                Profession libérale : 15.09%
                """
            },
            {
                "nom": "Sous-Massa",
                "coord": [30.0000, -8.5000],
                "info": """
                <strong>Sous-Massa</strong><br>
                Nombre des patients : 1000<br>
                Année : Nombre des cas , Fréquence <br> 
                2014 : 139 , 13%<br>
                2015 : 125 , 14%<br>
                2016 : 148 , 13%<br>
                2017 : 142 , 14%<br>
                2018 : 268 , 27%<br>
                2019 : 178 , 19%<br>
                Femmes : 52%<br>
                Hommes : 48%<br>
                Situation de famille : Marié : 73.8%, Autre(Célibataire, Divorcé et Veuf) : 26.2%<br>
                Environnement : Urbain : 54%, Rural : 46%
                """
            },
            {
                "nom": "Agadir-Ida-Outanane",
                "coord": [30.4167, -9.58333],
                "info": """
                <strong>Agadir-Ida-Outanane</strong><br>
                Nombre des patients : 246 
                Fréquence : 23,8%<br> 
                """
            },
            {
                "nom": "Inezgane-ait-Melloul",
                "coord": [30.3523, -9.5514],
                "info": """
                <strong>Inezgane-ait-Melloul</strong><br>
                Nombre des patients : 181 
                Fréquence : 17,5%<br> 
                """
            },
            {
                "nom": "Chtouka-Ait-Baha",
                "coord": [30.0688, -9.1525],
                "info": """
                <strong>Chtouka-Ait-Baha</strong><br>
                Nombre des patients : 102 
                Fréquence : 11,1%<br> 
                """
            },
            {
                "nom": "Taroudannt",
                "coord": [30.4727, -8.8748],
                "info": """
                <strong>Taroudannt</strong><br>
                Nombre des patients : 183 
                Fréquence : 18,1%<br> 
                """
            },
            {
                "nom": "Tiznit",
                "coord": [29.6969, -9.7331],
                "info": """
                <strong>Tiznit</strong><br>
                Nombre des patients : 47 
                Fréquence : 5,4%<br> 
                """
            },
            {
                "nom": "Tata",
                "coord": [29.7428, -7.9725],
                "info": """
                <strong>Tata</strong><br>
                Nombre des patients : 20 
                Fréquence : 2,1%<br> 
             
                """
            }
        ]

        # Ajouter les marqueurs avec des fiches d'information
        for ville in villes:
            folium.Marker(
                ville["coord"],
                popup=folium.Popup(ville["info"], max_width=300),
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(self.carte_maroc)

        # Lire et ajouter le fichier GeoJSON des frontières du Maroc
        geojson_path = "maroc.geojson"
        if os.path.exists(geojson_path):
            with open(geojson_path, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)

            # Liste des régions à colorier en rouge
            regions_rouges = ["Casablanca-Settat","Rabat-Sale-Kenitra", "Souss Massa","Fes-Meknes"]
            
            # Appliquer le style conditionnel
            def style_function(feature):
                nom_region =feature['properties'].get('region', '')   # Vérifiez si 'NOM' est la bonne clé
                if nom_region in regions_rouges:
                    return {"color": "red", "weight": 2, "fillOpacity": 0.5}
                else:
                    return {"color": "white", "weight": 1, "fillOpacity": 0.1}

            folium.GeoJson(
                geojson_data,
                name="Frontières du Maroc",
                style_function=style_function
            ).add_to(self.carte_maroc)
        else:
            print(f"Erreur : Le fichier GeoJSON '{geojson_path}' est introuvable.")
            sys.exit()

        # Ajouter un contrôle des couches
        folium.LayerControl().add_to(self.carte_maroc)

        # Enregistrer la carte dans un fichier HTML
        map_html_path = os.path.abspath("carte_maroc.html")
        self.carte_maroc.save(map_html_path)

        # Afficher la carte dans un QWebEngineView
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl.fromLocalFile(map_html_path))

        # Organiser la disposition dans la fenêtre PyQt
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        self.setLayout(layout)

        print(f"Carte interactive du Maroc créée : ouvre '{map_html_path}' dans ton navigateur.")


# Code pour lancer l'application PyQt5
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PageMaps()
    window.show()
    sys.exit(app.exec_())

import sys
import folium
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Exemple de données de risque
data_risk = {
    "Laayoune-Saguia Hamra": {"risk": "Bas", "percentage": "5%", "factors": "Faible densité, sécurité renforcée"},
    "Casablanca-Settat": {"risk": "Élevé", "percentage": "40%", "factors": "Forte urbanisation, densité élevée"},
    "Fès-Meknès": {"risk": "Élevé", "percentage": "30%", "factors": "Zone industrielle, pollution"},
    "Rabat-Salé-Kénitra": {"risk": "Bas", "percentage": "10%", "factors": "Bonne gestion des ressources"},
}

# Classe de la page Maps
class PageMaps(QWidget):
    def __init__(self, parent=None):
        super(PageMaps, self).__init__(parent)

        # Créer une carte centrée sur le Maroc
        self.map = folium.Map(location=[31.7917, -7.0926], zoom_start=6)

        # Chemin vers le fichier GeoJSON
        geojson_path = r'C:\Users\HP\Desktop\tkinter\maroc.geojson'

        if not os.path.exists(geojson_path):
            print(f"Erreur : le fichier GeoJSON '{geojson_path}' est introuvable.")
            return

        # Fonction pour récupérer les informations de risque et personnaliser le style
        def style_function(feature):
            region_name = feature['properties'].get('region', 'Inconnu')
            risk_info = data_risk.get(region_name, {"risk": "Inconnu", "percentage": "0%"})
            risk = risk_info['risk']
            color = {
                "Bas": "#00ff00",      # Vert pour faible risque
                "Modéré": "#ffff00",   # Jaune pour risque modéré
                "Élevé": "#ff0000"     # Rouge pour risque élevé
            }.get(risk, "#d3d3d3")    # Gris par défaut
            return {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.5
            }

        # Fonction pour créer des tooltips détaillés avec les facteurs de risque
        def create_tooltip(feature):
            region_name = feature['properties'].get('region', 'Inconnu')
            risk_info = data_risk.get(region_name, {"risk": "Inconnu", "percentage": "0%", "factors": "Non spécifié"})
            tooltip_content = f"""
            <div style='font-family: Arial; font-size: 12px;'>
                <strong>Région :</strong> {region_name}<br>
                <strong>Niveau de risque :</strong> {risk_info['risk']}<br>
                <strong>Pourcentage :</strong> {risk_info['percentage']}<br>
                <strong>Facteurs :</strong> {risk_info['factors']}<br>
            </div>
            """
            return tooltip_content

        # Ajouter le GeoJSON avec des Tooltips détaillés
        geojson = folium.GeoJson(
            geojson_path,
            name="Carte des risques",
            style_function=style_function,
        )

        # Ajouter des tooltips au GeoJSON
        geojson.add_child(folium.GeoJsonTooltip(
            fields=["region"],
            aliases=["Région :"],
            labels=True,
            sticky=True,
            style=("background-color: white; color: black; font-family: Arial; font-size: 12px; padding: 10px;"),
            parse_html=True,
            show=True
        ))

        # Ajouter le GeoJSON à la carte
        geojson.add_to(self.map)

        # Enregistrer la carte dans un fichier HTML
        map_html_path = os.path.join(os.path.dirname(__file__), 'map_maroc_regions.html')
        self.map.save(map_html_path)

        # Créer un QWebEngineView pour afficher la carte
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl.fromLocalFile(map_html_path))

        # Configurer le layout
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        self.setLayout(layout)

# Classe principale de l'application
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carte des Risques")
        self.setGeometry(100, 100, 800, 600)

        # Ajouter la page des cartes
        layout = QVBoxLayout()
        self.map_page = PageMaps()
        layout.addWidget(self.map_page)
        self.setLayout(layout)


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTabWidget, QWidget, QLabel, QComboBox, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from pages.SoussMassa import RiskFactorChartsAppSoussMassa
from pages.Rabat import RiskFactorChartsAppRabat
from pages.Casa import RiskFactorChartsAppCasa
from pages.FesMeknes import DiagramAppFesMeknes

class DiagrammesFacteursRisque(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Barre de filtres
        self.filtre_layout = QHBoxLayout()
        self.main_layout.addLayout(self.filtre_layout)

        self.zone_label = QLabel("Filtrer par zone :")
        self.filtre_layout.addWidget(self.zone_label)

        self.zone_combobox = QComboBox()
        self.zone_combobox.addItems(["Rabat", "Casablanca", "Region Sous Massa","Fes Meknes","Etude comparative"])
        self.zone_combobox.currentTextChanged.connect(self.appliquer_filtre)
        self.filtre_layout.addWidget(self.zone_combobox)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        # Onglets pour les diagrammes
        self.tabs = QTabWidget()
        self.scroll_layout.addWidget(self.tabs)

        # Dictionnaire associant chaque ville à sa classe de contenu
        self.villes = {
            "Rabat": RiskFactorChartsAppRabat,
            "Casablanca": RiskFactorChartsAppCasa,
            "Region Sous Massa": RiskFactorChartsAppSoussMassa,
            "Fes Meknes" :DiagramAppFesMeknes,
            "Etude comparative" :DiagramAppFesMeknes,
            
        }

        # Sélectionner "Rabat" par défaut dans la combobox et afficher les diagrammes associés
        self.zone_combobox.setCurrentText("Rabat")
        self.appliquer_filtre("Rabat")

    def appliquer_filtre(self, zone):
        # Effacer le contenu actuel
        for i in range(self.tabs.count()):
            self.tabs.removeTab(0)

        # Obtenir le contenu de la ville choisie
        ville_class = self.villes.get(zone)
        if ville_class:
            ville_content = ville_class()
            self.tabs.addTab(ville_content, zone)

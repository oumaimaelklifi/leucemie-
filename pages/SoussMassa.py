import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd

# Charger les données
file_path = 'Patients_data_souss_massa.xlsx'
data = pd.read_excel(file_path)

class RiskFactorChartsAppSoussMassa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_tabs()

    def create_tabs(self):
        factors = {
            "Sex": "Le sexe est un facteur clé qui peut influencer les risques de santé.",
            "Age": "L'âge est un facteur important dans les analyses épidémiologiques.",
            "Year": "Analyser les années permet d'identifier les tendances temporelles.",
            "Provenance": "Les régions permettent d'étudier les disparités géographiques des risques.",
            "Profession": "La profession peut être un indicateur de certains risques spécifiques.",
            "Marital Status": "Le statut matrimonial peut influencer certains aspects des risques de santé."
        }

        for factor, explanation in factors.items():
            tab = QWidget()
            layout = QVBoxLayout()

            # Ajouter des espaces pour centrer verticalement
            layout.addStretch()  # Espace flexible en haut

           

            # Ajouter le diagramme
            canvas = self.create_chart(factor)
            layout.addWidget(canvas, alignment=Qt.AlignHCenter)

            # Ajouter une explication
            label = QLabel(explanation)
            
            label.setFont(QFont("Poppins", 16))
            label.setAlignment(Qt.AlignCenter)
            
            layout.addWidget(label, alignment=Qt.AlignHCenter)
            

            # Ajouter des espaces pour centrer verticalement
            layout.addStretch()  # Espace flexible en bas

            tab.setLayout(layout)
            self.tabs.addTab(tab, factor)

    def create_chart(self, factor):
        data_counts = data[factor].value_counts()
        labels = data_counts.index.tolist()
        sizes = data_counts.values

        if factor == "Age":
            # Diagrammes en barres pour l'Âge
            fig, ax = plt.subplots(figsize=(10, 6))  # Augmenter la taille de la figure
            ax.bar(labels, sizes, color=["#1f77b4", "#d62728"][:len(labels)])
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
            plt.xticks(rotation=45)
        elif factor == "Year":
            # Courbe pour les Années
            fig, ax = plt.subplots(figsize=(10, 6))  # Augmenter la taille de la figure
            sorted_data = data[factor].value_counts().sort_index()
            labels = sorted_data.index.tolist()
            sizes = sorted_data.values
            ax.plot(labels, sizes, marker='o', color='b')
            ax.set_title(f"Évolution annuelle", fontsize=20, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
        elif factor == "Provenance":
            # Diagrammes en barres pour les Régions
            fig, ax = plt.subplots(figsize=(10, 6))  # Augmenter la taille de la figure
            colors = plt.cm.RdBu(range(len(labels)))
            ax.bar(labels, sizes, color=colors)
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
            plt.xticks(rotation=45)
        elif factor in ["Profession", "Marital Status", "Sex"]:
            # Diagrammes circulaires
            fig, ax = plt.subplots(figsize=(10, 6))  # Augmenter la taille de la figure
            wedges, texts, autotexts = ax.pie(
                sizes, autopct="%1.1f%%", startangle=90, colors=["#1f77b4", "#d62728", "#ff7f0e", "#2ca02c"][:len(labels)]
            )
            ax.legend(wedges, labels, title="Légende", loc="upper right", bbox_to_anchor=(1.2, 0.8))
            for text in autotexts:
                text.set_color("white")
                text.set_fontsize(10)
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})

        canvas = FigureCanvas(fig)
        return canvas



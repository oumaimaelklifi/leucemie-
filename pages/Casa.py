import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Charger les données
data = pd.read_csv('Data/Patients_data_casa.csv')

class RiskFactorChartsAppCasa(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_tabs()

    def create_tabs(self):
        factors = {
            "Sexe": "Le sexe peut influencer la susceptibilité à certains types de leucémie.",
            "Âge": "L'âge est un facteur déterminant pour évaluer le risque de leucémie.",
            "Environnement": "L'environnement peut jouer un rôle dans l'exposition aux facteurs de risque.",
            "Type de leucémie": "Différents types de leucémie affectent des groupes spécifiques.",
            "Tabagisme": "Le tabagisme est un facteur de risque important pour plusieurs cancers, y compris la leucémie.",
            "Génétique": "Les prédispositions génétiques augmentent le risque de développer une leucémie."
        }

        for factor, explanation in factors.items():
            tab = QWidget()
            layout = QVBoxLayout()

            # Ajouter le diagramme
            canvas = self.create_chart(factor)
            layout.addWidget(canvas)

            # Ajouter une explication
            label = QLabel(explanation)
            
            label.setFont(QFont("Arial", 16))
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

            tab.setLayout(layout)
            self.tabs.addTab(tab, factor)

    def create_chart(self, factor):
        if factor == "Âge" or factor == "Type de leucémie":
            # Diagrammes en barres
            data_counts = data[factor].value_counts()
            labels = data_counts.index.tolist()
            sizes = data_counts.values

            fig, ax = plt.subplots()
            ax.bar(labels, sizes, color=["#1f77b4", "#d62728"][:len(labels)])
            ax.set_title(f"Répartition par {factor}", fontsize=14)
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
            plt.xticks(rotation=45)
        elif factor == "Tabagisme":
            # Tabagisme: ajouter un diagramme circulaire et deux diagrammes en barres
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))

            # Diagramme circulaire pour Tabagisme
            data_counts = data[factor].value_counts()
            sizes = data_counts.values
            labels = data_counts.index.tolist()

            wedges, texts, autotexts = axes[0].pie(
                sizes, autopct="%1.1f%%", startangle=90, colors=["#1f77b4", "#d62728"][:len(labels)]
            )
            axes[0].legend(wedges, labels, title="Légende", loc="upper right")
            for text in autotexts:
                text.set_color("white")
                text.set_fontsize(10)
            axes[0].set_title("Répartition des Fumeurs et Non-Fumeurs",fontsize=18, fontdict={'weight': 'bold'})

            # Relation entre Tabagisme et Âge
            age_smoking = pd.crosstab(data["Âge"], data[factor])
            age_smoking.plot(kind="bar", stacked=True, ax=axes[1], color=["#1f77b4", "#d62728"])
            axes[1].set_title("Relation entre Tabagisme et Âge")
            axes[1].set_ylabel("Nombre de patients")
            axes[1].set_xlabel("Âge")

            # Relation entre Tabagisme et Sexe
            sex_smoking = pd.crosstab(data["Sexe"], data[factor])
            sex_smoking.plot(kind="bar", stacked=True, ax=axes[2], color=["#1f77b4", "#d62728"])
            axes[2].set_title("Relation entre Tabagisme et Sexe")
            axes[2].set_ylabel("Nombre de patients")
            axes[2].set_xlabel("Sexe")

            fig.tight_layout()
        else:
            # Diagramme circulaire pour les autres facteurs
            data_counts = data[factor].value_counts()
            sizes = data_counts.values
            labels = data_counts.index.tolist()

            fig, ax = plt.subplots()
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

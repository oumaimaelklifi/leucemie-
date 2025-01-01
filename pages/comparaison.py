import sys
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

age_data = pd.DataFrame({
    "Casablanca": [151, 143, 123, 94, 101, 121, 72, 195],
    "Souss-Massa": [0, 0, 0, 42, 600, 349, 9, 0],
    "Rabat": [151, 56, 88, 84, 217, 236, 122, 46],
    "Fès": [63, 0, 295, 0, 363, 0, 279, 0]
}, index=["[0-9]", "[10-19]", "[20-29]", "[30-39]", "[40-49]", "[50-59]", "[60-69]", "70+"])

sex_data = pd.DataFrame({
    "Hommes": [537, 475, 577, 517],
    "Femmes": [463, 525, 423, 483]
}, index=["Casablanca", "Souss-Massa", "Rabat", "Fès"])


class DiagramComparaison(QWidget):
    def __init__(self, title_text, data, colors, explanation_text, bar_labels=None):
        super().__init__()
        self.data = data
        self.colors = colors
        self.bar_labels = bar_labels
        self.title_text = title_text

        layout = QVBoxLayout(self)

      
        title = QLabel(title_text)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        layout.addWidget(title)

        # Create a bar chart
        if not data.empty:
            self.fig, self.ax = plt.subplots(figsize=(8, 6))
            if bar_labels:
                x = np.arange(len(data.index))
                width = 0.35
                self.ax.bar(x - width / 2, data.iloc[:, 0], width, label=bar_labels[0], color=colors[0])
                self.ax.bar(x + width / 2, data.iloc[:, 1], width, label=bar_labels[1], color=colors[1])
                self.ax.set_xticks(x)
                self.ax.set_xticklabels(data.index)
            else:
                data.plot(kind="bar", ax=self.ax, color=colors, legend=True)

            self.ax.set_title(title_text, fontsize=18)
            self.ax.set_ylabel("Valeur", fontsize=16)
            self.ax.set_xlabel("Catégories", fontsize=16)
            self.ax.legend(loc="upper right")
            canvas = FigureCanvas(self.fig)
            layout.addWidget(canvas)
            plt.close(self.fig)
        else:
            error_label = QLabel("Données insuffisantes pour créer un graphique.")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)

      
        explanation = QLabel(explanation_text)
        explanation.setWordWrap(True)
        explanation.setAlignment(Qt.AlignCenter)
        explanation.setStyleSheet("font-size: 20px;")
        layout.addWidget(explanation)

        self.download_button = QPushButton("Télécharger le graphique en PDF")
        self.download_button.clicked.connect(self.download_pdf)
        layout.addWidget(self.download_button)

 

    def download_pdf(self):
        if hasattr(self, "fig"):
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Enregistrer le graphique", "", "PDF Files (*.pdf);;All Files (*)", options=options
            )
            if file_path:
                # Ouvrir le fichier PDF pour y ajouter le contenu
                with PdfPages(file_path) as pdf:
                 
                    fig, ax = plt.subplots(figsize=(8.5, 11))
                    ax.axis("off")  

                    # Contenu de la page de garde
                    title = "Etude comparative sur la leucémie au Maroc)"
                    subtitle = "Une étude épidémiologique rétrospective descriptive, quantitative et analytique."
                    footer = " Ministère de la Santé - Juin 2019"

                    # Ajouter des éléments au design
                    ax.text(0.5, 0.85, title, fontsize=20, fontweight="bold", ha="center", color="#003366")
                    ax.text(0.5, 0.8, subtitle, fontsize=12, ha="center", style="italic", color="#555555")
                    ax.text(0.5, 0.15, footer, fontsize=10, ha="center", color="#777777")

                    # Ajouter un rectangle pour le style
                    ax.add_patch(plt.Rectangle((0.2, 0.2), 0.6, 0.01, color="#003366"))
                    ax.add_patch(plt.Rectangle((0.2, 0.18), 0.6, 0.01, color="#cccccc"))

                    pdf.savefig(fig)
                    plt.close(fig)

                    # Ajouter une page supplémentaire pour le contenu structuré
                    fig, ax = plt.subplots(figsize=(8.5, 11))
                    ax.axis("off")  # Cacher les axes

                    # Contenu structuré
                    content = [
                        "### Introduction :",
                        "La synthèse suivante met en évidence les facteurs communs ainsi que les différences spécifiques aux régions étudiées : Casablanca, Rabat, Souss-Massa, et Fès-Meknès.",
                        "",
                        "### Facteurs communs:",
                        "-Tabagisme ",
                        "- Répartition par âge ",
                        "- Environnement .",
                        "",
                        "### Différences régionales dans les facteurs de risque :\n\n",
                        "- Casablanca :Tabagisme élevé : Le tabagisme est particulièrement dominant chez les hommes (26,9 % à 35,9 %),.\n",
                        "- Rabat :Répartition par sexe : Les hommes présentent un taux dincidence légèrement supérieur (3,2 %) à celui des femmes (2,5 %).\n",
                        "- Souss-Massa :	Dominance féminine : Contrairement aux autres régions, les femmes représentent 52 % des cas.\n",
                        "- Fès-Meknès :Prévalence de la leucémie myéloïde chronique : Cette forme représente 46,7 % des cas recensés dans la région .\n",


                       
                    ]

                 
                    y = 0.9
                    for line in content:
                        ax.text(0.1, y, line, fontsize=11, wrap=True, ha="left", color="#333333")
                        y -= 0.05

                    pdf.savefig(fig)
                    plt.close(fig)

                    pdf.savefig(self.fig)
                    plt.close(self.fig)

                print(f"Graphique sauvegardé dans {file_path}")



class Comparaison(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

    
        age_tab = DiagramComparaison(
            "Comparaison du Facteur d'Âge par Catégories",
            age_data,
            colors=["#004c99", "#0073e6", "#3399ff", "#99ccff"],
            explanation_text="Ce diagramme compare les tranches d'âge des patients dans les différentes régions. "
                             "Chaque barre représente une région spécifique et une catégorie d'âge (par tranche de 10 ans)."
        )
        self.tabs.addTab(age_tab, "Âge")

    
        sex_tab = DiagramComparaison(
            "Comparaison du Facteur de Sexe",
            sex_data,
            colors=["#3399ff", "#b30000"],
            explanation_text="Ce diagramme compare le sexe (homme/femme) des patients dans les différentes régions. "
                             "Chaque groupe de barres représente une région, avec une barre pour les hommes et une barre pour les femmes.",
            bar_labels=["Hommes", "Femmes"]
        )
        self.tabs.addTab(sex_tab, "Sexe")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Comparaison()
    window.setWindowTitle("Comparaison des Facteurs")
    window.show()
    sys.exit(app.exec_())

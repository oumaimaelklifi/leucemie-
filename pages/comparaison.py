import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

# Data from the summary tables
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
        layout = QVBoxLayout(self)

        # Title of the tab
        title = QLabel(title_text)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold;")  
        layout.addWidget(title)

        # Create a bar chart
        if not data.empty:
            fig, ax = plt.subplots(figsize=(8, 6))
            if bar_labels:
                x = np.arange(len(data.index))  
                width = 0.35  
                ax.bar(x - width / 2, data.iloc[:, 0], width, label=bar_labels[0], color=colors[0])
                ax.bar(x + width / 2, data.iloc[:, 1], width, label=bar_labels[1], color=colors[1])
                ax.set_xticks(x)
                ax.set_xticklabels(data.index)
            else:
                data.plot(kind="bar", ax=ax, color=colors, legend=True)

            ax.set_title(title_text, fontsize=18)
            ax.set_ylabel("Valeur", fontsize=16)
            ax.set_xlabel("Catégories", fontsize=16)
            ax.legend(loc="upper right")
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
            plt.close(fig) 
        else:
            error_label = QLabel("Données insuffisantes pour créer un graphique.")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)

        # Explanation text
        explanation = QLabel(explanation_text)
        explanation.setWordWrap(True)
        explanation.setAlignment(Qt.AlignCenter)
        explanation.setStyleSheet("font-size: 20px;") 
        layout.addWidget(explanation)


class Comparaison(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Age factor tab
        age_tab = DiagramComparaison(
            "Comparaison du Facteur d'Âge par Catégories",
            age_data,
            colors=["#004c99", "#0073e6", "#3399ff", "#99ccff"],
            explanation_text="Ce diagramme compare les tranches d'âge des patients dans les différentes régions. "
                             "Chaque barre représente une région spécifique et une catégorie d'âge (par tranche de 10 ans)."
        )
        self.tabs.addTab(age_tab, "Âge")

        # Sex factor tab
        sex_tab = DiagramComparaison(
            "Comparaison du Facteur de Sexe",
            sex_data,
            colors=["#3399ff", "#b30000"],
            explanation_text="Ce diagramme compare le sexe (homme/femme) des patients dans les différentes régions. "
                             "Chaque groupe de barres représente une région, avec une barre pour les hommes et une barre pour les femmes.",
            bar_labels=["Hommes", "Femmes"]
        )
        self.tabs.addTab(sex_tab, "Sexe")


# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Comparaison()
    window.setWindowTitle("Comparaison des Facteurs")
    window.show()
    sys.exit(app.exec_())

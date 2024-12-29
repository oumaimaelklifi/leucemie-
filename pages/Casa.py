import os
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

# Charger les données
data = pd.read_csv('Data/Patients_data_casa.csv')

class RiskFactorChartsAppCasa(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("Analyse des facteurs de risque de leucémie")

        self.tabs = QTabWidget()
        self.figures = []  # Liste pour stocker les graphiques

        self.create_tabs()  # Créer les onglets
        self.add_export_button_to_main_window()  # Ajouter le bouton d'exportation

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
            canvas, fig = self.create_chart(factor)
            self.figures.append(fig)  # Stocker les figures pour le PDF
            layout.addWidget(canvas)

            # Ajouter une explication
            label = QLabel(explanation)
            label.setFont(QFont("Arial", 16))
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

            tab.setLayout(layout)
            self.tabs.addTab(tab, factor)

    def create_chart(self, factor):
        if factor in ["Âge", "Type de leucémie"]:
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
            # Diagrammes multiples pour Tabagisme
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))

            # Diagramme circulaire
            data_counts = data[factor].value_counts()
            sizes = data_counts.values
            labels = data_counts.index.tolist()

            wedges, texts, autotexts = axes[0].pie(
                sizes, autopct="%1.1f%%", startangle=90, colors=["#1f77b4", "#d62728"][:len(labels)]
            )
            axes[0].legend(wedges, labels, title="Légende", loc="upper right")
            axes[0].set_title("Répartition des Fumeurs et Non-Fumeurs", fontsize=18, fontweight='bold')

            # Relation entre Tabagisme et Âge
            age_smoking = pd.crosstab(data["Âge"], data[factor])
            age_smoking.plot(kind="bar", stacked=True, ax=axes[1], color=["#1f77b4", "#d62728"])
            axes[1].set_title("Relation entre Tabagisme et Âge")

            # Relation entre Tabagisme et Sexe
            sex_smoking = pd.crosstab(data["Sexe"], data[factor])
            sex_smoking.plot(kind="bar", stacked=True, ax=axes[2], color=["#1f77b4", "#d62728"])
            axes[2].set_title("Relation entre Tabagisme et Sexe")

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
            ax.legend(wedges, labels, title="Légende", loc="upper right")
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontweight='bold')

        canvas = FigureCanvas(fig)
        return canvas, fig

    def add_export_button_to_main_window(self):
        export_button = QPushButton("Exporter les graphiques en PDF")
        export_button.setFont(QFont("Arial", 14))
        export_button.clicked.connect(self.export_to_pdf)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(export_button)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def export_to_pdf(self, event=None):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pdf_path = os.path.join(desktop_path, "Casablanca_Rapport.pdf")

        with PdfPages(pdf_path) as pdf:
            # Première page : Page de garde
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.axis("off")  # Cacher les axes

            # Contenu de la page de garde
            title = "Rapport sur la leucémie\n ville de Casablanca\n\n "
            subtitle = "\n\n\n\n\n\n\n\nNombre de population affectée par la leucémie : 1000 patients\n Une étude épidémiologique rétrospective descriptive, quantitative et analytique\nLes études menées au Maroc sur les facteurs de risque liés à la leucémie ont révélé plusieurs\n éléments importants."
          
            footer = "Casablanca - Ministère de la Santé "

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
                "Études sur les facteurs de risque liés à la leucémie au Maroc",
                "",
                "Les études menées au Maroc sur les facteurs de risque liés à la leucémie ont révélé plusieurs éléments importants. Les facteurs suivants sont fréquemment cités :",
                "- Sexe, âge, état civil, origine (ville).",
                "- Environnement (urbain/rural), profession.",
                "- Mode de paiement, localisation et types de cancer.",
                "",
                "### Tabagisme :",
                "- Le tabagisme actif et passif a été identifié comme un facteur de risque significatif",
                "dans plusieurs études, augmentant le risque de divers cancers, y compris la leucémie..",
               
                "",
                "### Impact environnemental:",
                "- La majorité de la population citadine (91,6 %)\nest plus exposée que les ruraux (8,4 %) ",
               
                "",
            ]

            # Ajout du contenu structuré
            y = 0.9
            for line in content:
                ax.text(0.1, y, line, fontsize=11, wrap=True, ha="left", color="#333333")
                y -= 0.05


            # Assurez-vous que l'espacement est suffisant pour ne pas trop surcharger la page


            pdf.savefig(fig)
              
            for fig in self.figures:
                pdf.savefig(fig)
            plt.close(fig)

        os.startfile(pdf_path)

    
if __name__ == "__main__":
    app = QApplication([])
    window = RiskFactorChartsAppCasa()
    window.show()
    app.exec_()

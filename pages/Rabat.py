import os
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

# Charger les données
data = pd.read_csv('Data/patients_data_rabat.csv')

class RiskFactorChartsAppRabat(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagrammes des Facteurs de Risque")
        self.setGeometry(100, 100, 1000, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.figures = []  
        
        self.create_tabs() 
        self.add_export_button_to_main_window() 

    def create_tabs(self):
        factors = {
            "Sexe": "Le sexe peut influencer la prévalence de certains types de leucémie.",
            "Groupe d'âge": "L'âge est un facteur de risque clé pour divers types de leucémie.",
            "Type de leucémie": "Différents types de leucémie affectent des populations distinctes.",
            "Tabagisme": "Le tabagisme est un facteur de risque connu pour plusieurs maladies, y compris les cancers."
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
            layout.addWidget(label, alignment=Qt.AlignHCenter)

            tab.setLayout(layout)
            self.tabs.addTab(tab, factor)

    def create_chart(self, factor):
        data_counts = data[factor].value_counts()
        labels = data_counts.index.tolist()
        sizes = data_counts.values

        if factor == "Groupe d'âge":
            sorted_data = data[factor].value_counts().sort_index()
            labels = sorted_data.index.tolist()
            sizes = sorted_data.values
            fig, ax = plt.subplots(figsize=(8.27, 8))
            ax.bar(labels, sizes, color=["#1f77b4", "#d62728"][:len(labels)])
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
            plt.xticks(rotation=45)
        elif factor == "Type de leucémie":
            fig, ax = plt.subplots(figsize=(8.27, 8))
            ax.bar(labels, sizes, color=["#1f77b4", "#d62728"][:len(labels)])
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
            plt.xticks(rotation=45)
        else:
            fig, ax = plt.subplots(figsize=(8.27, 8))
            wedges, texts, autotexts = ax.pie(
                sizes, autopct="%1.1f%%", startangle=90, colors=["#1f77b4", "#d62728", "#ff7f0e", "#2ca02c"][:len(labels)]
            )
            ax.legend(wedges, labels, title="Légende", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})
            for text in autotexts:
                text.set_color("white")
                text.set_fontsize(10)

        canvas = FigureCanvas(fig)
        self.figures.append(fig)  
        return canvas

    def add_export_button_to_main_window(self):
        export_button = QPushButton("Exporter les graphiques en PDF")
        export_button.setFont(QFont("Arial", 14))
        export_button.clicked.connect(self.export_to_pdf)

        layout = QVBoxLayout()
        layout.addWidget(export_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(self.tabs)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(export_button)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def export_to_pdf(self):
        # Détecter le bureau de l'utilisateur
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pdf_path = os.path.join(desktop_path, "Rapport_Rabat.pdf")

        # Générer le fichier PDF
        with PdfPages(pdf_path) as pdf:
            # Ajouter une page de titre
            fig, ax = plt.subplots(figsize=(8.27, 11.69))  # Taille A4
            ax.axis('off')

            title = "Rapport de la Ville de Rabat"
            subtitle = "Nombre de population affectée par la leucémie : 1000 patients"
            risk_factors = (
                "Facteurs de risque principaux :\n\n"
                "- Tabagisme : 13.4%\n\n"
                "- Répartition par sexe : Femme/Homme\n\n"
                "- Groupes d'âge : Les âges les plus touchés.\n\n"
            )

            ax.text(0.5, 0.85, title, fontsize=24, fontweight='bold', ha='center')
            ax.text(0.5, 0.75, subtitle, fontsize=16, ha='center', fontweight='bold')
            ax.text(0.2, 0.6, risk_factors, fontsize=16, va='top')

            pdf.savefig(fig)
            plt.close(fig)

            # Ajouter les diagrammes avec explications sur la même page
            factors_explanations = {
                "Sexe": "Le sexe peut influencer la prévalence de certains types de leucémie.",
                "Groupe d'âge": "L'âge est un facteur de risque clé pour divers types de leucémie.",
                "Type de leucémie": "Différents types de leucémie affectent des populations distinctes.",
                "Tabagisme": "Le tabagisme est un facteur de risque connu pour plusieurs maladies, y compris les cancers."
            }

            for fig, (factor, explanation) in zip(self.figures, factors_explanations.items()):
                # Sauvegarder le graphique temporairement en tant qu'image avec une meilleure résolution
                image_path = os.path.join(desktop_path, f"{factor}.png")
                fig.savefig(image_path, format='png', bbox_inches='tight', dpi=300)  # Augmenter la résolution à 300 dpi

                # Créer une nouvelle figure combinée
                combined_fig, axs = plt.subplots(2, 1, figsize=(8.27, 11.69))  # Taille A4, deux sous-graphes
                axs[0].axis('off')  # Zone pour le texte explicatif
                axs[0].text(
                    0.5, 0.5, explanation, fontsize=14, wrap=True, ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="#f0f0f0")
                )

                # Charger l'image sauvegardée et l'afficher
                img = plt.imread(image_path)
                axs[1].imshow(img, aspect='auto')
                axs[1].axis('off')

                # Sauvegarder la page combinée dans le PDF
                pdf.savefig(combined_fig)
                plt.close(combined_fig)

                # Supprimer l'image temporaire
                os.remove(image_path)

        print(f"PDF sauvegardé sur le bureau : {pdf_path}")
        os.startfile(pdf_path)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RiskFactorChartsAppRabat()
    window.show()
    sys.exit(app.exec_())

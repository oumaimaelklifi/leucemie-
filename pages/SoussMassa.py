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
file_path = 'Data/Patients_data_souss_massa.xlsx'
data = pd.read_excel(file_path)

class RiskFactorChartsAppSoussMassa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.figures = []  # Pour stocker les figures pour l'export PDF
        self.explanations = {}  # Pour stocker les explications
        self.create_tabs()
        self.add_export_button()

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
            layout.addStretch()

            # Ajouter le diagramme
            canvas = self.create_chart(factor)
            layout.addWidget(canvas, alignment=Qt.AlignHCenter)

            # Ajouter l'explication
            label = QLabel(explanation)
            label.setFont(QFont("Poppins", 16))
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label, alignment=Qt.AlignHCenter)

            # Ajouter des espaces pour centrer verticalement
            layout.addStretch()

            tab.setLayout(layout)
            self.tabs.addTab(tab, factor)

            # Enregistrer l'explication dans un dictionnaire pour export PDF
            self.explanations[factor] = explanation

        # Ajouter le titre, sous-titre et facteurs de risque dans un onglet
        intro_tab = QWidget()
        intro_layout = QVBoxLayout()

        title = QLabel("Rapport de la ville de Casablanca")
        title.setFont(QFont("Poppins", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Nombre de population affectée par la leucémie : 1000 patients")
        subtitle.setFont(QFont("Poppins", 18))
        subtitle.setAlignment(Qt.AlignCenter)

        risk_factors = QLabel(
            "Facteurs de risque principaux :\n\n"
            "- Répartition par sexe : Femme/Homme\n\n"
            "- Groupes d'âge : Les âges les plus touchés.\n\n"
        )
        risk_factors.setFont(QFont("Poppins", 16))
        risk_factors.setAlignment(Qt.AlignLeft)

        intro_layout.addWidget(title)
        intro_layout.addWidget(subtitle)
        intro_layout.addWidget(risk_factors)
        intro_tab.setLayout(intro_layout)
        self.tabs.addTab(intro_tab, "Introduction")

    def create_chart(self, factor):
        data_counts = data[factor].value_counts()
        labels = data_counts.index.tolist()
        sizes = data_counts.values

        if factor == "Age":
            # Diagrammes en barres pour l'Âge
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(labels, sizes, color=["#1f77b4", "#d62728"][:len(labels)])
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
            plt.xticks(rotation=45)
        elif factor == "Year":
            # Courbe pour les Années
            fig, ax = plt.subplots(figsize=(10, 6))
            sorted_data = data[factor].value_counts().sort_index()
            labels = sorted_data.index.tolist()
            sizes = sorted_data.values
            ax.plot(labels, sizes, marker='o', color='b')
            ax.set_title(f"Évolution annuelle", fontsize=20, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
        elif factor == "Provenance":
            # Diagrammes en barres pour les Régions
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = plt.cm.RdBu(range(len(labels)))
            ax.bar(labels, sizes, color=colors)
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
            plt.xticks(rotation=45)
        elif factor in ["Profession", "Marital Status", "Sex"]:
            # Diagrammes circulaires
            fig, ax = plt.subplots(figsize=(10, 6))
            wedges, texts, autotexts = ax.pie(
                sizes, autopct="%1.1f%%", startangle=90, colors=["#1f77b4", "#d62728", "#ff7f0e", "#2ca02c"][:len(labels)]
            )
            ax.legend(wedges, labels, title="Légende", loc="upper right", bbox_to_anchor=(1.2, 0.8))
            for text in autotexts:
                text.set_color("white")
                text.set_fontsize(10)
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})

        canvas = FigureCanvas(fig)

        # Ajouter la figure à la liste pour l'export PDF
        self.figures.append(fig)

        return canvas

    def add_export_button(self):
        export_button = QPushButton("Exporter les graphiques en PDF")
        export_button.setFont(QFont("Arial", 14))
        export_button.clicked.connect(self.export_to_pdf)

        layout = QVBoxLayout()
        layout.addWidget(export_button)
        container = QWidget()
        container.setLayout(layout)
        self.tabs.addTab(container, "Exporter")

    def export_to_pdf(self):
        # Détecter le bureau de l'utilisateur
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pdf_path = os.path.join(desktop_path, "SoussMassa_Rapport.pdf")

        # Générer le fichier PDF
        with PdfPages(pdf_path) as pdf:
            # Ajouter le titre et sous-titre
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.7, "Rapport de la ville de Casablanca", ha='center', va='center', fontsize=24, fontweight='bold')
            ax.text(0.5, 0.5, "Nombre de population affectée par la leucémie : 1000 patients", ha='center', va='center', fontsize=18)
            ax.text(0.5, 0.3, "Facteurs de risque principaux :\n- Répartition par sexe : Femme/Homme\n- Groupes d'âge : Les âges les plus touchés.", ha='center', va='center', fontsize=16)
            ax.axis('off')  # Désactiver les axes
            pdf.savefig(fig)
            plt.close(fig)

            # Ajouter les graphiques et explications
            for fig, factor in zip(self.figures, self.explanations.keys()):
                # Ajouter le graphique
                pdf.savefig(fig)
                plt.close(fig)  # Fermer la figure après l'avoir enregistrée

                # Ajouter l'explication sous chaque graphique
                explanation_text = self.explanations[factor]
                fig, ax = plt.subplots(figsize=(10, 2))  # Un petit graphique vide pour l'explication
                ax.text(0.5, 0.5, explanation_text, ha='center', va='center', fontsize=12)
                ax.axis('off')  # Désactiver les axes
                pdf.savefig(fig)
                plt.close(fig)

            print(f"PDF sauvegardé sur le bureau : {pdf_path}")

        # Ouvrir automatiquement le fichier PDF
        os.startfile(pdf_path)


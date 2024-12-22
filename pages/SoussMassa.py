import os
import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget,
    QLabel, QComboBox, QHBoxLayout, QPushButton
)
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
        self.setWindowTitle("Analyse des Facteurs de Risque - Souss Massa")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.selected_provenance = None  # Provenance sélectionnée
        self.figures = []  # Stockage des figures pour exportation
        self.create_tabs()
        self.add_export_button()

    def create_tabs(self):
        # Ajouter un onglet pour les graphiques interactifs (avec provenance)
        self.main_tab = QWidget()
        self.tabs.addTab(self.main_tab, "Provenances")

        layout = QVBoxLayout()

        # Ajouter le filtre de provenance
        filter_layout = QHBoxLayout()
        self.filter_label = QLabel("Provenance")
        self.filter_label.setFont(QFont("Poppins", 12))
        self.filter_label.setAlignment(Qt.AlignLeft)

        self.provenance_selector = QComboBox()
        self.provenance_selector.addItem("Toutes les provenances")
        self.provenance_selector.addItems(sorted(data["Provenance"].unique()))
        self.provenance_selector.currentIndexChanged.connect(self.update_charts)

        filter_layout.addWidget(self.filter_label)
        filter_layout.addWidget(self.provenance_selector)
        layout.addLayout(filter_layout)

        # Conteneur pour les graphiques
        self.chart_container = QVBoxLayout()
        layout.addLayout(self.chart_container)
        
        # Ajouter la zone d'explication
        self.explanation_label = QLabel("")
        self.explanation_label.setFont(QFont("Poppins", 14))
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.explanation_label)

        self.main_tab.setLayout(layout)

        # Mettre à jour les graphiques au démarrage avec toutes les provenances
        self.update_charts()

        # Créer des onglets statiques pour chaque facteur
        factors = {
            "Sex": "Le sexe est un facteur clé qui peut influencer les risques de santé.",
            "Age": "L'âge est un facteur important dans les analyses épidémiologiques.",
            "Year": "Analyser les années permet d'identifier les tendances temporelles.",
            "Profession": "La profession peut être un indicateur de certains risques spécifiques.",
            "Marital Status": "Le statut matrimonial peut influencer certains aspects des risques de santé."
        }

        for factor, explanation in factors.items():
            tab = QWidget()
            layout = QVBoxLayout()

            # Ajouter un diagramme
            canvas = self.create_chart(factor, data)
            layout.addWidget(canvas, alignment=Qt.AlignHCenter)

            # Ajouter une explication
            label = QLabel(explanation)
            label.setFont(QFont("Poppins", 12))
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

            tab.setLayout(layout)
            self.tabs.addTab(tab, factor)

    def update_charts(self):
        # Supprimer les graphiques existants
        while self.chart_container.count():
            widget_to_remove = self.chart_container.takeAt(0).widget()
            if widget_to_remove:
                widget_to_remove.deleteLater()

        # Mettre à jour l'étiquette de provenance
        self.selected_provenance = self.provenance_selector.currentText()
        self.filter_label.setText(
            self.selected_provenance if self.selected_provenance != "Toutes les provenances" else "Provenance"
        )

        # Effacer les graphiques existants
        for i in reversed(range(self.chart_container.count())):
            widget_to_remove = self.chart_container.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)

        # Filtrer les données selon la provenance sélectionnée
        self.selected_provenance = self.provenance_selector.currentText()
        if self.selected_provenance != "Toutes les provenances":
            filtered_data = data[data["Provenance"] == self.selected_provenance]
        else:
            filtered_data = data

        pie_charts_layout = QHBoxLayout()
        bar_charts_layout = QHBoxLayout()

        # Ajouter des graphiques
        factors_circle = ["Sex", "Environment"]
        factors_bar = ["Marital Status", "Support Mode"]

        for factor in factors_circle:
            if factor in filtered_data.columns:
                chart = self.create_pie_chart(filtered_data, factor)
                pie_charts_layout.addWidget(chart)

        for factor in factors_bar:
            if factor in filtered_data.columns:
                chart = self.create_bar_chart(filtered_data, factor)
                bar_charts_layout.addWidget(chart)

        self.chart_container.addLayout(pie_charts_layout)
        self.chart_container.addLayout(bar_charts_layout)

        # Générer une phrase globale pour la provenance choisie
        if self.selected_provenance == "Toutes les provenances":
            general_explanation = "Les graphiques montrent la distribution globale des facteurs de risque pour toutes les provenances."
        else:
            general_explanation = f"Les graphiques montrent des tendances spécifiques pour la ville {self.selected_provenance}."

        # Ajouter la phrase explicative
        self.explanation_label.setText(general_explanation)

    def create_chart(self, factor, dataset):
        data_counts = dataset[factor].value_counts()
        labels = data_counts.index.tolist()
        sizes = data_counts.values

        if factor == "Age":
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(labels, sizes, color=["#1f77b4", "#d62728"][:len(labels)])
            ax.set_title(f"Répartition par {factor}", fontsize=15, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
            plt.xticks(rotation=45)
        elif factor == "Year":
            fig, ax = plt.subplots(figsize=(10, 6))
            sorted_data = dataset[factor].value_counts().sort_index()
            labels = sorted_data.index.tolist()
            sizes = sorted_data.values
            ax.plot(labels, sizes, marker='o', color='b')
            ax.set_title("Évolution annuelle", fontsize=20, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            wedges, texts, autotexts = ax.pie(
                sizes, autopct="%1.1f%%", startangle=90,
                colors=["#1f77b4", "#d62728", "#ff7f0e", "#2ca02c"][:len(labels)]
            )
            ax.legend(wedges, labels, title="Légende", loc="upper right", bbox_to_anchor=(1.2, 0.8))
            ax.set_title(f"Répartition par {factor}", fontsize=15, fontdict={'weight': 'bold'})

        canvas = FigureCanvas(fig)
        self.figures.append(fig)  
        return canvas
    
    def create_pie_chart(self, filtered_data, factor):
        data_counts = filtered_data[factor].value_counts()
        labels = data_counts.index.tolist()
        sizes = data_counts.values

        fig, ax = plt.subplots(figsize=(4, 3))  # Taille réduite des graphiques
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct="%1.1f%%", startangle=90,
            colors=["#1f77b4", "#d62728"]
        )
        ax.set_title(f"Répartition par {factor}", fontsize=12)

        canvas = FigureCanvas(fig)
        return canvas

    def create_bar_chart(self, filtered_data, factor):
        data_counts = filtered_data[factor].value_counts()
        categories = data_counts.index.tolist()
        values = data_counts.values

        fig, ax = plt.subplots(figsize=(5, 3))  # Taille réduite des graphiques
        ax.bar(categories, values, color=["#1f77b4", "#d62728"][:len(categories)])
        ax.set_title(f"Répartition par {factor}", fontsize=12)
        ax.set_ylabel("Nombre de patients")
        ax.set_xlabel(factor)

        canvas = FigureCanvas(fig)
        return canvas


    #def create_pie_chart(self, filtered_data, factor):
     #   return self.create_chart(factor, filtered_data)

    #def create_bar_chart(self, filtered_data, factor):
     #   return self.create_chart(factor, filtered_data)

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
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pdf_path = os.path.join(desktop_path, "SoussMassa.pdf")

        with PdfPages(pdf_path) as pdf:
            for fig in self.figures:
                pdf.savefig(fig)
            print(f"PDF sauvegardé sur le bureau : {pdf_path}")

        os.startfile(pdf_path)


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
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pdf_path = os.path.join(desktop_path, "SoussMassa_Rapport.pdf")

        with PdfPages(pdf_path) as pdf:
            # Add Title Page

            fig, ax = plt.subplots(figsize=(8.27, 11.69))  

            # Titre principal
            ax.text(0.5, 0.9, "Rapport Analyse des Facteurs de Risque", ha='center', fontsize=20, fontweight='bold')

            # Informations supplémentaires
            ax.text(0.5, 0.8, "Région : Souss Massa", ha='center', fontsize=16)
            ax.text(0.5, 0.75, "Année : 2014-2019", ha='center', fontsize=16)
            ax.text(0.5, 0.7, "Population : 1000 patients", ha='center', fontsize=16)

            # Texte descriptif long
            description = (
                "Dans la région du Souss Massa, nous avons mené une étude épidémiologique rétrospective descriptive, "
                "quantitative et analytique de plus de 40 cancers sur une période de 5,5 ans entre janvier 2014 et "
                "le premier semestre 2019."
            )
            ax.text(0.5, 0.6, description, ha='center', fontsize=14, wrap=True)

            ax.axis('off')
            pdf.savefig(fig)
            plt.close(fig)

            factors_explanations = {
                "Sexe": "Le sexe peut influencer la prévalence de certains types de leucémie.",
                "Groupe d'âge": "L'âge est un facteur de risque clé pour divers types de leucémie.",
                "Year": "Analyser les années permet d'identifier les tendances temporelles..",
                "Profession": "La profession peut être un indicateur de certains risques spécifiques.",
            }

            for fig, (factor, explanation) in zip(self.figures, factors_explanations.items()):
                # Sauvegarder le graphique temporairement en tant qu'image avec une meilleure résolution
                image_path = os.path.join(desktop_path, f"{factor}.png")
                fig.savefig(image_path, format='png', bbox_inches='tight', dpi=300)  # Augmenter la résolution à 300 dpi

                # Créer une nouvelle figure combinée
                combined_fig, axs = plt.subplots(2, 1, figsize=(8.27, 11.69))  
                axs[0].axis('off')  
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

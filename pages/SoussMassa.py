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

    def export_to_pdf(self, event=None):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pdf_path = os.path.join(desktop_path, "SoussMassa_Rapport.pdf")

        with PdfPages(pdf_path) as pdf:
            # Première page : Page de garde
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.axis("off")  # Cacher les axes

            # Contenu de la page de garde
            title = "Rapport sur la leucémie\nRégion Souss Massa\n(Janvier 2014 - Juin 2019)"
            subtitle = "Une étude épidémiologique rétrospective descriptive, quantitative et analytique."
            footer = "Région Souss Massa - Ministère de la Santé - Juin 2019"

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
                "Dans la région du Souss Massa, une étude épidémiologique rétrospective a été menée entre janvier 2014 et juin 2019.",
                "",
                "### Paramètres étudiés :",
                "- Sexe, âge, état civil, origine (ville).",
                "- Environnement (urbain/rural), profession.",
                "- Mode de paiement, localisation et types de cancer.",
                "",
                "### Incidence et facteurs de risque :",
                "- Incidence : *146,35/100 000 habitants*.",
                "- Prédominance féminine : *179,15/100 000 (p<0,0001)*.",
                "- Facteurs de risque principaux : sexe, âge, profession, et environnement.",
                "",
                "### Profil des patients :",
                "- 74% sont mariés.",
                "- 98% sans profession.",
                "- Répartition géographique : *54% urbains, **46% ruraux*.",
            ]

            # Ajout du contenu structuré
            y = 0.9
            for line in content:
                ax.text(0.1, y, line, fontsize=11, wrap=True, ha="left", color="#333333")
                y -= 0.05

            pdf.savefig(fig)
              
            for fig in self.figures:
                pdf.savefig(fig)
            plt.close(fig)

        os.startfile(pdf_path)



if __name__ == "__main__":
    app = QApplication([])
    window = RiskFactorChartsAppSoussMassa()
    window.show()
    app.exec_()

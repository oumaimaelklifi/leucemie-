import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QTabWidget, QWidget, QPushButton, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import os

# Charger les données
file_path = 'Data/Copie de patients_data_fès.xlsx'
data = pd.read_excel(file_path, engine='openpyxl')

class DiagramAppFesMeknes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1000, 800)

        self.data = data
        self.figures = []  # List to store figures for exporting

        # Initialisation de l'interface
        self.init_ui()

    def init_ui(self):
        # Create a layout for the central widget
        main_layout = QVBoxLayout()

        # Create the tab widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Ajouter les diagrammes comme onglets
        tabs.addTab(self.create_age_tab(), "Groupe d'âge")
        tabs.addTab(self.create_origin_tab(), "Origine")
        tabs.addTab(self.create_profession_tab(), "Profession")
        tabs.addTab(self.create_sex_tab(), "Sexe")

        # Create the Export Button
        export_button = QPushButton("Exporter en PDF")
        export_button.clicked.connect(self.export_to_pdf)

        # Add the button to the layout (not the toolbar)
        main_layout.addWidget(export_button)

        # Create a QWidget to set as the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_age_tab(self):
        return self.create_tab(
            self.data['Groupe d\'âge'],
            "Distribution par Groupe d'âge",
            "Cet histogramme montre la répartition des patients selon les groupes d'âge.",
            sns.color_palette(["#1f77b4", "#d62728"])
        )

    def create_origin_tab(self):
        return self.create_pie_tab(
            self.data['Origine'],
            "Répartition des Origines",
            "Ce diagramme circulaire montre la proportion des patients selon leur origine géographique.",
            ["Autre", "Fès"]
        )

    def create_profession_tab(self):
        return self.create_tab(
            self.data['Profession'],
            "Répartition par Profession",
            "Cet histogramme montre la répartition des patients selon leur profession.",
            sns.color_palette(["#1f77b4", "#d62728"])
        )

    def create_sex_tab(self):
        return self.create_pie_tab(
            self.data['Sexe'],
            "Répartition par Sexe",
            "Ce diagramme circulaire montre la répartition des patients selon leur sexe.",
            ["Homme", "Femme"]
        )

    def create_tab(self, series, title, explanation, palette):
        """Crée un onglet avec un histogramme et des explications."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Créer le graphique
        figure, ax = plt.subplots()
        sns.countplot(y=series, palette=palette, ax=ax)
        ax.set_title(title)
        ax.set_xlabel("Nombre de Patients")

        # Store the figure for PDF export
        self.figures.append(figure)

        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)

        # Ajouter une explication centrée
        explanation_label = QLabel(f"<h3 style='text-align:center;'>{explanation}</h3>")
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)

        return widget

    def create_pie_tab(self, series, title, explanation, labels):
        """Crée un onglet avec un diagramme circulaire, une légende à gauche et des explications."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Créer le graphique
        figure, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            series.value_counts(), autopct="%1.1f%%", startangle=90,
            colors=sns.color_palette(["#1f77b4", "#d62728"]), labels=labels
        )

        # Store the figure for PDF export
        self.figures.append(figure)

        ax.set_title(title)
        ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(-0.5, 0.5))
        ax.set_ylabel("") 

        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)

        # Ajouter une explication centrée et plus grande
        explanation_label = QLabel(f"<h3 style='text-align:center;'>{explanation}</h3>")
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)

        return widget

    def add_export_button(self):
        export_button = QPushButton("Exporter les graphiques en PDF")
        export_button.clicked.connect(self.export_to_pdf)

        layout = QVBoxLayout()
        layout.addWidget(export_button)
        container = QWidget()
        container.setLayout(layout)
        self.tabs.addTab(container, "Exporter")

    def export_to_pdf(self):
        # Détecter le bureau de l'utilisateur
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pdf_path = os.path.join(desktop_path, "Fes_Mekens.pdf")

        # Générer le fichier PDF
        with PdfPages(pdf_path) as pdf:
            for fig in self.figures:
                pdf.savefig(fig)
            print(f"PDF sauvegardé sur le bureau : {pdf_path}")

        # Ouvrir automatiquement le fichier PDF
        os.startfile(pdf_path)

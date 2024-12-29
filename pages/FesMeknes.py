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
        self.figures = [] 

        # Initialisation de l'interface
        self.init_ui()

    def init_ui(self):
     
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
        explanation_label = QLabel(f"<h2 style='text-align:center;'>{explanation}</h2>")
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
        explanation_label = QLabel(f"<h2 style='text-align:center;'>{explanation}</h2>")
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)

        return widget

    def add_export_button_to_main_window(self):
        export_button = QPushButton("Exporter les graphiques en PDF")
        
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

    def export_to_pdf(self, event=None):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pdf_path = os.path.join(desktop_path, "Fes_Mekens_Rapport.pdf")

        with PdfPages(pdf_path) as pdf:
            # Première page : Page de garde
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.axis("off")  # Cacher les axes

            # Contenu de la page de garde
            title = "Rapport sur la leucémie\n ville de la region de Fes Mekens\n\n "
            subtitle = "\n\n\n\n\n\n\n\nNombre de population affectée par la leucémie : 1000 patients\n Une étude épidémiologique rétrospective descriptive, quantitative et analytique\nLes études menées au Maroc sur les facteurs de risque liés à la leucémie ont révélé plusieurs\n éléments importants."
          
            footer = "- Ministère de la Santé "

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
                "- Sexe, âge,, origine (ville).",
                
                "- Mode de paiement, localisation et types de cancer.",
                "",
              
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

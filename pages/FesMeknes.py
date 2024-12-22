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

    def export_to_pdf(self):
            # Détecter le bureau de l'utilisateur
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            pdf_path = os.path.join(desktop_path, "Rapport_Fes_Meknes.pdf")

            # Générer le fichier PDF
            with PdfPages(pdf_path) as pdf:
                # Ajouter une page de titre
                fig, ax = plt.subplots(figsize=(8.27, 11.69))  # Taille A4
                ax.axis('off')

                title = "Rapport de la region de Fes Meknes "
                subtitle = "Nombre de population affectée par la leucémie : 1000 patients"
                risk_factors = (
                    "Facteurs de risque principaux :\n\n"
                    
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
        
                    "Groupe d'âge": "L'âge est un facteur de risque clé pour divers types de leucémie.",
                    "Sexe": "Le sexe peut influencer la prévalence de certains types de leucémie.",
                    
                    
                }

                for fig, (factor, explanation) in zip(self.figures, factors_explanations.items()):
                    # Sauvegarder le graphique temporairement en tant qu'image
                    image_path = os.path.join(desktop_path, f"{factor}.png")
                    fig.savefig(image_path, format='png', bbox_inches='tight')

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


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

    def export_to_pdf(self, event=None):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pdf_path = os.path.join(desktop_path, "Rabat_Rapport.pdf")

        with PdfPages(pdf_path) as pdf:
            # Première page : Page de garde
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.axis("off")  # Cacher les axes

            # Contenu de la page de garde
            title = "Rapport sur la leucémie\n ville de Rabat\n\n "
            subtitle = "\n\n\n\n\n\n\n\nNombre de population affectée par la leucémie : 1000 patients\n Une étude épidémiologique rétrospective descriptive, quantitative et analytique\nLes études menées au Maroc sur les facteurs de risque liés à la leucémie ont révélé plusieurs\n éléments importants."
          
            footer = "Rabat - Ministère de la Santé "

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
                "### Tabagisme :",
                "- Le tabagisme actif et passif a été identifié comme un facteur de risque significatif",
                "dans plusieurs études, augmentant le risque de divers cancers, y compris la leucémie..",
               
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
    app = QApplication(sys.argv)
    window = RiskFactorChartsAppRabat()
    window.show()
    sys.exit(app.exec_())

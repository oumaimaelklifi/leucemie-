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
        self.add_export_button() 

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
            fig, ax = plt.subplots()
            ax.bar(labels, sizes, color=["#1f77b4", "#d62728"][:len(labels)])
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
            plt.xticks(rotation=45)
        elif factor == "Type de leucémie":
            fig, ax = plt.subplots()
            ax.bar(labels, sizes, color=["#1f77b4", "#d62728"][:len(labels)])
            ax.set_title(f"Répartition par {factor}", fontsize=18, fontdict={'weight': 'bold'})
            ax.set_ylabel("Nombre de patients")
            ax.set_xlabel(factor)
            plt.xticks(rotation=45)
        else:
            fig, ax = plt.subplots()
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
        pdf_path = os.path.join(desktop_path, "Rabat.pdf")

        # Générer le fichier PDF
        with PdfPages(pdf_path) as pdf:
            for fig in self.figures:
                pdf.savefig(fig)
        print(f"PDF sauvegardé sur le bureau : {pdf_path}")

       
        os.startfile(pdf_path)

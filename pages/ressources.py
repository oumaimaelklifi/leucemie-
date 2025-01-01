from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QWidget,
    QLabel, QPushButton, QHBoxLayout, QGridLayout, QFileDialog
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys
from fpdf import FPDF
import shutil


class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 1366, 768)

        self.setCentralWidget(self.create_resources_tab())

    def create_resources_tab(self):
        """Crée l'onglet des ressources avec une meilleure esthétique."""
        resources_widget = QWidget()
        layout = QVBoxLayout()

   
        title = QLabel("Ressources Informatives sur la Leucémie")
        title.setFont(QFont("Arial", 15, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(17)  

      
        grid_layout.addWidget(self.create_section(
            "Causes",
            "La leucémie peut être causée par des facteurs génétiques, une exposition à des radiations, des substances chimiques toxiques (comme le benzène).",
            "assets/3.png"
        ), 0, 0)

        grid_layout.addWidget(self.create_section(
            "Symptômes",
            "Fatigue persistante, fièvre, infections fréquentes, perte de poids inexpliquée, ecchymoses ou saignements excessifs, douleurs osseuses.",
            "assets/4.png"
        ), 0, 1)

        grid_layout.addWidget(self.create_section(
            "Traitements",
            "Les traitements incluent la chimiothérapie, la radiothérapie, les thérapies ciblées et, dans certains cas, une greffe de moelle osseuse.",
            "assets/2.png"
        ), 1, 0)

        grid_layout.addWidget(self.create_section(
            "Centres de traitement",
            "- CHU Ibn Sina à Rabat\n- CHU Mohammed VI à Marrakech\n- CHU Hassan II à Fès\n- Hôpital Sheikh Khalifa à Casablanca.",
            "assets/6.png"
        ), 1, 1)

        grid_layout.addWidget(self.create_section(
            "Initiatives gouvernementales",
            "Le gouvernement marocain a lancé des programmes de sensibilisation, des dépistages gratuits, et des aides pour les patients atteints de leucémie à travers RAMED.",
            "assets/1 (2).png"
        ), 2, 0, 1, 2)

        layout.addLayout(grid_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)

        link_button = QPushButton("En savoir plus")
        link_button.setStyleSheet("background-color: #3a3a74; color: white; padding: 10px; border-radius: 5px; font-weight:700")
        link_button.clicked.connect(lambda: self.open_link("https://www.sante.gov.ma"))
        button_layout.addWidget(link_button)

     
        pdf_button = QPushButton("Télécharger les informations en PDF")
        pdf_button.setStyleSheet("background-color: #3a3a74; color: white; padding: 10px; border-radius: 5px;font-weight:700")
        pdf_button.clicked.connect(self.download_pdf)
        button_layout.addWidget(pdf_button)

        layout.addLayout(button_layout)

        resources_widget.setLayout(layout)
        return resources_widget

    def create_section(self, title, content, icon_path):
        """Crée une section visuellement améliorée avec un titre, du contenu et une image."""
        section_widget = QWidget()
        section_layout = QVBoxLayout()

        # Image
        image_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(200, 150, Qt.KeepAspectRatio)  
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        section_layout.addWidget(image_label)

        # Texte
        text_label = QLabel(f"<b>{title} :</b><br>{content}")
        text_label.setFont(QFont("Arial", 12))
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignLeft)
        section_layout.addWidget(text_label)

        section_layout.setSpacing(10)  
        section_layout.setContentsMargins(10, 10, 10, 10)
        section_widget.setLayout(section_layout)
        return section_widget

    def open_link(self, url):
        """Ouvre un lien web externe."""
        import webbrowser
        webbrowser.open(url)

    def download_pdf(self):
        """Télécharge un fichier PDF existant avec les informations de leucémie."""
       
        pdf_path = "Data/informations.pdf" 

    
        file_path, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le PDF", "informations.pdf", "PDF Files (*.pdf)")

 
        if file_path:
            try:
              
                shutil.copy(pdf_path, file_path)
            except Exception as e:
                print(f"Erreur lors de la copie du fichier PDF: {e}")


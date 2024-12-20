from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QWidget,
    QLabel, QPushButton, QHBoxLayout, QGridLayout, QFileDialog
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
import sys
from fpdf import FPDF


class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()

        # Define window properties
        self.setWindowTitle("Application Santé")
        self.setGeometry(100, 100, 1366, 768)

        # Set the main widget
        self.setCentralWidget(self.create_resources_tab())

    def create_resources_tab(self):
        """Creates the resources tab with improved aesthetics."""
        resources_widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Ressources Informatives sur la Leucémie")
        title.setFont(QFont("Arial", 15, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

     
        grid_layout = QGridLayout()
        grid_layout.setSpacing(17)  

        # Add sections to the grid
        grid_layout.addWidget(self.create_section(
            "Causes",
            "La leucémie peut être causée par des facteurs génétiques, une exposition à des radiations, des substances chimiques toxiques (comme le benzène), ou des mutations dans les cellules sanguines.",
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
            "assets/5.png"
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
        link_button.setIcon(QIcon("C:\\Users\\ADMIN\\Desktop\\images\\info.png"))
        link_button.setStyleSheet("background-color: #3a3a74; color: white; padding: 10px; border-radius: 5px;")
        link_button.clicked.connect(lambda: self.open_link("https://www.sante.gov.ma"))
        button_layout.addWidget(link_button)

        pdf_button = QPushButton("Télécharger les informations en PDF")
        pdf_button.setIcon(QIcon("C:\\Users\\ADMIN\\Desktop\\images\\download.png"))
        pdf_button.setStyleSheet("background-color: #3a3a74; color: white; padding: 10px; border-radius: 5px;")
        pdf_button.clicked.connect(self.download_pdf)
        button_layout.addWidget(pdf_button)

        layout.addLayout(button_layout)

        resources_widget.setLayout(layout)
        return resources_widget

    def create_section(self, title, content, icon_path):
        """Creates a visually enhanced section with a title, content, and image."""
        section_widget = QWidget()
        section_layout = QVBoxLayout() 

        # Image
        image_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(200, 150, Qt.KeepAspectRatio)  
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        section_layout.addWidget(image_label)

        # Text
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
        """Opens an external web link."""
        import webbrowser
        webbrowser.open(url)

    def download_pdf(self):
        """Downloads a PDF file with the leukemia information."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Informations sur la Leucémie au Maroc", ln=True, align="C")
        pdf.ln(10)

        sections = [
            ("Causes", "La leucémie peut être causée par des facteurs génétiques, une exposition à des radiations, des substances chimiques toxiques."),
            ("Symptômes", "Fatigue persistante, fièvre, infections fréquentes, perte de poids inexpliquée, douleurs osseuses."),
            ("Traitements", "Chimiothérapie, radiothérapie, thérapies ciblées, greffe de moelle osseuse."),
            ("Centres de traitement", "CHU Ibn Sina, CHU Mohammed VI, CHU Hassan II, Hôpital Sheikh Khalifa."),
            ("Initiatives gouvernementales", "Programmes de dépistage gratuits, aide RAMED pour les patients.")
        ]

        for title, content in sections:
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, txt=title, ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=content)
            pdf.ln(5)

        file_path, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le PDF", "", "PDF Files (*.pdf)")
        if file_path:
            pdf.output(file_path)



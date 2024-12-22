import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget
)
from PyQt5.QtCore import Qt
from pages.home import PageAccueil
from pages.maps import PageMaps
from pages.statistics import DiagrammesFacteursRisque
from pages.contact import PageContact
from pages.ressources import MainWindow1

# Fenêtre principale
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Leucémie")
        self.setGeometry(100, 100, 800, 600)
       
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)  
        main_layout.setContentsMargins(0, 0, 0, 0) 
        self.central_widget.setLayout(main_layout)

        # Barre de logo
        logo_bar = QVBoxLayout()
        logo_label = QLabel("Leucémie au Maroc")
        logo_label.setStyleSheet("font-family: Poppins; font-size: 29px; font-weight: bold; color: white;")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_bar_widget = QWidget()
        logo_bar_widget.setStyleSheet("background-color: #3a3a74;")
        logo_bar_widget.setLayout(logo_bar)
        logo_bar.addWidget(logo_label)
        main_layout.addWidget(logo_bar_widget)

        # Barre de navigation
        nav_bar = QHBoxLayout()
        nav_widget = QWidget()
        nav_widget.setStyleSheet("background-color: #3a3a74;")
        nav_widget.setLayout(nav_bar)
        main_layout.addWidget(nav_widget)

      
        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)

        # Ajouter les pages au QStackedWidget
        self.page_accueil = PageAccueil()
        self.page_maps = PageMaps()
        self.page_statistiques = DiagrammesFacteursRisque()
        self.page_contact = PageContact()
        self.page_ressources = MainWindow1()

        self.pages.addWidget(self.page_accueil)
        self.pages.addWidget(self.page_maps)
        self.pages.addWidget(self.page_statistiques)
        self.pages.addWidget(self.page_contact)
        self.pages.addWidget(self.page_ressources)

        # Boutons de navigation
        self.buttons = []
        self.active_button = None

        # Configuration des boutons
        buttons = [
            ("Accueil", self.show_page_accueil),
            ("Maps", self.show_page_maps),
            ("Visualisation graphique", self.show_page_statistiques),
            ("Ressources", self.show_page_ressources),
            ("Contact", self.show_page_contact),
            
        ]

        for label, callback in buttons:
            btn = QPushButton(label)
            btn.setStyleSheet("font-family: Poppins; font-size: 24px; color: white; background-color: #3a3a74; border: none; font-weight: 900;")
            btn.clicked.connect(callback)
            nav_bar.addWidget(btn)
            self.buttons.append(btn)

       
        self.show_page_accueil()

    
    def show_page_accueil(self):
        self.change_page(self.page_accueil, self.buttons[0])

    def show_page_maps(self):
        self.change_page(self.page_maps, self.buttons[1])

    def show_page_statistiques(self):
        self.change_page(self.page_statistiques, self.buttons[2])

    def show_page_ressources(self):
        self.change_page(self.page_ressources, self.buttons[3])

    def show_page_contact(self):
        self.change_page(self.page_contact, self.buttons[4])


    def change_page(self, page, button):
        self.pages.setCurrentWidget(page)
        if self.active_button:
            self.active_button.setStyleSheet(
                "font-family: Poppins; font-size: 24px; color: white; background-color: #3a3a74; border: none; font-weight: 900;"
            )
        button.setStyleSheet(
            "font-family: Poppins; font-size: 24px; color: #3a3a74; background-color: white; border: 1px solid #3a3a74; font-weight: 900;"
        )
        self.active_button = button


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

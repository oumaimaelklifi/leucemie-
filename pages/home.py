from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class PageAccueil(QWidget):
    def __init__(self, parent=None):
        super(PageAccueil, self).__init__(parent)

        # Layout principal vertical
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)  
        layout_principal.setSpacing(20)
        self.setLayout(layout_principal)

        # Layout pour le contenu principal
        layout_contenu = QHBoxLayout()
        layout_contenu.setAlignment(Qt.AlignCenter)  

        # Texte d'introduction
        texte = QLabel(
            "La leucémie est un type de cancer qui affecte le sang et la moelle osseuse, où sont produits les cellules sanguines. "
            "Elle se caractérise par une production anormale et incontrôlée de globules blancs immatures ou anormaux, appelés blastes. "
            "Ces cellules anormales empêchent les cellules sanguines normales de fonctionner correctement....\n"
        )
        texte.setWordWrap(True)
        texte.setAlignment(Qt.AlignCenter)  
        texte.setStyleSheet("font-family: Poppins; font-size: 25px; color: #333; font-weight:600;")
        layout_contenu.addWidget(texte)

        # Affichage de l'image
        try:
            image = QLabel()
            pixmap = QPixmap("assets/1.png")
            image.setPixmap(pixmap.scaled(750, 750, Qt.KeepAspectRatio))  
            layout_contenu.addWidget(image, alignment=Qt.AlignRight | Qt.AlignVCenter)
        except Exception as e:
            layout_contenu.addWidget(QLabel("Image non trouvée."))

        # Ajouter le contenu principal au layout principal
        layout_principal.addLayout(layout_contenu)

        # Ajouter un espace entre le contenu et la barre de navigation
        spacer1 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_principal.addItem(spacer1)

        # Navigation bar
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(00, 20, 20, 20)

        nav_buttons = [
            ("CANCER TODAY", "#ffa500"),
            ("CANCER OVER TIME", "#007bff"),
            ("CANCER TOMORROW", "#007bff"),
            ("CANCER CAUSES", "#ff66b2"),
            ("CANCER SURVIVAL", "#ff66b2"),
            ("CANCER @CSU", "#b8d9ff"),
        ]

        # Ajout des boutons de navigation avec des actions (ou juste un exemple ici)
        for text, color in nav_buttons:
            button = QPushButton(text)
            button.setStyleSheet(f"""
                background-color: {color}; color: white; font-size: 17px; 
                font-family: Poppins; font-weight: bold; padding: 10px 20px; border-radius: 10px;font-weight:900
            """)
            # Associer une action ou une fonctionnalité (ajoutez la fonction connect ici)
            nav_layout.addWidget(button)

        layout_principal.addLayout(nav_layout)

       
        spacer2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_principal.addItem(spacer2)

  
        footer = QLabel("© 2024 Leucémie au Maroc. Tous droits réservés.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-family: Roboto; font-size: 23px; font-weight: bold; color: white; background-color:  #3a3a74;")
        footer.setFixedHeight(50)
        layout_principal.addWidget(footer)


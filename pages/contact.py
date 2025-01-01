from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout
)
from PyQt5.QtCore import Qt

class PageContact(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 70, 20, 20)
        layout_principal.setSpacing(20)
        self.setLayout(layout_principal)

        # Titre de la page
        label_titre = QLabel("Contactez-nous")
        label_titre.setAlignment(Qt.AlignCenter)
        label_titre.setStyleSheet("font-family: Poppins; font-size: 30px; font-weight: bold; color: #8B0000; font-weight:900")
        layout_principal.addWidget(label_titre)

        # Description
        label_description = QLabel("Pour toute question ou information supplémentaire, n'hésitez pas à nous contacter via les moyens ci-dessous.")
        label_description.setAlignment(Qt.AlignCenter)
        label_description.setStyleSheet("font-family: Poppins; font-size: 25px; color: black;font-weight:900")
        layout_principal.addWidget(label_description)

        # Informations de contact
        layout_contact = QVBoxLayout()
        layout_contact.setAlignment(Qt.AlignCenter)

        label_email = QLabel("📧 Email : contact@leucemie-maroc.com")
        label_email.setStyleSheet("font-family: Poppins; font-size: 20px; color: #333;font-weight:900")
        layout_contact.addWidget(label_email)

        label_telephone = QLabel("📞 Téléphone : +212 5 00 00 00 00")
        label_telephone.setStyleSheet("font-family: Poppins; font-size: 20px; color: #333;font-weight:900")
        layout_contact.addWidget(label_telephone)

        label_adresse = QLabel("📍 Adresse : 123 Fstt, Tanger, Maroc")
        label_adresse.setStyleSheet("font-family: Poppins; font-size: 21px; color: #333;font-weight:900")
        layout_contact.addWidget(label_adresse)

        layout_principal.addLayout(layout_contact)


        spacer = QSpacerItem(7, 4)
        layout_principal.addItem(spacer)


        label_message = QLabel("Laissez-nous un message :")
        label_message.setAlignment(Qt.AlignCenter)
        label_message.setStyleSheet("font-family: Poppins; font-size: 26px; font-weight: bold; color: #8B0000;font-weight:900")
        layout_principal.addWidget(label_message)
        layout_message = QVBoxLayout()
        layout_message.setAlignment(Qt.AlignCenter)

        entry_message = QTextEdit()
        entry_message.setPlaceholderText("Écrivez votre message ici...")
        entry_message.setFixedWidth(500)
        entry_message.setFixedHeight(200)
        entry_message.setFontFamily("Poppins")
        layout_message.addWidget(entry_message)

        spacer_message = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_message.addItem(spacer_message)

        layout_bouton = QHBoxLayout()
        layout_bouton.setAlignment(Qt.AlignCenter) 

        bouton_envoyer = QPushButton("Envoyer")
        bouton_envoyer.setStyleSheet("font-family: Poppins; font-size: 20px; background-color: #8B0000; color: white; padding: 10px; border-radius: 5px;font-weight:900")
        bouton_envoyer.setFixedWidth(190)
        
        layout_bouton.addWidget(bouton_envoyer)

    
        layout_message.addLayout(layout_bouton)

     
        layout_principal.addLayout(layout_message)

      
        spacer2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_principal.addItem(spacer2)

        # Footer
        footer = QLabel("© 2024 Leucémie au Maroc. Tous droits réservés.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-family: Roboto; font-size: 23px; font-weight: bold; color: white; background-color:  #3a3a74;")
        footer.setFixedHeight(50)
        layout_principal.addWidget(footer)

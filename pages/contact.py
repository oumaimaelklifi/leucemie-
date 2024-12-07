import tkinter as tk

def afficher_page_contact(frame_contenu, bouton):
    # Nettoyer le contenu existant
    for widget in frame_contenu.winfo_children():
        widget.destroy()
    
    # Contenu de la page de contact
    frame_contact = tk.Frame(frame_contenu, )
    frame_contact.pack(fill=tk.BOTH, expand=True)
    
    # Titre de la page
    label_titre = tk.Label(frame_contact, text="Contactez-nous",
                           font=("Poppins", 20, "bold"), fg="#8B0000", )
    label_titre.pack(pady=20)
    
 
    label_description = tk.Label(frame_contact,
                                  text="Pour toute question ou information supplémentaire, n'hésitez pas à nous contacter via les moyens ci-dessous.",
                                  font=("Poppins", 14), fg="black", justify="center")
    label_description.pack(pady=10)
    
    # Informations de contact
    label_email = tk.Label(frame_contact, text=" 📧 Email : contact@leucemie-maroc.com",
                           font=("Poppins", 12), fg="#333", )
    label_email.pack(pady=5)
    
    label_telephone = tk.Label(frame_contact, text="📞 Téléphone : +212 5 00 00 00 00",
                               font=("Poppins", 13), fg="#333", )
    label_telephone.pack(pady=5)
    
    label_adresse = tk.Label(frame_contact, text="📍 Adresse : 123 Fstt, Tanger, Maroc",
                             font=("Poppins", 12), fg="#333", )
    label_adresse.pack(pady=5)
    
 
    label_message = tk.Label(frame_contact, text="Laissez-nous un message :",
                             font=("Poppins", 17, "bold"), fg="#8B0000", )
    label_message.pack(pady=15)
    
    entry_message = tk.Text(frame_contact, width=50, height=5, font=("Poppins", 12), bd=2, relief="solid")
    entry_message.pack(pady=10)
    
    bouton_envoyer = tk.Button(frame_contact, text="Envoyer", font=("Poppins", 14), bg="#8B0000", fg="white", bd=0,
                               command=lambda: print("Message envoyé"))
    bouton_envoyer.pack(pady=10)
    
  


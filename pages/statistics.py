# import sys
# import pandas as pd
# import matplotlib.pyplot as plt
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QAction, QMenuBar
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# class PageStatistiques(QWidget):
#     def __init__(self, title, data, labels, chart_type='bar', parent=None):
#         super(PageStatistiques, self).__init__(parent)
        
#         # Créer un canvas pour afficher le graphique
#         fig = plt.figure()
#         ax = fig.add_subplot(111)
        
#         if chart_type == 'pie':
#             ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
#             ax.set_title(title)
#         elif chart_type == 'bar':
#             ax.bar(labels, data)
#             ax.set_title(title)
#             ax.set_xlabel('Catégories')
#             ax.set_ylabel('Fréquence')
#         elif chart_type == 'stacked_bar':
#             # Diagramme en barres empilées pour deux variables
#             data.plot(kind='bar', stacked=True, ax=ax)
#             ax.set_title(title)
#             ax.set_xlabel('Catégories')
#             ax.set_ylabel('Fréquence')

#         canvas = FigureCanvas(fig)
        
#         # Layout pour afficher le canvas
#         layout = QVBoxLayout(self)
#         layout.addWidget(canvas)
#         self.setLayout(layout)


# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Initialiser l'interface
#         self.setWindowTitle('Diagrammes Statistiques')
#         self.setGeometry(100, 100, 800, 600)

#         # Créer un QStackedWidget pour afficher différentes pages
#         self.stacked_widget = QStackedWidget()
#         central_widget = QWidget(self)
#         central_layout = QVBoxLayout(central_widget)
#         central_layout.addWidget(self.stacked_widget)
#         self.setCentralWidget(central_widget)

#         # Charger les données du fichier Excel spécifique
#         self.data = pd.read_excel('patients_data_rabat.xlsx')  # Remplacez par votre chemin de fichier
#         print(self.data.head())  # Afficher les premières lignes pour vérifier le chargement

#         # Créer les pages pour chaque graphique
#         self.create_pages()

#         # Créer un menu de navigation
#         self.create_navigation()

#     def create_pages(self):
#         # Créer chaque page pour les différents diagrammes

#         # Répartition par sexe (diagramme circulaire)
#         sex_counts = self.data['Sexe'].value_counts()
#         sex_page = PageStatistiques('Répartition par Sexe', sex_counts, sex_counts.index, chart_type='pie')
#         self.stacked_widget.addWidget(sex_page)

#         # Répartition par type de leucémie (diagramme circulaire)
#         leucemie_counts = self.data['Type de leucémie'].value_counts()
#         leucemie_page = PageStatistiques('Répartition par Type de Leucémie', leucemie_counts, leucemie_counts.index, chart_type='pie')
#         self.stacked_widget.addWidget(leucemie_page)

#         # Répartition par groupe d'âge (diagramme en barres)
#         age_counts = self.data['Groupe d\'âge'].value_counts()
#         age_page = PageStatistiques('Répartition par Groupe d\'Âge', age_counts, age_counts.index, chart_type='bar')
#         self.stacked_widget.addWidget(age_page)

#         # Répartition par tabagisme (diagramme en barres)
#         tabagisme_counts = self.data['Tabagisme'].value_counts()
#         tabagisme_page = PageStatistiques('Répartition par Tabagisme', tabagisme_counts, tabagisme_counts.index, chart_type='bar')
#         self.stacked_widget.addWidget(tabagisme_page)

#         # Répartition par sexe et tabagisme (diagramme en barres empilées)
#         sexe_tabagisme_counts = pd.crosstab(self.data['Sexe'], self.data['Tabagisme'])
#         sexe_tabagisme_page = PageStatistiques('Répartition par Sexe et Tabagisme', sexe_tabagisme_counts, sexe_tabagisme_counts.columns, chart_type='stacked_bar')
#         self.stacked_widget.addWidget(sexe_tabagisme_page)

#     def create_navigation(self):
#         # Créer une barre de menu avec des actions pour chaque page
#         menubar = self.menuBar()  # Utilisation correcte de menuBar() ici
#         view_menu = menubar.addMenu('Voir')

#         sex_action = QAction('Répartition par Sexe', self)
#         sex_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
#         view_menu.addAction(sex_action)

#         leucemie_action = QAction('Répartition par Type de Leucémie', self)
#         leucemie_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(1))
#         view_menu.addAction(leucemie_action)

#         age_action = QAction('Répartition par Groupe d\'Âge', self)
#         age_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(2))
#         view_menu.addAction(age_action)

#         tabagisme_action = QAction('Répartition par Tabagisme', self)
#         tabagisme_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(3))
#         view_menu.addAction(tabagisme_action)

#         sexe_tabagisme_action = QAction('Répartition par Sexe et Tabagisme', self)
#         sexe_tabagisme_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(4))
#         view_menu.addAction(sexe_tabagisme_action)



## fichier : interface.py
import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTabWidget, QWidget, QLabel,
    QScrollArea, QComboBox, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

## fichier : diagrammes.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class BaseDiagram:
    """Classe de base pour les diagrammes."""
    def __init__(self, data):
        self.data = data

    def create_figure(self):
        raise NotImplementedError("Cette méthode doit être implémentée par les sous-classes.")

class SexeDiagram(BaseDiagram):
    def create_figure(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        self.data["Sexe"].value_counts().plot.pie(
            ax=ax, autopct="%1.1f%%", startangle=90, colors=["blue", "pink"]
        )
        ax.set_title("Répartition par sexe")
        ax.set_ylabel("")
        fig.tight_layout()
        return fig

class AgeDiagram(BaseDiagram):
    def create_figure(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x=self.data["Groupe d'âge"].value_counts().index,
            y=self.data["Groupe d'âge"].value_counts().values,
            palette="viridis",
            ax=ax
        )
        ax.set_title("Distribution des groupes d'âge")
        ax.set_xlabel("Groupe d'âge")
        ax.set_ylabel("Nombre de patients")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        return fig

class EnvironnementDiagram(BaseDiagram):
    def create_figure(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        self.data["Environnement"].value_counts().plot.pie(
            ax=ax, autopct="%1.1f%%", startangle=90, colors=["green", "orange"]
        )
        ax.set_title("Répartition par environnement")
        ax.set_ylabel("")
        fig.tight_layout()
        return fig

class TypeLeucemieDiagram(BaseDiagram):
    def create_figure(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x=self.data["Type de leucémie"].value_counts().index,
            y=self.data["Type de leucémie"].value_counts().values,
            palette="coolwarm",
            ax=ax
        )
        ax.set_title("Distribution des types de leucémie")
        ax.set_xlabel("Type de leucémie")
        ax.set_ylabel("Nombre de patients")
        fig.tight_layout()
        return fig

class TabagismeDiagram(BaseDiagram):
    def create_figure(self):
        # Diagramme général de tabagisme
        fig, axs = plt.subplots(3, 1, figsize=(12, 18))

        # Diagramme 1 : Répartition générale
        self.data["Tabagisme"].value_counts().plot.pie(
            ax=axs[0], autopct="%1.1f%%", startangle=90, colors=["grey", "purple"]
        )
        axs[0].set_title("Tabagisme")
        axs[0].set_ylabel("")

        # Diagramme 2 : Tabagisme par sexe
        sns.countplot(
            x="Sexe", hue="Tabagisme", data=self.data, palette="Set2", ax=axs[1]
        )
        axs[1].set_title("Tabagisme par sexe")
        axs[1].set_xlabel("Sexe")
        axs[1].set_ylabel("Nombre de patients")

        # Diagramme 3 : Tabagisme par groupe d'âge
        sns.countplot(
            x="Groupe d'âge", hue="Tabagisme", data=self.data, palette="cool", ax=axs[2]
        )
        axs[2].set_title("Tabagisme par groupe d'âge")
        axs[2].set_xlabel("Groupe d'âge")
        axs[2].set_ylabel("Nombre de patients")
        axs[2].tick_params(axis='x', rotation=45)

        fig.tight_layout()
        return fig

class GenetiqueDiagram(BaseDiagram):
    def create_figure(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        self.data["Facteur génétique"].value_counts().plot.pie(
            ax=ax, autopct="%1.1f%%", startangle=90, colors=["cyan", "magenta"]
        )
        ax.set_title("Présence d'un facteur génétique")
        ax.set_ylabel("")
        fig.tight_layout()
        return fig

# Charger les données
data_path = 'PatientsCasa.csv'

try:
    data = pd.read_csv(data_path)
    print("Données chargées avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement des données : {e}")
    data = None

class DiagrammesFacteursRisque(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagrammes des Facteurs de Risque")
        self.setGeometry(100, 100, 1200, 800)

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Barre de filtres
        self.filtre_layout = QHBoxLayout()
        self.main_layout.addLayout(self.filtre_layout)

        self.zone_label = QLabel("Filtrer par zone :")
        self.filtre_layout.addWidget(self.zone_label)

        self.zone_combobox = QComboBox()
        self.zone_combobox.addItems(["Toutes", "Casa"])
        self.zone_combobox.currentTextChanged.connect(self.appliquer_filtre)
        self.filtre_layout.addWidget(self.zone_combobox)

        # Zone de défilement principale
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        # Onglets pour les diagrammes
        self.tabs = QTabWidget()
        self.scroll_layout.addWidget(self.tabs)

        if data is not None:
            self.creer_onglets()
        else:
            self.message_erreur = QLabel("Erreur : Les données n'ont pas été chargées correctement.")
            self.scroll_layout.addWidget(self.message_erreur)

    def creer_onglets(self):
        self.diagram_classes = [
            SexeDiagram, AgeDiagram, EnvironnementDiagram, TypeLeucemieDiagram,
            TabagismeDiagram, GenetiqueDiagram
        ]

        for diagram_class in self.diagram_classes:
            diagram_instance = diagram_class(data)
            self.creer_onglet(diagram_instance)

    def creer_onglet(self, diagram_instance):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        figure = diagram_instance.create_figure()
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)

        self.tabs.addTab(tab, diagram_instance.__class__.__name__.replace("Diagram", ""))

    def appliquer_filtre(self, texte):
        print(f"Filtre appliqué : {texte}")  

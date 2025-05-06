# -*- coding: utf-8 -*-
# Importation des modules nécessaires
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from tkinter import *
import os
import pygame

from courbes import generer_pourcentage_augmentation, application_variation
from utils import Entreprise, Portefeuille, afficher_info_inutile
from sauvegardes import sauvegarder_partie, charger_partie, supprimer_sauvegarde, lister_sauvegardes
from musique import jouer_musiques

# conctantes
LARGE_FONT = ("Verdana", 12)

# Variables globales de configuration
config = {
    "theme": "clair",
    "style_courbe": "ligne",
    "couleurs": {}  # Nom de l'entreprise -> couleur choisie
}

DOSSIER_SAUVEGARDES = "saves"
os.makedirs(DOSSIER_SAUVEGARDES, exist_ok=True)

portefeuille = Portefeuille()



# Création de la classe ecran pour l'interface utilisateur
class Ecran(tk.Tk):
    """Classe principale de l'interface utilisateur."""
    def __init__(self, entreprises : list =None, *args, **kwargs) -> None:
        """Initialise l'interface utilisateur avec les entreprises et le portefeuille."""
        if entreprises is None:
            entreprises = []  # Liste d'entreprises par défaut si aucune n'est fournie
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="icon.ico")  # Remplacer ou enlever si nécessaire
        tk.Tk.wm_title(self, "jeu de bourse")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageTwo, PageThree, PageOne):
            if F == PageThree or F == PageTwo:
                frame = F(container, self, entreprises, portefeuille)
            elif F == PageOne:
                frame = F(container, self, entreprises, portefeuille, self.frames)
            else:
                frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TButton", 
                        font=("Helvetica", 12),
                        padding=6,
                        relief="flat",
                        background="#3498db",
                        foreground="Black",
                        bordercolor="#2980b9",
                        highlightthickness=0,
                        highlightbackground="#2980b9",
                        highlightcolor="#2980b9",
                        focuscolor="#2980b9",)
        style.configure("TButton", background="#3498db")  # Ensure base TButton style is set
        style.map("TButton",
                  background=[("active", "#2980b9"), ("pressed", "#2980b9")],
                    foreground=[("active", "white"), ("pressed", "white")],
                    bordercolor=[("active", "#2980b9"), ("pressed", "#2980b9")],
                    relief=[("active", "flat"), ("pressed", "flat")])

        self.show_frame(StartPage)


    def show_frame(self, cont : str) -> None:
        """Affiche le cadre de la page spécifiée."""
        frame = self.frames[cont]
        frame.tkraise()
    
    def appliquer_theme(self) -> None:
        """Applique le thème sombre ou clair à l'interface."""
        couleur_fond = "black" if config["theme"] == "sombre" else "white"
        for frame in self.frames.values():
            frame.configure(bg=couleur_fond)
            for widget in frame.winfo_children():
                try:
                    widget.configure(bg=couleur_fond, fg="white" if config["theme"] == "sombre" else "black")
                except:
                    pass  # certains widgets n'ont pas bg/fg





class StartPage(tk.Frame):
    """Page d'accueil de l'interface utilisateur."""
    def __init__(self, parent : object, controller : object = None) -> None:
        """Initialise la page d'accueil."""
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=("Helvetica", 20, "bold"), fg="#2e86de")
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            style="custom.TButton",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                             command=lambda: controller.show_frame(PageTwo),
                             style="TButton")
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                             command=lambda: controller.show_frame(PageThree),
                             style="TButton")
        button3.pack()


class PageOne(tk.Frame):
    """Page pour la sauvegarde et le chargement des parties."""
    def __init__(self, parent : object, controller : object, entreprises : list, portefeuille : object, frames : dict) -> None:
        """Initialise la page."""
        global config
        self.entreprises = entreprises
        self.portefeuille = portefeuille
        self.frames = frames
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.controller = controller

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage),
                             style="TButton")
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                             command=lambda: controller.show_frame(PageTwo),
                             style="TButton")
        button2.pack()

        button3 = tk.Button(self, text="💾 Sauvegarder", width='18', borderwidth=2,  background="gray",relief=RAISED,command=lambda: self.popup_sauvegarde())
        button3.pack(pady=10, padx=10)

        menuCharger = Menubutton(self, text='📂 Charger', width='20', borderwidth=2, bg='gray', activebackground='darkorange',relief = RAISED)
        # Création d'un menu défilant
        menuDeroulant1 = Menu(menuCharger)
        for nom in lister_sauvegardes():
            menuDeroulant1.add_command(label=nom, command=lambda nom=nom: self.charger_partie_utilisateur(nom))

        # Attribution du menu déroulant au menu Affichage
        menuCharger.configure(menu=menuDeroulant1)
        menuCharger.pack(pady=10, padx=10)

        menuSupprimer = Menubutton(self, text='🗑️ Supprimer', width='20', borderwidth=2, bg='gray', activebackground='darkred', activeforeground='white', relief=RAISED)
        # Création d'un menu défilant
        menuDeroulant2 = Menu(menuSupprimer)
        for nom in lister_sauvegardes():
            menuDeroulant2.add_command(label=nom, command=lambda nom=nom: supprimer_sauvegarde(nom))

        # Attribution du menu déroulant au menu Affichage
        menuSupprimer.configure(menu=menuDeroulant2)
        menuSupprimer.pack(pady=10, padx=10)
        

    def sauvegarder_partie_utilisateur(self, nom : str) -> None:
        """Sauvegarde l'état du jeu dans un fichier JSON."""
        global config
        dico_entreprises = {}
        joueur = {
            "argent": self.portefeuille.get_argent(),
            "portefeuille": self.portefeuille.get_actions()
        }
        for i in range(len(self.entreprises)):
            dico_entreprises[self.entreprises[i].get_nom()] = self.entreprises[i].get_historique()
        parametres = config

        sauvegarder_partie(nom, joueur, dico_entreprises, parametres)
        print(f"✅ Partie '{nom}' sauvegardée !")


    def charger_partie_utilisateur(self, nom : str) -> None:
        """Charge une partie sauvegardée à partir du fichier JSON."""
        donnees = charger_partie(nom)
        if not donnees:
            print(f"❌ Sauvegarde '{nom}' introuvable.")
            return

        # 1) Met à jour tes objets métier
        self.portefeuille.modifier_argent(donnees["joueur"]["argent"])
        self.portefeuille.modifier_actions(donnees["joueur"]["portefeuille"])

        # Reconstruis tes entreprises à partir du format sauvegardé
        nouvelles = []
        for nom_e, histo in donnees["entreprises"].items():
            e = Entreprise(nom_e, histo["valeurs"][-1])
            # on remplit le nouvel historique dict {debut, valeurs}
            e.historique = { "debut": histo["debut"], "valeurs": histo["valeurs"][:] }
            nouvelles.append(e)
        self.entreprises[:] = nouvelles  # remplace la liste en place

        # 2) Mets la config à jour
        global config
        config = donnees["parametres"]

        # 3) recharger la PageThree
        page3 = self.controller.frames[PageThree]
        page3.load_data(self.entreprises, self.portefeuille)

        # 4) Enfin, affiche la page 3
        self.controller.show_frame(PageThree)
        print(f"✅ Partie '{nom}' chargée avec succès.")
    
    def popup_sauvegarde(self) -> None:
        """Crée une fenêtre popup pour la sauvegarde."""
        def nomination() -> None:
            """Fonction pour valider le nom de la sauvegarde."""
            nom = my_entry.get()
            if nom:
                self.sauvegarder_partie_utilisateur(nom)
                popup.destroy()
            else:
                label.config(text="Nom de sauvegarde invalide !", fg="red")
            popup.destroy
        # Crée une fenêtre popup pour la sauvegarde
        popup = tk.Toplevel(self)
        popup.title("Sauvegarde")
        label = tk.Label(popup)
        label.pack(pady=0, padx=0)
        my_entry = Entry(popup)
        my_entry.pack()
        button1 = ttk.Button(popup, text="Annuler", command=popup.destroy)
        button1.pack(pady=5)
        button2 = ttk.Button(popup, text="Sauvegarder", command=nomination)
        button2.pack(pady=5)
        popup.transient(self)  # Set the popup as a transient window of the main window
    

        



class PageTwo(tk.Frame):
    """Page pour les paramètres de l'interface utilisateur."""
    def __init__(self, parent, controller, entreprises, portefeuille) -> None:
        """Initialise la page des paramètres."""
        self.entreprises = entreprises
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Paramètres", font=("Helvetica", 20, "bold"))
        label.pack(pady=10)

        # Bouton thème sombre
        self.bouton_theme = tk.Button(self, text="Activer Thème Sombre" , width='18', borderwidth=2,  background="gray",relief=RAISED, command=self.basculer_theme)
        self.bouton_theme.pack(pady=30)

        menuMusique = Menubutton(self, text='🎵 Muse ique', width='20', borderwidth=2, bg='gray', activebackground='darkred', activeforeground='white', relief=RAISED)
        # Création d'un menu défilant
        menuDeroulant = Menu(menuMusique)
        musique_dossier = r'Muse'
        musique_fichiers = [os.path.join(musique_dossier, f) for f in os.listdir(musique_dossier) if f.endswith('.mp3')]
        for nom in musique_fichiers:
            menuDeroulant.add_command(label=nom, command=lambda nom=nom:jouer_musiques(nom))

        # Attribution du menu déroulant au menu Musique
        menuMusique.configure(menu=menuDeroulant)
        menuMusique.pack(pady=10, padx=10)

        bouton_arreter_musique = tk.Button(self, text="⏸️ Pause", width='18', borderwidth=2, background="gray", relief=RAISED, command=lambda: pygame.mixer.music.pause())
        bouton_arreter_musique.pack(pady=5)
        bouton_continuer_musique = tk.Button(self, text="▶️ Reprendre", width='18', borderwidth=2, background="gray", relief=RAISED, command=lambda: pygame.mixer.music.unpause())
        bouton_continuer_musique.pack(pady=5)

        # Gestion du volume
        label_volume = tk.Label(self, text="Volume :", font=("Helvetica", 12))
        label_volume.pack(pady=5)

        self.volume_var = tk.DoubleVar(value=0.5)  # Valeur initiale du volume (50%)
        scale_volume = tk.Scale(self, from_=0, to=1, resolution=0.01, orient="horizontal",
                    variable=self.volume_var, command=self.ajuster_volume)
        scale_volume.pack(pady=5)


        # Boutons de navigation
        bouton_retour = ttk.Button(self, text="Retour Accueil",
                                   command=lambda: controller.show_frame(StartPage))
        bouton_retour.pack(pady=10)

        self.controller = controller

    def basculer_theme(self) -> None:
        """Bascule entre le thème clair et sombre."""
        if config["theme"] == "clair":
            config["theme"] = "sombre"
            self.bouton_theme.config(text="Activer Thème Clair")
            self.controller.appliquer_theme()
        else:
            config["theme"] = "clair"
            self.bouton_theme.config(text="Activer Thème Sombre")
            self.master.configure(bg="white")
            self.configure(bg="white")
            self.controller.appliquer_theme()

    def valider_style(self) -> None:
        """Valide le style de courbe choisi."""
        config["style_courbe"] = self.style_var.get()
        print("Style de courbe sélectionné :", config["style_courbe"])

    def valider_couleurs(self) -> None:
        """Valide les couleurs choisies pour les entreprises."""
        for nom, var in self.couleur_vars.items():
            config["couleurs"][nom] = var.get()
        print("Couleurs choisies :", config["couleurs"])

    def ajuster_volume(self, volume : float) -> None:
        """Ajuste le volume de la musique."""
        pygame.mixer.music.set_volume(float(volume))



class PageThree(tk.Frame):
    """Page pour afficher le graphique des entreprises."""
    def __init__(self, parent, controller, entreprises, portefeuille) -> None:
        """Initialise la page du graphique."""
        self.portefeuille = portefeuille
        tk.Frame.__init__(self, parent)
        self.entreprises = entreprises
        
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage),
                             style="TButton")
        button1.pack()

        # --- Nouveau : frame global pour séparer graphique et infos ---
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Frame pour le graphique
        graph_frame = tk.Frame(main_frame)
        graph_frame.pack(side="left", fill="both", expand=True)

        # Frame pour les infos des entreprises
        self.info_frame = tk.Frame(main_frame, bg="white", padx=10)
        self.info_frame.pack(side="right", fill="y")

        # --- Partie graphique ---
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)

        self.a.clear()  # Efface pour redessiner proprement
        self.lines = {}
        for e in entreprises:
            histo = e.get_historique()
            jours = list(range(histo["debut"], histo["debut"] + len(histo["valeurs"])))
            valeurs = histo["valeurs"]
            couleur = config["couleurs"].get(e.get_nom(), None)
            style = '-' if config["style_courbe"] == "ligne" else 'o'
            line, = self.a.plot(jours, valeurs, style, label=e.get_nom(), color=couleur)
            self.lines[e.get_nom()] = line


        self.a.set_title("Évolution des prix des actions")
        self.a.set_xlabel("Temps")
        self.a.set_ylabel("Prix (€)")
        self.a.legend()
        self.a.grid(True)
            

        self.a.set_title("Évolution des prix des actions")
        self.a.set_xlabel("Temps")
        self.a.set_ylabel("Prix (€)")
        self.a.legend()
        self.a.grid(True)

        self.canvas = FigureCanvasTkAgg(self.f, graph_frame)

        self.label_portefeuille = tk.Label(self.info_frame, text=self.portefeuille.get_resume(), font=("Helvetica", 10), justify="left")
        self.label_portefeuille.pack(pady=10)

        self.boutons_entreprises = {}

        self.entreprise_labels = {}
        for e in entreprises:
            cadre = tk.Frame(self.info_frame)
            cadre.pack(pady=5)

            label = tk.Label(cadre, text=e.get_nom(), font=("Helvetica", 12))
            label.pack(side=tk.LEFT)

            lbl = tk.Label(self.info_frame, text="", font=("Helvetica", 12), anchor="w", bg="white")
            lbl.pack(fill="x", pady=2)
            self.entreprise_labels[e.get_nom()] = lbl

            bouton_acheter = ttk.Button(cadre, text="Acheter", command=lambda e=e: self.acheter_action(e))
            bouton_acheter.pack(side=tk.LEFT, padx=2)

            bouton_vendre = ttk.Button(cadre, text="Vendre", command=lambda e=e: self.vendre_action(e))
            bouton_vendre.pack(side=tk.LEFT, padx=2)

            self.boutons_entreprises[e.get_nom()] = (bouton_acheter, bouton_vendre)


        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar(self.canvas, graph_frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.mettre_a_jour_graphique()
        
        self.label_info = tk.Label(self, text="", font=("Arial", 10), fg="gray")
        self.label_info.pack(side="bottom", pady=5)
        self.mettre_a_jour_info()
        




    def mettre_a_jour_info(self):
        afficher_info_inutile(self.label_info)
        self.after(20000, self.mettre_a_jour_info)
        

    def acheter_action(self, entreprise : object) -> None:
        """Acheter une action de l'entreprise spécifiée."""
        if self.portefeuille.acheter(entreprise, 1):
            self.update_portefeuille()
        else:
            print("Pas assez d'argent pour acheter.")

    def vendre_action(self, entreprise : object) -> None:
        """Vendre une action de l'entreprise spécifiée."""
        if self.portefeuille.vendre(entreprise, 1):
            self.update_portefeuille()
        else:
            print("Pas assez d'actions pour vendre.")

    def update_portefeuille(self) -> None:
        """Met à jour l'affichage du portefeuille."""
        self.label_portefeuille.config(text=self.portefeuille.get_resume())


    def mettre_a_jour_graphique(self) -> None:
        """Met à jour le graphique et les informations affichées."""
        # Pour éviter d'empiler les appels
        if hasattr(self, "_after_id"):
            self.after_cancel(self._after_id)

        # Met à jour la variation des entreprises
        for e in self.entreprises:
            pourcentage = generer_pourcentage_augmentation(e.get_valeur(), e.get_variation())
            valeur, variation = application_variation(e.get_valeur(), pourcentage)
            e.update(valeur, variation)

        # Met à jour les courbes existantes
        for e in self.entreprises:
            ligne = self.lines[e.get_nom()]
            histo = e.get_historique()
            jours = list(range(histo["debut"], histo["debut"] + len(histo["valeurs"])))
            valeurs = histo["valeurs"]
            ligne.set_xdata(jours)
            ligne.set_ydata(valeurs)


        # Ajuste les limites du graphique
        self.a.relim()
        self.a.autoscale_view()

        # Redessine le graphique
        self.canvas.draw()

        # --- Mettre à jour les infos affichées ---
        for e in self.entreprises:
            valeur = e.get_valeur()
            variation = e.get_variation()
            self.entreprise_labels[e.get_nom()].config(
                text=f"{e.get_nom()} : {valeur:.2f} € ({variation:+.2f}%)"
            )

        # Appelle cette fonction toutes les 1000 ms (1 seconde)
        self.after(1000, self.mettre_a_jour_graphique)

    def load_data(self, entreprises : list, portefeuille : object) -> None:
        """Charge les données des entreprises et du portefeuille dans le graphique."""
        # Stoppe les mises à jour précédentes
        self.after_cancel(self._after_id) if hasattr(self, "_after_id") else None

        # Nettoyer le graphique et l'affichage
        self.a.clear()
        self.canvas.draw()

        # Après avoir tout supprimé
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # <-- Ajoute ceci pour recréer le label de l'argent
        self.label_portefeuille = tk.Label(self.info_frame, text=self.portefeuille.get_resume(), font=("Helvetica", 10), justify="left")
        self.label_portefeuille.pack(pady=10)


        # Réinitialise les données internes
        self.entreprises = entreprises
        self.portefeuille = portefeuille
        self.lines = {}
        self.entreprise_labels = {}
        self.boutons_entreprises = {}

        # Reconstruire le graphique et les éléments visuels
        for e in entreprises:
            histo = e.get_historique()
            jours = list(range(histo["debut"], histo["debut"] + len(histo["valeurs"])))
            valeurs = histo["valeurs"]
            couleur = config["couleurs"].get(e.get_nom(), None)
            style = '-' if config["style_courbe"] == "ligne" else 'o'
            line, = self.a.plot(jours, valeurs, style, label=e.get_nom(), color=couleur)
            self.lines[e.get_nom()] = line

            cadre = tk.Frame(self.info_frame)
            cadre.pack(pady=5)
            label = tk.Label(cadre, text=e.get_nom(), font=("Helvetica", 12))
            label.pack(side=tk.LEFT)

            lbl = tk.Label(self.info_frame, text="", font=("Helvetica", 12), anchor="w", bg="white")
            lbl.pack(fill="x", pady=2)
            self.entreprise_labels[e.get_nom()] = lbl

            bouton_acheter = ttk.Button(cadre, text="Acheter", command=lambda e=e: self.acheter_action(e))
            bouton_acheter.pack(side=tk.LEFT, padx=2)

            bouton_vendre = ttk.Button(cadre, text="Vendre", command=lambda e=e: self.vendre_action(e))
            bouton_vendre.pack(side=tk.LEFT, padx=2)

            self.boutons_entreprises[e.get_nom()] = (bouton_acheter, bouton_vendre)

        self.a.set_title("Évolution des prix des actions")
        self.a.set_xlabel("Temps")
        self.a.set_ylabel("Prix (€)")
        self.a.legend()
        self.a.grid(True)

        self.canvas.draw()

        # Redémarre les mises à jour
        self._after_id = self.after(1000, self.mettre_a_jour_graphique)
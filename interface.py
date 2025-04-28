#Interface graphique (Tkinter)
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk

from courbes import generer_pourcentage_augmentation, application_variation
from utils import Entreprise, generer_liste_entreprises, Portefeuille

LARGE_FONT = ("Verdana", 12)

# Variables globales de configuration
config = {
    "theme": "clair",
    "style_courbe": "ligne",
    "couleurs": {}  # Nom de l'entreprise -> couleur choisie
}



# Création de la classe ecran pour l'interface utilisateur
class Ecran(tk.Tk):
    def __init__(self, entreprises=None, *args, **kwargs):
        if entreprises is None:
            entreprises = []  # Liste d'entreprises par défaut si aucune n'est fournie
        tk.Tk.__init__(self, *args, **kwargs)

 #       tk.Tk.iconbitmap(self, default="clienticon.ico")  # Remplacer ou enlever si nécessaire
        tk.Tk.wm_title(self, "jeu de bourse")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):
            if F == PageThree or F == PageTwo:
                frame = F(container, self, entreprises)  # Passer la liste d'entreprises à PageThree
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
                        borderwidth=0,
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

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def appliquer_theme(self):
        couleur_fond = "black" if config["theme"] == "sombre" else "white"
        for frame in self.frames.values():
            frame.configure(bg=couleur_fond)
            for widget in frame.winfo_children():
                try:
                    widget.configure(bg=couleur_fond, fg="white" if config["theme"] == "sombre" else "black")
                except:
                    pass  # certains widgets n'ont pas bg/fg


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage),
                             style="TButton")
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                             command=lambda: controller.show_frame(PageTwo),
                             style="TButton")
        button2.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller, entreprises):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Paramètres", font=("Helvetica", 20, "bold"))
        label.pack(pady=10)

        # Bouton thème sombre
        self.bouton_theme = ttk.Button(self, text="Activer Thème Sombre", command=self.basculer_theme)
        self.bouton_theme.pack(pady=5)

        # Sélection du style de courbe
        label_style = tk.Label(self, text="Style de Courbe :", font=("Helvetica", 12))
        label_style.pack(pady=5)

        self.style_var = tk.StringVar(value=config["style_courbe"])
        style_frame = tk.Frame(self)
        style_frame.pack()

        radio_ligne = tk.Radiobutton(style_frame, text="Ligne continue", variable=self.style_var, value="ligne")
        radio_points = tk.Radiobutton(style_frame, text="Points", variable=self.style_var, value="points")
        radio_ligne.pack(side=tk.LEFT, padx=10)
        radio_points.pack(side=tk.LEFT, padx=10)

        bouton_valider_style = ttk.Button(self, text="Valider Style", command=self.valider_style)
        bouton_valider_style.pack(pady=5)

        # Choix des couleurs pour chaque entreprise
        label_couleurs = tk.Label(self, text="Couleur des Entreprises :", font=("Helvetica", 12))
        label_couleurs.pack(pady=5)

        self.couleur_vars = {}
        for e in entreprises:
            frame = tk.Frame(self)
            frame.pack(pady=2)
            label = tk.Label(frame, text=e.get_nom())
            label.pack(side=tk.LEFT)

            couleur_var = tk.StringVar(value=config["couleurs"].get(e.get_nom(), "#000000"))
            self.couleur_vars[e.get_nom()] = couleur_var

            entry = tk.Entry(frame, textvariable=couleur_var, width=10)
            entry.pack(side=tk.LEFT, padx=5)

        bouton_valider_couleurs = ttk.Button(self, text="Valider Couleurs", command=self.valider_couleurs)
        bouton_valider_couleurs.pack(pady=10)

        # Boutons de navigation
        bouton_retour = ttk.Button(self, text="Retour Accueil",
                                   command=lambda: controller.show_frame(StartPage))
        bouton_retour.pack(pady=10)

        self.controller = controller

    def basculer_theme(self):
        if config["theme"] == "clair":
            config["theme"] = "sombre"
            self.bouton_theme.config(text="Activer Thème Clair")
            self.controller.appliquer_theme()
        else:
            config["theme"] = "clair"
            self.bouton_theme.config(text="Activer Thème Sombre")
            self.master.configure(bg="white")
            self.configure(bg="white")

    def valider_style(self):
        config["style_courbe"] = self.style_var.get()
        print("Style de courbe sélectionné :", config["style_courbe"])
        print(config)

    def valider_couleurs(self):
        for nom, var in self.couleur_vars.items():
            config["couleurs"][nom] = var.get()
        print("Couleurs choisies :", config["couleurs"])
        print(config)



class PageThree(tk.Frame):
    def __init__(self, parent, controller, entreprises):
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
            couleur = config["couleurs"].get(e.get_nom(), None)
            style = '-' if config["style_courbe"] == "ligne" else 'o'
            self.a.plot(e.get_historique(), style, label=e.get_nom(), color=couleur)
            self.lines[e.get_nom()] = self.a.lines[-1]

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

        # Création du portefeuille
        self.portefeuille = Portefeuille()

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
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)            

        self.mettre_a_jour_graphique()
    
    def acheter_action(self, entreprise):
        if self.portefeuille.acheter(entreprise, 1):
            self.update_portefeuille()
        else:
            print("Pas assez d'argent pour acheter.")

    def vendre_action(self, entreprise):
        if self.portefeuille.vendre(entreprise, 1):
            self.update_portefeuille()
        else:
            print("Pas assez d'actions pour vendre.")

    def update_portefeuille(self):
        self.label_portefeuille.config(text=self.portefeuille.get_resume())


    def mettre_a_jour_graphique(self):
        # Met à jour la variation des entreprises
        for e in self.entreprises:
            pourcentage = generer_pourcentage_augmentation(e.get_valeur(), e.get_variation())
            valeur, variation = application_variation(e.get_valeur(), pourcentage)
            e.update(valeur, variation)

        # Met à jour les courbes existantes
        for e in self.entreprises:
            ligne = self.lines[e.get_nom()]
            historique = e.get_historique()
            ligne.set_ydata(historique)
            ligne.set_xdata(range(len(historique)))

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
        self.after(1, self.mettre_a_jour_graphique)

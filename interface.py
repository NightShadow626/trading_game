#Interface graphique (Tkinter)
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk

from courbes import generer_pourcentage_augmentation, application_variation
from utils import Entreprise

LARGE_FONT = ("Verdana", 12)





# Supposons que vous avez déjà les données des entreprises et leurs courbes générées dans une variable entreprises.
entreprises = [Entreprise("NovaTech", 12.5),Entreprise("BioCorp", 10),Entreprise("LuxIndustries", 215.0)]

# Création de la classe ecran pour l'interface utilisateur
class Ecran(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

 #       tk.Tk.iconbitmap(self, default="clienticon.ico")  # Remplacer ou enlever si nécessaire
        tk.Tk.wm_title(self, "jeu de bourse")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):
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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage),
                             style="TButton")
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne),
                             style="TButton")
        button2.pack()


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage),
                             style="TButton")
        button1.pack()

        # Création du graphique pour afficher les entreprises
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)

        # Initialisation du graphique
        self.lines = {}
        for e in entreprises:
            line, = self.a.plot(e.get_historique(), label=e.get_nom())
            self.lines[e.get_nom()] = line

        self.a.set_title("Évolution des prix des actions")
        self.a.set_xlabel("Temps")
        self.a.set_ylabel("Prix (€)")
        self.a.legend()
        self.a.grid(True)

        # Affichage du graphique dans la fenêtre Tkinter
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Appel de la méthode pour générer et mettre à jour les variations toutes les secondes
        self.mettre_a_jour_graphique()

    def mettre_a_jour_graphique(self):
        # Met à jour la variation des entreprises
        for e in entreprises:
            pourcentage = generer_pourcentage_augmentation(e.get_valeur(), e.get_variation())
            valeur, variation = application_variation(e.get_valeur(), pourcentage)
            e.update(valeur, variation)

        # Met à jour les courbes existantes
        for e in entreprises:
            ligne = self.lines[e.get_nom()]
            historique = e.get_historique()
            ligne.set_ydata(historique)
            ligne.set_xdata(range(len(historique)))

        # Ajuste les limites du graphique
        self.a.relim()
        self.a.autoscale_view()

        # Redessine le graphique
        self.canvas.draw()

        # Appelle cette fonction toutes les 1000 ms (1 seconde)
        self.after(10, self.mettre_a_jour_graphique)



app = Ecran()
app.mainloop()

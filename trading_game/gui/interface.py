#Interface graphique (Tkinter)
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)

# Supposons que vous avez déjà les données des entreprises et leurs courbes générées dans une variable entreprises.
entreprises = [
    {"nom": "NovaTech", "valeur": 12.5, "variation": 0.0, "historique": [12.5]},
    {"nom": "BioCorp", "valeur": 10, "variation": 0.0, "historique": [10]},
    {"nom": "LuxIndustries", "valeur": 215.0, "variation": 0.0, "historique": [215.0]}
]

# Exemples de simulation de l'évolution des entreprises (comme dans votre code précédent)
def generer_pourcentage_augmentation(valeur: float, dernier_pourcentage: float) -> float:
    import random
    coef_volatilite = 1.5 if valeur < 100 else 0.8
    bruit = random.uniform(-1, 1) * coef_volatilite
    variation = bruit
    variation = max(-20, min(20, variation))
    return round(variation, 2)

def application_variation(valeur, variation):
    nouvelle_valeur = round(valeur * (1 + variation / 100), 2)
    return (nouvelle_valeur, variation)

# Création de la classe SeaofBTCapp pour l'interface utilisateur
class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

 #       tk.Tk.iconbitmap(self, default="clienticon.ico")  # Remplacer ou enlever si nécessaire
        tk.Tk.wm_title(self, "Sea of BTC client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                             command=lambda: controller.show_frame(PageThree))
        button3.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # Création du graphique pour afficher les entreprises
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)

        # Initialisation du graphique
        self.lines = {}
        for e in entreprises:
            line, = self.a.plot(e["historique"], label=e["nom"])
            self.lines[e["nom"]] = line

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
            pourcentage = generer_pourcentage_augmentation(e["valeur"], e["variation"])
            e["valeur"], e["variation"] = application_variation(e["valeur"], pourcentage)
            e["historique"].append(e["valeur"])



        # Met à jour les courbes du graphique
        for e in entreprises:
            self.a.plot(e["historique"], label=e["nom"])

        # Redessine le graphique avec les nouvelles valeurs
        self.canvas.draw()

        # Appelle cette fonction toutes les 1000 ms (1 seconde)
        self.after(1000, self.mettre_a_jour_graphique)


app = SeaofBTCapp()
app.mainloop()

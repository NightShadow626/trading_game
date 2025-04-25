#Fonctions utiles (formatage, génération de noms…)
class Entreprise:
    def __init__(self, nom: str, valeur_initiale: float):
        self.nom = nom
        self.valeur = valeur_initiale
        self.variation = 0.0
        self.historique = [valeur_initiale]

    def update(self, nouvelle_valeur: float, nouvelle_variation: float):
        self.valeur = nouvelle_valeur
        self.variation = nouvelle_variation
        self.historique.append(nouvelle_valeur)

    def __repr__(self):
        return f"{self.nom} : {self.valeur:.2f}€ ({self.variation:+.2f}%)"


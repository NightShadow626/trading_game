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
    
    def get_nom(self):
        return self.nom
    
    def get_valeur(self):
        return self.valeur

    def get_variation(self):
        return self.variation

    def get_historique(self):
        return self.historique

    def __repr__(self):
        return f"{self.nom} : {self.valeur:.2f}€ ({self.variation:+.2f}%)"

def generer_liste_entreprises(noms):
    # Génère une liste d'entreprises avec des valeurs initiales aléatoires
    import random
    return [Entreprise(nom, random.uniform(1, 100)) for nom in noms]

class Portefeuille:
    def __init__(self, argent_initial=10000):
        self.argent = argent_initial
        self.actions = {}  # nom_entreprise -> nombre d'actions possédées

    def acheter(self, entreprise, quantite):
        cout_total = entreprise.get_valeur() * quantite
        if cout_total <= self.argent:
            self.argent -= cout_total
            self.actions[entreprise.get_nom()] = self.actions.get(entreprise.get_nom(), 0) + quantite
            return True
        return False

    def vendre(self, entreprise, quantite):
        if self.actions.get(entreprise.get_nom(), 0) >= quantite:
            self.actions[entreprise.get_nom()] -= quantite
            self.argent += entreprise.get_valeur() * quantite
            return True
        return False
    
    def get_resume(self):
        return f"Argent disponible: {self.argent:.2f}€\n" + "\n".join(
            [f"{nom}: {qte} actions" for nom, qte in self.actions.items() if qte > 0]
        )


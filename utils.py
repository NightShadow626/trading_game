#Fonctions utiles (formatage, génération de noms…)
class Entreprise:
    def __init__(self, nom: str, valeur_initiale: float):
        self.nom = nom
        self.valeur = valeur_initiale
        self.variation = 0.0
        self.historique = {
            "debut": 0,
            "valeurs": [valeur_initiale]
        }

    def update(self, nouvelle_valeur: float, nouvelle_variation: float):
        self.valeur = nouvelle_valeur
        self.variation = nouvelle_variation
        self.mettre_a_jour_historique(nouvelle_valeur)

    def mettre_a_jour_historique(self, nouveau_prix):
        self.historique["valeurs"].append(nouveau_prix)

        # Garde uniquement les 100 derniers jours
        if len(self.historique["valeurs"]) > 100:
            surplus = len(self.historique["valeurs"]) - 100
            self.historique["valeurs"] = self.historique["valeurs"][surplus:]
            self.historique["debut"] += surplus

    def get_nom(self):
        return self.nom
    
    def mod_nom(self, nom):
        self.nom = nom

    def get_valeur(self):
        return self.valeur
    
    def mod_valeur(self, valeur):
        self.valeur = valeur

    def get_variation(self):
        return self.variation
    
    def mod_variation(self, variation):
        self.variation = variation

    def get_historique(self):
        return self.historique

    def get_all(self):
        return {
            "nom": self.nom,
            "valeur": self.valeur,
            "variation": self.variation,
            "historique": self.historique
        }



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
    
    def get_argent(self):
        return self.argent

    def get_actions(self):
        return self.actions

    def modifier_argent(self, argent):
        self.argent = argent
    
    def modifier_actions(self, actions):
        self.actions = actions
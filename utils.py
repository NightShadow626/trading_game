# Importation des modules nécessaires
import random

#Fonctions utiles
class Entreprise:
    '''Classe représentant une entreprise avec un nom, une valeur et une variation de valeur.
    Elle contient également un historique des valeurs pour les 100 derniers jours.'''
    def __init__(self, nom: str, valeur_initiale: float) -> None:
        '''Initialise l'entreprise avec un nom et une valeur initiale. L'historique est initialisé avec la valeur initiale.'''
        self.nom = nom
        self.valeur = valeur_initiale
        self.variation = 0.0
        self.historique = {
            "debut": 0,
            "valeurs": [valeur_initiale]
        }

    def update(self, nouvelle_valeur: float, nouvelle_variation: float) -> None:
        '''Met à jour la valeur et la variation de l'entreprise, et met à jour l'historique des valeurs.'''
        self.valeur = nouvelle_valeur
        self.variation = nouvelle_variation
        self.mettre_a_jour_historique(nouvelle_valeur)

    def mettre_a_jour_historique(self, nouveau_prix: float) -> None:
        '''Met à jour l'historique des valeurs avec la nouvelle valeur. Garde uniquement les 100 derniers jours.'''
        self.historique["valeurs"].append(nouveau_prix)

        # Garde uniquement les 100 derniers jours
        if len(self.historique["valeurs"]) > 100:
            surplus = len(self.historique["valeurs"]) - 100
            self.historique["valeurs"] = self.historique["valeurs"][surplus:]
            self.historique["debut"] += surplus

    def get_nom(self) -> str:
        '''Retourne le nom de l'entreprise.'''
        return self.nom
    
    def mod_nom(self, nom : str) -> None:
        '''Modifie le nom de l'entreprise.'''
        self.nom = nom

    def get_valeur(self) -> float:
        '''Retourne la valeur actuelle de l'entreprise.'''
        return self.valeur
    
    def mod_valeur(self, valeur : float) -> None:
        '''Modifie la valeur de l'entreprise.'''
        self.valeur = valeur

    def get_variation(self) -> float:
        '''Retourne la variation actuelle de l'entreprise.''' 
        return self.variation
    
    def mod_variation(self, variation : float) -> None:
        '''Modifie la variation de l'entreprise.'''
        self.variation = variation

    def get_historique(self) -> dict:
        '''Retourne l'historique des valeurs de l'entreprise.'''
        return self.historique
    
    def get_debut_historique(self) -> int:
        return self.historique["debut"]

    def get_all(self) -> dict:
        '''Retourne toutes les informations de l'entreprise sous forme de dictionnaire.'''
         # Retourne un dictionnaire avec toutes les informations de l'entreprise
         # y compris le nom, la valeur, la variation et l'historique
        return {
            "nom": self.nom,
            "valeur": self.valeur,
            "variation": self.variation,
            "historique": self.historique
        }



def generer_liste_entreprises(noms : list) -> list:
    '''Génère une liste d'entreprises avec des valeurs initiales aléatoires entre 1 et 100.'''
    import random
    return [Entreprise(nom, random.uniform(1, 100)) for nom in noms]



class Portefeuille:
    '''Classe représentant un portefeuille d'actions. Il contient l'argent disponible et les actions possédées.'''
    def __init__(self, argent_initial : float = 100) -> None:
        '''Initialise le portefeuille avec un montant d'argent initial et un dictionnaire d'actions.'''
        self.argent = argent_initial
        self.actions = {}  # nom_entreprise -> nombre d'actions possédées

    def acheter(self, entreprise : object, quantite : int) -> bool:
        '''Achète une certaine quantité d'actions d'une entreprise si l'argent disponible le permet.'''
        cout_total = entreprise.get_valeur() * quantite
        if cout_total <= self.argent:
            self.argent -= cout_total
            self.actions[entreprise.get_nom()] = self.actions.get(entreprise.get_nom(), 0) + quantite
            return True
        return False

    def vendre(self, entreprise : object, quantite : int) -> bool:
        '''Vend une certaine quantité d'actions d'une entreprise si le portefeuille en possède suffisamment.'''
        if self.actions.get(entreprise.get_nom(), 0) >= quantite:
            self.actions[entreprise.get_nom()] -= quantite
            self.argent += entreprise.get_valeur() * quantite
            return True
        return False
    
    def get_resume(self) -> str:
        '''Retourne un résumé du portefeuille sous forme de chaîne de caractères.'''
        return f"Argent disponible: {self.argent:.2f}€\n" + "\n".join(
            [f"{nom}: {qte} actions" for nom, qte in self.actions.items() if qte > 0]
        )
    
    def get_argent(self) -> float:
        '''Retourne le montant d'argent disponible dans le portefeuille.'''
        return self.argent

    def get_actions(self) -> dict:
        '''Retourne le dictionnaire des actions possédées dans le portefeuille.'''
        return self.actions

    def modifier_argent(self, argent : float) -> None:
        '''Modifie le montant d'argent disponible dans le portefeuille.'''
        self.argent = argent
    
    def modifier_actions(self, actions : dict) -> None:
        '''Modifie le dictionnaire des actions possédées dans le portefeuille.'''
        self.actions = actions

# Lists to generate silly info messages
subjects = [
    "Le hamster du trader", "Une licorne", "Un pigeon", "Le café de la machine",
    "Le stagiaire", "La photocopieuse", "L’imprimante", "Le robot aspirateur",
    "La plante verte", "Le PDG", "Le chat", "Le chien", "Le poisson rouge",
    "La souris", "Le cochon d'Inde", "Le lama", "Le kangourou", "Le panda",
    "Le serpent", "Le robot", "Le fantôme", "Le squelette", "Le ninja",
    "Le pirate", "Le dragon", "Le robot-cuiseur", "La télécommande", "La télé",
    "Le grille-pain", "Le vélo"
]

verbs = [
    "a piraté", "a dansé sur", "a dévoré", "a glissé sur", "a tweeté",
    "a enchanté", "a hypnotisé", "a imprimé", "a téléporté", "a lancé",
    "a vendu", "a acheté", "a peint", "a transformé", "a cassé",
    "a réparé", "a chanté", "a sifflé", "a nagé dans", "a cuisiné",
    "a exploré", "a ignoré", "a embrassé", "a endormi", "a réveillé",
    "a effrayé", "a construit", "a déchaîné", "a fait pousser", "a planté"
]

objects = [
    "un sandwich", "le Nasdaq", "une machine à café", "une licorne en peluche",
    "une boule de cristal", "un fromage volant", "un nuage", "la blockchain",
    "un sel de bain", "une chaussette", "le code source", "une banane",
    "un arc-en-ciel", "une pizza", "un dragon miniature", "une porte transparente",
    "un toaster", "une trottinette", "un cactus", "un trombone", "un donut",
    "un cupcake", "une galette"
]



def afficher_info_inutile(label):
    message = f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)}."
    label.config(text="📢 Flash Info : " + message)
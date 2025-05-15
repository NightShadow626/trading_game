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

    def supprimer_action(self):
        self.actions = {}
    
    def get_argent(self) -> float:
        '''Retourne le montant d'argent disponible dans le portefeuille.'''
        return self.argent

    def get_actions(self) -> dict:
        '''Retourne le dictionnaire des actions possédées dans le portefeuille.'''
        return self.actions

    def modifier_argent(self, argent : float) -> None:
        '''Modifie le montant d'argent disponible dans le portefeuille.'''
        self.argent = argent
    
    def ajouter_argent(self, argent : float) -> None:
        self.argent += argent
    
    def modifier_actions(self, actions : dict) -> None:
        '''Modifie le dictionnaire des actions possédées dans le portefeuille.'''
        self.actions = actions

infos_inutiles = [
    "Le PDG de Financo a été aperçu en train de danser sur son bureau.",
    "Les pigeons de la place boursière prévoient un crash imminent.",
    "CryptoPotato annonce une nouvelle blockchain... pour les patates.",
    "FoodiCorp aurait racheté un fast-food pour l'expérience immersive.",
    "TechNova offre désormais des toasters connectés avec abonnement mensuel.",
    "Une taupe a été vue quittant les locaux de GameStart Inc.",
    "Le stagiaire de BioCorp aurait cliqué sur 'Vendre tout' par erreur.",
    "Le directeur de CleanPower roule en diesel. Chut.",
    "Un bug a fait monter la valeur de NullCompany à ∞€.",
    "Le conseil d’administration s’est perdu en salle de réunion.",
    "On a retrouvé un canard malin investissant dans les ETF.",
    "La machine à café de WallStreetCo refuse de servir avant 9h.",
    "La photocopieuse de TechSoft imprime uniquement des memes.",
    "Un chaton travaille désormais comme analyste financier junior.",
    "Les sandwichs de la cafétéria sont cotés en bourse.",
    "Le cloud de DataSky gonfle plus vite qu’un ballon de baudruche.",
    "Le bureau 42 est officiellement classé zone à haut risque de crash.",
    "On dit que l’imprimante de DevCorp émet des signaux de trading.",
    "Un ninja invisible a fait fondre le compte test de TradeSense.",
    "Le scooter flambant neuf du CEO est taxé comme un actif crypto.",
    "Les plantes vertes de FinTechHouse génèrent 0,05% de rendement.",
    "Une légende parle d’un glitch qui racheta toutes les actions Meta.",
    "Le grille-pain de SmartHomeCo brûle les toasts sur un trend ascendant.",
    "Les tableaux blancs de StrategyCorp s’auto-inscrivent en IPO.",
    "Le poney secret du département R&D fait grimper les valorisations.",
    "La porte du local data reste coincée sur un signal haussier.",
    "Un drone livre désormais les dividendes directement à domicile.",
    "La fax antique de RetroTrade envoie des ordres à 300 baud.",
    "On soupçonne un parc JurassicParkTokens de miner du Bitcoin.",
    "Le hamster du CEO s’est échappé avec des plans de diversification.",
    "Les tickets de métro chez CityTransit Inc. affichent le Cours du jour.",
    "On a découvert un trésor de pièces de monnaie dans l’armoire du bureau.",
    "Le distributeur de snacks déclenche des alertes de volatilité.",
    "Le chat de l’administrateur système a accès à tous les wallets.",
    "Les murs de la salle de réunion sont recouverts de graphiques TikZ.",
    "L’horloge du trading tourne à l’heure du Lapin Blanc d’Alice.",
    "Un ours en peluche porte un costume d’analyste financier senior.",
    "Le code de la dernière mise à jour est écrit en hiéroglyphes.",
    "Le stagiaire relit les contrats en format Comic Sans.",
    "La photocopieuse recrache des billets de Monopoly à chaque copie.",
    "Le distributeur d’eau propose maintenant des jetons NFT.",
    "Un chat holographique fait office de speaker dans les conférences.",
    "Le serveur principal tourne désormais sous Windows 95, par nostalgie.",
    "La RSI de CupcakeCorp est mesurée en parts de gâteau.",
    "Le drone de surveillance joue du ukulélé quand il patrouille.",
    "Un troll légendaire commente chaque transaction via Slack.",
    "Le toboggan du bureau est désormais la route d’évacuation d’urgence.",
    "Les employés reçoivent des actions en formules de blagues.",
    "Le distributeur de cafés prépare désormais des CappuInvestments.",
]

def afficher_info_inutile(label):
    '''Affiche une information inutile aléatoire sur l'interface graphique.'''
    # Choisir une information inutile aléatoire
    message = f"{random.choice(infos_inutiles)}."
    # Afficher l'information sur le label
    label.config(text="📢 Flash Info : " + message)

import os
import sys

def resource_path(relative_path):
    """Obtenir le chemin absolu vers une ressource, même si on est dans un .exe PyInstaller"""
    try:
        # PyInstaller crée un dossier temporaire et y place les fichiers
        base_path = sys._MEIPASS
    except AttributeError:
        # En mode développement
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#importation des modules nécessaires
# -*- coding: utf-8 -*-
import json
import os

#Constantes
# Chemin vers le fichier de sauvegarde
FICHIER_SAUVEGARDE = "sauvegardes.json"

def charger_toutes_les_sauvegardes() -> dict:
    """Charge toutes les sauvegardes à partir du fichier JSON."""
    if not os.path.exists(FICHIER_SAUVEGARDE): 
        return {}
    with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_partie(nom : str, joueur : dict, entreprises : dict, parametres : dict) -> None:
    """Sauvegarde l'état du jeu dans un fichier JSON."""
    sauvegardes = charger_toutes_les_sauvegardes()
    sauvegardes[nom] = {
        "nom": nom,
        "joueur": joueur,
        "entreprises": entreprises,
        "parametres": parametres
    }
    with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
        json.dump(sauvegardes, f, indent=4)

def charger_partie(nom : str) -> dict:
    """Charge une partie sauvegardée à partir du fichier JSON."""
    sauvegardes = charger_toutes_les_sauvegardes()
    return sauvegardes.get(nom)

def supprimer_sauvegarde(nom : str) -> None:
    """Supprime une sauvegarde spécifique."""
    sauvegardes = charger_toutes_les_sauvegardes()
    if nom in sauvegardes:
        del sauvegardes[nom]
        with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
            json.dump(sauvegardes, f, indent=4)

def lister_sauvegardes() -> list:
    """Liste toutes les sauvegardes disponibles."""
    return list(charger_toutes_les_sauvegardes().keys())
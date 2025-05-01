import json
import os

FICHIER_SAUVEGARDE = "sauvegardes.json"

def charger_toutes_les_sauvegardes():
    if not os.path.exists(FICHIER_SAUVEGARDE):
        return {}
    with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_partie(nom, joueur, entreprises, parametres):
    sauvegardes = charger_toutes_les_sauvegardes()
    sauvegardes[nom] = {
        "nom": nom,
        "joueur": joueur,
        "entreprises": entreprises,
        "parametres": parametres
    }
    with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
        json.dump(sauvegardes, f, indent=4)

def charger_partie(nom):
    sauvegardes = charger_toutes_les_sauvegardes()
    return sauvegardes.get(nom)

def supprimer_sauvegarde(nom):
    sauvegardes = charger_toutes_les_sauvegardes()
    if nom in sauvegardes:
        del sauvegardes[nom]
        with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
            json.dump(sauvegardes, f, indent=4)

def lister_sauvegardes():
    return list(charger_toutes_les_sauvegardes().keys())

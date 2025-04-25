import matplotlib.pyplot as plt
import random

#Génération des courbes / données
def generer_pourcentage_augmentation(valeur : float, dernier_pourcentage : float) -> float:
    """
    Génère un pourcentage de variation réaliste en fonction de la valeur de l'action.
    
    Les actions peu chères sont plus volatiles, les actions chères varient peu.

    valeur : float -> prix actuel de l'action (ex : 5.0, 120.0, etc.)
    dernier_pourcentage : float -> dernière variation (%)

    Retourne : float (ex : +1.43 ou -2.56)
    """

    # Coefficient de volatilité basé sur le prix
    # Plus le prix est bas, plus le multiplicateur est haut
    if valeur < 5:
        coef_volatilite = 8.0  # très volatile
    elif valeur < 20:
        coef_volatilite = 2.5
    elif valeur < 100:
        coef_volatilite = 1.5
    else:
        coef_volatilite = 0.8  # très stable

    # Influence de la tendance précédente (lissage)
    tendance = dernier_pourcentage * 0.3

    # Bruit aléatoire réaliste, modulé par le coef
    bruit = random.uniform(-1, 1) * coef_volatilite

    # Rare événement de marché (crash ou pic)
    evenement = 0
    if random.random() < 0.001:  # 0.1% de chance
        evenement = random.choice([-1, 1]) * random.uniform(5, 12)

    # Calcul de la variation finale
    variation = tendance + bruit + evenement

    # Clamp entre -20% et +20%
    variation = max(-20, min(20, variation))

    return round(variation, 2)

def application_variation(valeur, variation):
    nouvelle_valeur = round(valeur * (1 + variation / 100),2)
    return (nouvelle_valeur, variation)


#script test des deux fonction generer et apllication
#valeur = 7.5
#dernier = 1.2
#for i in range(20):
#    pourcentage = generer_pourcentage_augmentation(valeur, dernier)
#    valeur, dernier = application_variation(valeur, pourcentage)
#    print(valeur, pourcentage)

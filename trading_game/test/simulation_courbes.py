from data.courbes import *
from logic.utils import Entreprise

entreprises = [
    Entreprise("NovaTech", 12.5),
    Entreprise("BioCorp", 10),
    Entreprise("LuxIndustries", 215.0)
]

for _ in range(500):
    for e in entreprises:
        pourcentage = generer_pourcentage_augmentation(e.valeur, e.variation)
        nouvelle_valeur, variation = application_variation(e.valeur, pourcentage)
        e.update(nouvelle_valeur, variation)


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

for e in entreprises:
    plt.plot(e["historique"], label=e["nom"])

plt.title("Évolution du prix des actions")
plt.xlabel("Temps")
plt.ylabel("Prix (€)")
plt.legend()
plt.grid(True)
plt.show()

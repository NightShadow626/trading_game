# importation des modules nécessaires
# -*- coding: utf-8 -*-
from utils import generer_liste_entreprises
from interface import Ecran

# noms des entreprises à générer
# Ces noms sont fictifs et peuvent être modifiés selon les besoins
noms = ["TechCorp", "HealthInc", "AutoMakers", "Foodies", "FinTech"]
entreprises = generer_liste_entreprises(noms)

# Initialisation de l'interface graphique
# L'interface graphique est initialisée avec la liste d'entreprises générée
app = Ecran(entreprises=entreprises)
app.mainloop()
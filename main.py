#fichier mere, endroit où va s'executer le programme
from courbes import generer_pourcentage_augmentation, application_variation
from utils import Entreprise, generer_liste_entreprises, Portefeuille
from interface import Ecran

noms = ["TechCorp", "HealthInc", "AutoMakers", "Foodies", "FinTech"]
entreprises = generer_liste_entreprises(noms)

app = Ecran(entreprises=entreprises)
app.mainloop()
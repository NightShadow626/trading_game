from utils import generer_liste_entreprises
from interface import Ecran

noms = ["TechCorp", "HealthInc", "AutoMakers", "Foodies", "FinTech"]
entreprises = generer_liste_entreprises(noms)

app = Ecran(entreprises=entreprises)
app.mainloop()
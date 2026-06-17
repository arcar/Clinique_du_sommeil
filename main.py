#importation de l'objet cnx dans main.py
from ConnexionBdd import cnx

#connexion bdd
bdd = cnx

print("connexion réussi !")

#création d'une requête pour tester la connexion
cur = cnx.cursor()
query = "select * from appareil"

#éxecution de la requête
cur.execute(query)
result = cur.fetchall()
for f in result:
    print(f)
import pandas as pd

fileToRead = "./raw/signal-psg-patient-2-nuit-2.csv"

# Lire le CSV capteur patient
df = pd.read_csv(fileToRead, sep=",", encoding="utf-8-sig")

# Calcul des décibels max depuis le csv
decibels_max = df['ronflements_db'].max()

# Calcul de la moyenne des décibels depuis le csv
decibels_moy = df['ronflements_db'].mean()

import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import csv
from pathlib import Path



#-----------------------------------------------------
#-------- LECTURE FICHIER CSV-------------------------

# Pour choisir le csv a charger en fonction de l'id_nuit
id_nuit = input("Entrez l'id_nuit du fichier à charger : ")

for fichier in os.listdir("./raw/"):
    if fichier.endswith(f"-{id_nuit}.csv"):
        df = pd.read_csv("./raw/"+fichier)
        break
else :
    print("Aucun fichier trouvé")

#-----------------------------------------------------
#-------- DUREE SOMMEIL MINUTES ----------------------

# ICI on crée une variable pour indiquer la durée du sommeil en fonction des notes techniques
duree_sommeil_min =  int(input("Entrez durée du sommeil en minutes : "))



#-----------------------------------------------------
#-------- LECTURE SQL---------------------------------

load_dotenv()

# connexion bdd clinique
cnx = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print("Connexion réussie !")

#création d'une requête pour tester la connexion
cur = cnx.cursor()
query = "SELECT * FROM evenement_respiratoire where id_nuit = 1"

#éxecution de la requête
cur.execute(query)
result = cur.fetchall()
for f in result:
    print(f)



#-----------------------------------------------------
#-------- CALCUL INDICATEURS -------------------------

# Calcul des décibels max depuis le csv
decibels_max = df['ronflements_db'].max()

# Calcul de la moyenne des décibels depuis le csv
decibels_moy = df['ronflements_db'].mean()

# Suppression d'éventuelles espaces sur les colonnes
df["timestamp_sec"] = df["timestamp_sec"].astype(str).str.strip()
df["spo2"] = df["spo2"].astype(str).str.strip()
df["debit_nasal_pct"] = df["debit_nasal_pct"].astype(str).str.strip()
df["effort_thoracique_pct"] = df["effort_thoracique_pct"].astype(str).str.strip()

df["position"] = df["position"].astype(str).str.strip()
df["ronflements_db"] = df["ronflements_db"].astype(str).str.strip()

df["flag_evenement"] = df["flag_evenement"].astype(str).str.strip()


df["spo2"] = pd.to_numeric(df["spo2"],errors="coerce")

# Calcul Min spo2
spo2_min = min(df["spo2"])

# Calcul Moyenne spo2
spo2_moy = round(df.loc[:,'spo2'].mean(),1)

# Calcul médiane spo2
spo2_mediane = round(df.loc[:,'spo2'].median(),1)


print(f"spo2_min :{spo2_min}")
print(f"spo2_moy :{spo2_moy}")
print(f"spo2_mediane :{spo2_mediane}")



# Compter le nombre de secondes où spo2 < 90 - Chaque ligne 10 secondes 
nbr_secondes = len(df.loc[df['spo2'] < 90]) * 10
print(f"le nombre de secondes où spo2 < 90 : {nbr_secondes}")

# Calcul du nombre de ronflement fort 
df["ronflements_db"] = pd.to_numeric(df["ronflements_db"],errors="coerce")
nbr_ronflements_forts = len(df.loc[df["ronflements_db"]>70])
print(f"Nombre de ronflements forts : { nbr_ronflements_forts}")

# Calcul de la position dominante

position_dominante = df['position'].value_counts()

# label de max value
position_dominante = position_dominante[position_dominante == max(position_dominante)].index.tolist()[0]

print(f"Position dominante : {position_dominante}")

nb_doublons = df.duplicated().sum()

print(df)



print(position_dominante)


#-----------------------------------------------------
#-------- EXTRAPOLATION RESULTATS --------------------

new_duree_hypoxie = round(((nbr_secondes/60)*duree_sommeil_min)/60, 1)
new_nb_ronflements_forts = round((nbr_ronflements_forts/60)*duree_sommeil_min)

print(new_nb_ronflements_forts)

# Copier le CSV brut dans /raw/traite/
df.to_csv(f"./raw/traite/traite_signal-psg-patient-2-nuit-{id_nuit}.csv", sep=",", index=False, encoding="utf-8-sig")


# Charger les résultats_nuit dans SQL
cur.callproc('insert_data_night',(id_nuit, spo2_min, spo2_moy, spo2_mediane, duree_sommeil_min, new_duree_hypoxie, position_dominante, decibels_max, decibels_moy, new_nb_ronflements_forts))
cnx.commit()


#-----------------------------------------------------
#-------- COURBES --------------- --------------------

# Dossier de destination
dossier = Path(f"nuit/{id_nuit}")

# Création du dossier et des sous-dossiers si nécessaire
dossier.mkdir(parents=True, exist_ok=True)

# Générer une courbe PNG et PDF pour debit nasal
# Objectif : visualiser les données.
debit = []
with open("./raw/"+fichier, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        debit.append(float(row["debit_nasal_pct"]))
heures = list(range(len(debit)))
plt.plot(heures, debit, marker='o')
plt.xlabel("/10 secondes")
plt.ylabel("Débit nasal")
plt.title("Évolution du débit nasal sur une heure par tranche de 10 secondes")
plt.grid(True)
plt.savefig(dossier / f"debit_nasal_nuit_{id_nuit}.png")
plt.savefig(dossier / f"debit_nasal_nuit_{id_nuit}.pdf")

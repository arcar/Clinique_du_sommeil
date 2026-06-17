import pandas as pd
from ConnexionBdd import cnx


#-----------------------------------------------------
#-------- LECTURE FICHIER CSV-------------------------

fileToRead = "./raw/signal-psg-patient-2-nuit-2.csv"

# Lire le CSV capteur patient
df = pd.read_csv(fileToRead, sep=",", encoding="utf-8-sig")

#-----------------------------------------------------
#-------- LECTURE SQL---------------------------------

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
spo2_moy = df.loc[:,'spo2'].mean()

# Calcul médiane spo2
spo2_mediane = df.loc[:,'spo2'].median()


print(f"spo2_min :{spo2_min}")
print(f"spo2_moy :{spo2_moy}")
print(f"spo2_mediane :{spo2_mediane}")

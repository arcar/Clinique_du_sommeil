import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd


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

# label de  max value
position_dominante = position_dominante[position_dominante == max(position_dominante)].index.tolist()[0]

print(position_dominante)



#-----------------------------------------------------
#-------- EXTRAPOLATION RESULTATS --------------------

# new_nb_apnees = 
# new_nb_hypopnees =
# new_nb_rera =
# new_nb_microreveils =
new_duree_hypoxie = round(((nbr_secondes/60)*duree_sommeil_min)/60, 1)
new_nb_ronflements_forts = round((nbr_ronflements_forts/60)*duree_sommeil_min)

print(new_nb_ronflements_forts)

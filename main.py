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




#-----------------------------------------------------
#-------- CALCUL INDICATEURS -------------------------

# Calcul des décibels max depuis le csv
decibels_max = df['ronflements_db'].max()

# Calcul de la moyenne des décibels depuis le csv
decibels_moy = round(df['ronflements_db'].mean(),1)

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






# Compter le nombre de secondes où spo2 < 90 - Chaque ligne 10 secondes 
nbr_secondes = len(df.loc[df['spo2'] < 90]) * 10


# Calcul du nombre de ronflement fort 
df["ronflements_db"] = pd.to_numeric(df["ronflements_db"],errors="coerce")
nbr_ronflements_forts = len(df.loc[df["ronflements_db"]>70])


# Calcul de la position dominante

position_dominante = df['position'].value_counts()

# label de max value
position_dominante = position_dominante[position_dominante == max(position_dominante)].index.tolist()[0]



nb_doublons = df.duplicated().sum()








#-----------------------------------------------------
#-------- EXTRAPOLATION RESULTATS --------------------

new_duree_hypoxie = round(((nbr_secondes/60)*duree_sommeil_min)/60, 1)
new_nb_ronflements_forts = round((nbr_ronflements_forts/60)*duree_sommeil_min)



# Copier le CSV brut dans /raw/traite/
df.to_csv(f"./raw/traite/traite_signal-psg-patient-2-nuit-{id_nuit}.csv", sep=",", index=False, encoding="utf-8-sig")


#Charger les résultats_nuit dans SQL
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
ronflement_db = []
with open("./raw/"+fichier, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        debit.append(float(row["debit_nasal_pct"]))
        ronflement_db.append(float(row["ronflements_db"]))

heures = list(range(len(debit)))
plt.plot(heures, debit, marker='o')
plt.xlabel("/10 secondes")
plt.ylabel("Débit nasal")
plt.title("Évolution du débit nasal sur une heure par tranche de 10 secondes")
plt.grid(True)
plt.savefig(dossier / f"debit_nasal_nuit_{id_nuit}.png")
plt.savefig(dossier / f"debit_nasal_nuit_{id_nuit}.pdf")
plt.close()

heures2 = list(range(len(ronflement_db)))
plt.plot(heures2, ronflement_db, marker='o')
plt.xlabel("/10 secondes")
plt.ylabel("Ronflement (dB)")
plt.title("Évolution du ronflement sur une heure par tranche de 10 secondes")
plt.grid(True)
plt.savefig(dossier / f"ronflement_db_{id_nuit}.png")
plt.savefig(dossier / f"ronflement_db_{id_nuit}.pdf")


#-----------------------------------------------------
#-------- Rapport Medical ----------------------------

cur = cnx.cursor()

requete = """
SELECT nb_apnees, nb_hypopnees, nb_rera,iah
FROM resultat_nuit
WHERE id_nuit = %s
"""

cur.execute(requete, (id_nuit,))
result = cur.fetchone()

if result:
    nb_apnees = result[0]
    nb_hypopnees = result[1]
    nb_rera = result[2]
    iah = result[3]
else:
    nb_apnees = 0
    nb_hypopnees = 0
    nb_rera = 0
    iah = 0


with open(dossier / f"rapport_medical_{id_nuit}.txt", "w", encoding="utf-8") as f:
    f.write("=== Rapport médical pour le Medecin ===\n\n")
    
    f.write("============================================\n")
    f.write(f"=== Nuit : {id_nuit} ===\n\n")
    f.write("Spo2 min/moy/max: \n\n")
    f.write(f"minimum :{spo2_min}\n\n")
    f.write(f"moyen :{spo2_moy}\n\n")
    f.write(f"mediane :{spo2_mediane}\n\n")
    f.write("============================================\n\n")
    f.write("Ronflement fort (>70dB): \n\n")
    f.write(f"{new_nb_ronflements_forts}\n\n")
    f.write("intensité des ronflements : \n\n")
    f.write(f" MAX : {decibels_max} \n\n")
    f.write(f" MOYEN : {decibels_moy}\n\n")
    f.write("============================================\n\n")
    f.write("Duree Hypoxie : \n\n")
    f.write(f"{new_duree_hypoxie} min\n\n")
    f.write("============================================\n\n")
    f.write("Position Dominante : \n\n")
    f.write(f" {position_dominante}\n\n")
    f.write("============================================\n\n")
    f.write("Nombre d’apnées / hypopnées / RERA : \n\n")
    f.write(f" apnées :{nb_apnees}\n\n")
    f.write(f" hypopnées :{nb_hypopnees}\n\n")
    f.write(f" RERA :{nb_rera}\n\n")
    f.write("============================================\n\n")
    f.write("IAH : \n\n")
    f.write(f" IAH:{iah}\n\n")
    
    print(f"Rapport Medical généré dans 'rapport_medical.txt'.")

    

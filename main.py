import pandas as pd

fileToRead = "./raw/signal-psg-patient-2-nuit-2.csv"

# Lire le CSV capteur patient
df = pd.read_csv(fileToRead, sep=",", encoding="utf-8-sig")

# Calcul des décibels max depuis le csv
decibels_max = df['ronflements_db'].max()

# Calcul de la moyenne des décibels depuis le csv
decibels_moy = df['ronflements_db'].mean()
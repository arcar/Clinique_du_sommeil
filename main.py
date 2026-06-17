import pandas as pd


fileToRead = "./raw/signal-psg-patient-2-nuit-2.csv"

# Lire le CSV capteur patient
df = pd.read_csv(fileToRead, sep=",", encoding="utf-8-sig")


print(df)

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
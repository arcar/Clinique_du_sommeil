from ConnexionBdd import cnx
bdd = cnx
print("connexion réussi !")

cur = cnx.cursor()
query = "select * from appareil"

cur.execute(query)
result = cur.fetchall()
for f in result:
    print(f)
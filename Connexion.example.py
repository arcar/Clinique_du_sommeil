import mysql.connector


# connexion bdd clinique
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="votre_mdp",
    database="clinique"
)
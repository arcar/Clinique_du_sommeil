# Clinique_du_sommeil

# Objectif projet

-Lit le CSV capteur
-Calcule les indicateurs cliniques
-Remplit la table resultatnuit avec les indicateurs cliniques du csv et de la table evenementrespiratoire
-Envoie le CSV dans le datalake pour usage futur(modèle en étoile fait_nuits)
-Porduit un rapport médical avec diagnostic et courbes que le médecin pourra charger plus tard

# utilité du projet
le projet va servir a le connecter à une application front end(html/css/js) et back end(node.js/express.js)pour permettre au medecin de charger des rapport ainsi que des courbes sur des résultat d'analyse et ainsi implémenter les données nettoyer sur une IA disponible publiquement (TensorFlow)

# contribution équipe
Cedric = [Extraction - Lire le CSV capteur depuis un répertoire raw/]-[Transformation - Extrapolation sur la nuit complète] - [Livrables - Courbe à générer - Courbe débit nasal vs temps]

flora = [Transformation - Depuis le CSV - Décibels maximum et moyenne]- [Transformation - Depuis evenement_respiratoire -Nb d'apnées, hypopnées, RERA et évènements] - [calcul IAH et diag SAHOS] - [Livrables - Courbe à générer -  Courbe ronflements db vs temps]

malik = [Transformation - Depuis le CSV - Ronflement (nb) et position de someil] - [Transformation - Depuis le CSV - spo2 minimum moyenne, médianne et <90] - [Transformation - une fois les calculs réalisés - Copier le CSV brut dans /raw/traite/] - [Optionnel - Livrables - Courbe à générer - Surligner les segments d'événements]

yassine = [connection bdd en dotenv pour protection info connexion] - [Extraction - Lire les événements depuis la table evenement_respiratoire(via SQL)]- [Rapport - Réaliser le rapport médical (pour le médecin)]-[Livrables - Courbe à générer - Courbe SpO2 vs temps] - [redaction du readme.md]

# Projet versionner avec git

branche principal -> main
branch pour les test -> dev
depuis -> dev ->branche perso(votre_nom)
depuis ->branche perso ->branche <feat>,<fix>,<docs>,<chores>

lead = cedric
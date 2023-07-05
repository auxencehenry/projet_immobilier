####################################################
######## Définir les différents paramètres #########
####################################################

### 1. Définir le chemin où seront stockées les données immobilières dans la base SQL et nommer le fichier ###
chemin_base_sql = 'P:\Projets\Projet immobilier\Scraping\Bienici'
nom_base_sql = 'bdd_immobiliere'

### 2. Définir le chemin où sera créé le fichier Excel ###
chemin_excel = 'P:\Projets\Projet immobilier\Scraping\Bienici'
nom_excel = 'export_annonces_locatives'

####################################################
### Exécution du code avec les paramètres entrés ###
####################################################

import sqlite3
import pandas as pd

# Connexion à la base de données
con = sqlite3.connect(f'{chemin_base_sql}\{nom_base_sql}.db')

# Exportation des locations immobilières vers Excel
query = 'SELECT * FROM Locations'
df = pd.read_sql_query(query, con)
df.to_excel(f'{chemin_excel}\{nom_excel}.xlsx', sheet_name='Locations', index=False)

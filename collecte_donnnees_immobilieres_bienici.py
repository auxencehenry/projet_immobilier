####################################################
######## Définir les différents paramètres #########
####################################################

### 1. Définir le chemin où seront stockées les données immobilières dans la base SQL et nommer le fichier ###
chemin_base_sql = 'P:\Projets\Projet immobilier\Scraping\Bienici'
nom_base_sql = 'bdd_immobiliere'

### 2. Définir la liste des lieux dans lequel on veut collecter les annonces locatives : cela peut être une commune ou un département ###
# - Exemple pour les communes : place_list = ['lyon-69000','saint-etienne-42000','grenoble-38000','valence-26000','chambery-73000','annecy-74000','bourg-en-bresse-01000','villefranche-sur-saone-69400','roanne-42300','macon-71000','aix-les-bains-73100','vienne-38200','bourgoin-jallieu-38300','voiron-38500']
# - Exemple pour les départements : place_list = ['rhone-et-grand-lyon-69','isere-38','loire-42','haute-savoie-74','ain-01','drome-26','savoie-73','saone-et-loire-71','ardeche-07']
place_list = ['lyon-69000']

### 3. Définir le chemin où se situe le driver pour le bon fonctionnement de Selenium (en l'ayant téléchargé au même endroit au préalable)
chemin_driver = "C:\Program Files (x86)\chromedriver.exe"

####################################################
### Exécution du code avec les paramètres entrés ###
####################################################

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime
import sqlite3
import re

# Connexion à la base de données
con = sqlite3.connect(f'{chemin_base_sql}\{nom_base_sql}.db')
cur = con.cursor()

# Création de la table SQL incluse dans la base de données (si la table est déjà créée, on passe à la suite)
try:
  cur.execute('''CREATE TABLE Locations
               (date_collecte, url_annonce, titre_annonce, lieu_annonce, prix_annonce)''')
except:
  pass

# On initialise le driver avec des options utiles à la collecte, notamment l'option headless pour gagner en efficacité
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--enable-javascript")
driver = webdriver.Chrome(chemin_driver, options=chrome_options)

# La variable page_max va calculer le nombre de pages d'annonces maximum à collecter pour un lieu défini. L'algorithme ne s'arrête pas tant que l'on a pas collecté l'entiereté des annonces.
page_max = 1
for place in place_list:
  page = 1
  #On collecte chaque page d'annonce
  while page <= page_max:
    # On regarde seulement les appartements, mais il y a la possibilité de modifier l'URL pour inclure maisons, bâtiments et autres
    url_scraping = f"https://www.bienici.com/recherche/location/{place}/appartement?page={page}"
    driver.get(url_scraping)
    if page == 1:
      # On accepte les cookies
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='didomi-notice-agree-button']"))).click()
      # Le site Bien'Ici affiche exactement 24 annonces par page (en dehors des annonces mises en avant), on peut donc deviner le nombre de pages à parcourir par rapport à la quantité totale d'annonces affichées
      nombre_annonces = int(re.sub("[^0-9]", "",WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='search-results-count__title']/span/h2"))).text))
      page_max = nombre_annonces//24+1
    try:
      # On collecte la liste des annonces de la page que l'on est en train de parcourir (il y a donc 24 éléments dans cette liste)
      liste_annonces = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='sideListContainer']/div/article/div/div/div/div[1]/div/div[2]/div/a")))
      for annonce in liste_annonces:
        # Extraction de l'URL de l'annonce (pour aller voir plus tard du détail si l'annonce est intéressante)
        url_annonce = annonce.get_attribute('href').split('?')[0]
        # Extraction du titre, dans lequel on pourra extraire le type de bien (Studio, Duplex, Appartement ...) mais également la surface locative
        titre_annonce = WebDriverWait(annonce, 10).until(EC.presence_of_element_located((By.XPATH, "./div[2]/div[2]/h3/span[1]"))).text
        # Extraction du lieu, dans lequel on pourra extraire le code postal, la ville et parfois le quartier dans lequel se situe le bien
        lieu_annonce = WebDriverWait(annonce, 10).until(EC.presence_of_element_located((By.XPATH, "./div[2]/div[2]/h3/span[2]"))).text
        # Extraction du prix de l'annonce
        prix_annonce = WebDriverWait(annonce, 10).until(EC.presence_of_element_located((By.XPATH, "./div[2]/div[2]/div/div/span[1]"))).text

        # On supprime l'ancienne annonce collectée par la nouvelle en comparant les URL
        # Note importante : si un annonceur a créé deux URL différents pour un même bien locatif, il y aura donc deux lignes dans la base de données
        cur.execute('DELETE FROM Locations WHERE (url_annonce=?)', (url_annonce,))
        # On ajoute les éléments de l'annonce dans la table "Locations" de la base de données immobilière
        cur.execute('INSERT INTO Locations VALUES (?,?,?,?,?)', (datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"), url_annonce, titre_annonce, lieu_annonce, prix_annonce))
    except TimeoutException:
      pass
    # On sauvegarde la table "Locations" à chaque itération, ce qui permet de stocker les dernières informations en cas d'imprévu (coupure de courant, erreur inhabituelle ...)
    con.commit()
    page = page + 1

# On a fini de collecter les données, on peut donc fermer la table et la base de donnée SQL
con.close()
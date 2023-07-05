Voici un algorithme simple et concis de Web Scraping qui permet de collecter les données d'annonces immobilières locatives n'importe où en France grâce au site web https://www.bienici.com/

L'utilisation de cet algorithme peut avoir pour but (liste non exhaustive) :
- de chercher un bien immobilier en location pour avoir des référentiels de prix et de surface par rapport à la localisation souhaitée
- de produire des rapports sur les potentielles opportunités d'investissement locatif en s'appuyant sur des données essentielles

L'algorithme peut se paramètrer à l'aide d'une liste de villes, et même de départements, en stockant les résultats dans une base SQL en local.

Dans l'exemple fourni, j'ai paramétré l'algorithme sur la ville de Lyon, en focalisant la recherche sur les appartements (il est tout à fait possible d'ajouter les autres types de biens comme les maisons ou les immeubles selon les souhaits).

Egalement, je me suis limité aux métriques essentielles dans la collecte de données, en me focalisant sur la localisation, le prix et la surface locative des biens immobiliers.

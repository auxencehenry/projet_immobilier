Le fichier 'collecte_donnnees_immobilieres_bienici.py' est un algorithme simple et concis de Web Scraping qui permet de collecter les données d'annonces immobilières locatives n'importe où en France grâce au site web https://www.bienici.com/

L'utilisation de cet algorithme peut avoir pour but (liste non exhaustive) :
- de chercher un bien immobilier en location pour avoir des référentiels de prix et de surface par rapport à la localisation souhaitée
- de produire des rapports sur les potentielles opportunités d'investissement locatif en s'appuyant sur des données essentielles (voir le graphique 'Annonces locatives à Lyon (05-07-2023)')
- de traquer l'évolution du marché immobilier au cours du temps, en faisant fonctionner l'algorithme de manière journalière

L'algorithme peut se paramètrer à l'aide d'une liste de villes, et même de départements, en stockant les résultats dans une base SQL en local.

Dans l'exemple fourni, j'ai paramétré l'algorithme sur la ville de Lyon, en focalisant la recherche sur les appartements (il est tout à fait possible d'ajouter les autres types de biens comme les maisons ou les immeubles selon les souhaits).

Egalement, je me suis limité aux métriques essentielles dans la collecte de données, en me focalisant sur la localisation, le prix et la surface locative des biens immobiliers.

Enfin, il est possible d'exporter les données SQL sous format Excel à l'aide du fichier 'exporter_sql_en_excel.py'

**Note importante**
Je me suis limité à quelque chose de simple, mais il y a beaucoup de voies d'amélioration et notamment de collecter des données :
- le bilan énergétique par bien immobilier (DPE, GES)
- les données relatives à la personne qui a posté l'annonce (particulier, pro ...)
- intégrer du NLP (Natural Language Processing) pour collecter de la donnée qualitative et quantitative dans la description des annonces

Egalement, il est possible d'améliorer l'efficacité de l'algorithme en ajoutant :
- du multithreading en créant plusieurs threads pour exécuter une partie du code de manière indépendante
- la parallélisation pour exécuter simultanément plusieurs tâches ou processus indépendants

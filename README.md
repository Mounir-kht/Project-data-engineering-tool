# Projet DataEngineringTool
## Reddit Stocks Analysis
Par Mounir Khettou et Arthur Bargas

### Présentation du projet
Nous avons développé un outil sous forme de page web permettant d'analyser et de créer des liens entre les posts Reddit du thread "Trading" et les fluctuations des courts des bourses des entreprises du Dow Jones (indice boursier de New York, équivalent du CAC 40 français).

### Installation
Pour installer et avoir accès à notre projet, il vous faut simplement cloner ce projet github sur votre machine, ouvrir un terminal, se rendre dans le répertoire contenant le projet cloné et exécuter un `"docker compose up -d"`. Une fois ces actions réalisées, l'outil sera lancé automatiquement et vous pourrez vous y connecter en vous rendant sur l'adresse `localhost:5066` de votre navigateur après quelques secondes.


### Guide utilisateur
Une fois sur la page, vous pourrez prendre connaissance de l'interface. Vous y trouverez au centre deux sélecteurs. 
- Le premier demande de choisir un nombre qui correspond au nombre de posts que vous souhaitez scraper sur le thread reddit "r/Trading". 
- Le second quant à lui, permet de choisir quelle entreprise vous visez parmi la liste des entreprises du Dow Jones.

Une fois les deux informations sélectionnées, vous pourrez valider à l'aide du bouton en bas de page. Une fois que vous aurez validé, le scraping en live se lance ainsi que la récupération des données boursières. `Attention` cette opération peut prendre plusieurs minutes (surtout si vous sélectionnez un grand nombre de posts). Il est donc important de ne cliquer qu'une seule fois sur le bouton valider, faut de quoi vous lancerez plusieurs requêtes qui ne feront qu'augmenter le temps d'attente.

### Guide développeur

L'application est répartie dans différents environnements. Tout d'abord, l'application de lance dans un container docker qui contient python3.8, MongoDB et Selenium Firefox. Ces trois containers sont créés et lancés lors de l'exécution de la commande "docker compose up".

Concernant les programmes, l'application se lance en exécutant le programme `reddit.py`.    Celui-ci appelle le script `script_selenium_new.py` qui contient trois fonctions:
- Scraping qui effectue le scraping sur le site de reddit
- search_mongo qui effectue des requêtes dans la base de données mongo et qui renvoie le nombre de posts qu'elle a trouvé
- finance_data qui récupère les informations boursières de l'entreprise passée en paramètre vis l'API yahoo finance.

Concernant le programme reddit.py, il gère toute l'interface web avec flask et fait le lien entre les pages et fichiers html et css dans les dossiers templates et static. Il permet aussi de générer les graphiques sur la seconde page du site.

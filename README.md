# OC-P12 : EPICEVENT - Développez une architecture back-end sécurisée avec Python et SQL

## Objectif
![logo](assets/logo.png)
Ce programme est un exercice proposé par [OpenClassRooms](https://openclassrooms.com/fr/) dans le cadre de la formation :
Développeur d'applications Python.

L'objectif est de développer une solution CRM sécurisée interne à l'entreprise Epic Events.
Epic Events est une entreprise qui organise des événements (fêtes, réunions professionnelles, manifestations hors les murs) pour ses clients.


## Fonctionnalités
L'idée est de pouvoir collecter et traiter les données des clients et des évènements que l'entreprise
organise pour eux à travers une base de données, tout en facilitant la communication entre les
différents pôles de l'entreprise.

La gestion est assurée par 3 départements:

● le département commercial.

● le département support.

● le département gestion.

Les commerciaux démarchent les clients. Ils créent et mettent à jour leurs profils sur la plateforme. Lorsqu’un client souhaite organiser un événement, un collaborateur du département gestion crée un contrat et l’associe au client.

Une fois le contrat signé, le commercial crée l’événement dans la plateforme et le département gestion désigne un membre du
département support qui sera responsable de l’organisation et du déroulé de l’événement.

## Technologies utilisées

<div align="center">

| Base de données | Interface    | Qualité                 |
|-----------------|--------------|-------------------------|
| sqlachemy       | click        | Flake8, Pylance         |
| argon           | rich         | Pytest                  |
| postgresql | questionnary | pytest-cov, pytest-html |
| pgadmin    |              | sentry                  |
| jwt |||
</div>

## Installation

- Creer le fichier d'environnement .env

```
DEFAULT_DATABASE = <<nom de la base de données>>
SECRET_KEY = <<clé d'encryptage des mots de passe>>
TOKEN_DELTA = 120 # temps de validité d'un token de connexion
```

- Ensuite cloner le projet github et activer l'environnement virtuel.

```
git clone https://github.com/Slb59/OC-P12.git
mkdir .venv
pipenv install
pipenv shell
```

- Pour installer la base de donnée, vous avez besoin de la connexion administrateur et du port pour l'accès. Il vous sera également demnandé un nom et un mot de passe pour le manager principal. Le manager pourra ensuite se connecter à la base pour créer les autres employés. L'outil d'installation propose également la création d'un jeu de données test.

```
python epicevent.py initbase
```

## Utilisation

- Pour se connecter l'utilisateur utilise la commande suivante:
```
python epicevent.py login
```

- La fonction de déconnection est également accessible:
```
python epicevent.py logout
```

- La liste des fonctions disponibles peut être visualisée en utilisant simplement les commandes suivantes:
```
python epicevent.py : commandes principales
python epicevent.py employee : commandes relatives à la gestion des employés
python epicevent.py client : commandes relatives à la gestion des clients
python epicevent.py contract : commandes relatives à la gestion des contrats
python epicevent.py event : commandes relatives à la gestion des évènements
```

## Documentation

Vous trouverez la documentation du projet dans le répertoire docs

## Execution des tests

Pour obtenir le rapport des tests:
```
pytest tests --html=htmlcov/report_tests.html
```

Pour la couverture de tests:
```
pytest --cov=./epicevents tests --cov-report html
```

Les accès au rapport de tests report_test.html et à la couverture de tests index.html
sont alors accessible depuis le répertoire htmlcov.

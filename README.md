# Pixel & Co. Project Manager

Une application web Python simple pour gérer les projets, tâches, user stories, utilisateurs et notifications d’une petite agence.

## Objectif

Cette preuve de concept propose une interface web moderne et simple pour centraliser la gestion de projet de Pixel & Co. Les données sont stockées localement dans un fichier binaire, sans besoin de base de données externe.

## Fonctionnalités principales

- connexion et gestion des rôles (administrateur, chef de projet, développeur, membre de l’équipe)
- création, modification et archivage de projets
- backlog de tâches avec statuts, priorités, assignations et dépendances
- user stories liées aux projets
- tableau de bord avec indicateurs de charge et échéances
- notifications locales et historique des actions

## Installation

1. Créez et activez un environnement Python.
2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Exécution locale

```bash
python run.py
```

Ouvrez ensuite http://127.0.0.1:5000.

## Docker

Construire l’image :

```bash
docker build -t projet-gestion .
```

Lancer le conteneur :

```bash
docker run --rm -p 5000:5000 projet-gestion
```

Avec Docker Compose :

```bash
docker compose up --build
```

Par défaut, le service est exposé sur le port 5002 pour éviter un conflit avec une autre application locale. Si vous voulez utiliser le port 5000, lancez :

```bash
PORT=5000 docker compose up --build
```

## Pipeline GitHub Actions

Le workflow CI se déclenche automatiquement sur push et pull request.

Il vérifie :
- l’installation des dépendances ;
- l’exécution des tests ;
- la construction de l’image Docker.

## Compte initial

- email : admin@pixelco.test
- mot de passe : admin

## Notes

Les données sont enregistrées localement dans data/db.bin. Si le fichier n’existe pas, il est créé automatiquement au premier lancement.

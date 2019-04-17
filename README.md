# webappden
Application d'intranet dans le cadre du projet final de mon AEC en Administration de réseaux et sécurité.

## Objectif
Mon équipe était composée de 5 personnes et j'avais comme objectif de faire une sorte d'intranet qui allait s'authentifier sur l'Active Directory du projet.

## Fonctionnalités
* Voir l'inventaire des équipements de l'entreprise fictive;
* Pouvoir laisser des notes sur la page d'accueil avec une sorte de petit tchat (sans websocket);
* Un look épuré (le look a été pris sur Internet par manque de temps pour le projet);
* Interface de connexion qui utilise LDAP pour synchroniser la base de donnée Active Directory avec MySQL;
* Une table dans la base de donnée MySQL pour l'inventaire de l'entreprise et les notes.

## Technologies utilisées
* Python 3 (https://www.python.org/)
* Django (https://www.djangoproject.com/)
* MySQL (https://www.mysql.com/fr/)
* Gunicorn (https://gunicorn.org/)
* NGINX (https://www.nginx.com/)

## Auteurs
* Olivier Example (https://github.com/olickqc)

## Sources
Design du front-end: https://github.com/creativetimofficial/paper-dashboard/, sous license MIT

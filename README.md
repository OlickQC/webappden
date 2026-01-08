# webappden
Application d'intranet dans le cadre du projet final de mon AEC en Administration de réseaux et sécurité (2018).

**⚠️ Note**: Projet scolaire de 2018 remis à jour en janvier 2026 pour fonctionner avec les technologies modernes.

**[🇬🇧 English version](README_EN.md)**

## Objectif original (2018)
Mon équipe était composée de 5 personnes et j'avais comme objectif de faire une sorte d'intranet qui allait s'authentifier sur l'Active Directory du projet.

## Fonctionnalités
* Voir l'inventaire des équipements de l'entreprise fictive;
* Pouvoir laisser des notes sur la page d'accueil avec une sorte de petit tchat (sans websocket);
* Un look épuré (le look a été pris sur Internet par manque de temps pour le projet);
* Interface de connexion qui utilise LDAP pour synchroniser la base de donnée Active Directory avec MySQL;
* Une table dans la base de donnée MySQL pour l'inventaire de l'entreprise et les notes.

## Mises à jour 2026

Ce projet a été modernisé et sécurisé en janvier 2026. Voici les principales modifications :

### Sécurité
- ✅ **Migration des secrets vers fichiers .env** : Secret key, mots de passe et configuration LDAP externalisés
- ✅ **Nettoyage de l'historique Git** : Suppression complète des informations sensibles (clés secrètes, mots de passe, informations personnelles) de tous les commits avec git-filter-repo
- ✅ **Ajout de python-decouple** : Gestion sécurisée des variables d'environnement
- ✅ **Configuration via variables d'environnement** : Database, LDAP, SECRET_KEY, DEBUG, ALLOWED_HOSTS

### Mises à jour des dépendances
- ✅ **Django 2.0.5 → Django 4.2 LTS** : Migration vers la version Long Term Support (support jusqu'en avril 2026)
- ✅ **Python 3.7-3.9 → Python 3.10-3.12** : Support des versions modernes de Python
- ✅ **Gunicorn 19.8.1 → 22.0.0** : Serveur WSGI mis à jour
- ✅ **mysqlclient 1.3.12 → 2.2.0** : Driver MySQL moderne
- ✅ **ldap3 2.5 → 2.9.1** : Client LDAP mis à jour
- ✅ **django-python3-ldap 0.11.1 → 0.15.0** : Support LDAP amélioré
- ✅ **pytz 2018.4 → 2024.1** : Base de données de fuseaux horaires à jour

### Compatibilité Django 4.2
- ✅ **Migration des vues d'authentification** : `auth_views.login` → `LoginView.as_view()`
- ✅ **Correction des imports obsolètes** : Suppression des imports dépréciés
- ✅ **Configuration ALLOWED_HOSTS dynamique** : Support pour plusieurs domaines/IPs
- ✅ **DEFAULT_AUTO_FIELD** : Configuration BigAutoField pour éliminer les warnings
- ✅ **STATICFILES_DIRS** : Configuration correcte des fichiers statiques (CSS/JS/images)

### Fonctionnalités ajoutées
- ✅ **Support Docker complet** : Dockerfile + docker-compose.yml pour déploiement conteneurisé
- ✅ **Déploiement Unraid** : Documentation complète pour Compose Manager
- ✅ **Option LDAP activable/désactivable** : Variable `LDAP_ENABLED` pour basculer entre auth Django et LDAP
- ✅ **GitHub Actions CI/CD** : Tests automatisés avec Python 3.10, 3.11 et 3.12
- ✅ **Support MariaDB distant** : Configuration flexible de la base de données

### Configuration
- ✅ **Fichiers .env** : Templates fournis (.env.example, .env.docker)
- ✅ **Documentation Docker** : Guide complet de déploiement (DOCKER_DEPLOYMENT.md)
- ✅ **Port configurable** : Support de multiples instances
- 
## Technologies utilisées

### Stack actuel (2026)
* **Python 3.10+** (https://www.python.org/)
* **Django 4.2 LTS** (https://www.djangoproject.com/)
* **MariaDB/MySQL 8.0+** (https://www.mysql.com/fr/)
* **Gunicorn 22.0** (https://gunicorn.org/)
* **NGINX** (https://www.nginx.com/)
* **Docker & Docker Compose** (https://www.docker.com/)
* **python-decouple** (https://pypi.org/project/python-decouple/) - Gestion des variables d'environnement
* **django-python3-ldap** (optionnel) - Authentification LDAP/Active Directory

### Stack original (2018)
* Python 3.6-3.7
* Django 2.0.5
* MySQL 5.7
* Gunicorn 19.8

## Déploiement

### Option 1 : Développement local (recommandé pour débuter)

1. **Cloner le dépôt**
```bash
git clone https://github.com/OlickQC/webappden.git
cd webappden
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
# Copier le template
cp .env.example .env
# Éditer le fichier .env avec vos valeurs
```

Variables minimales requises dans `.env` :
```env
SECRET_KEY=votre-cle-secrete-django-unique
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=webappden
DB_USER=root
DB_PASSWORD=votre-mot-de-passe
DB_HOST=localhost
DB_PORT=3306

LDAP_ENABLED=False  # Mettre True si vous avez un serveur LDAP
```

5. **Créer la base de données**
```sql
CREATE DATABASE webappden CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. **Exécuter les migrations**
```bash
python manage.py migrate
```

7. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic --noinput
```

8. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

9. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

L'application sera accessible sur http://localhost:8000

### Option 2 : Déploiement Docker (production)

Pour un déploiement avec Docker sur Unraid ou autre serveur, consultez la documentation complète :

📖 **[Guide de déploiement Docker](docs/DOCKER_DEPLOYMENT.md)**

Démarrage rapide Docker :
```bash
# Créer le fichier .env avec vos valeurs
cp .env.docker .env
nano .env

# Démarrer les conteneurs
docker-compose up -d

# Exécuter les migrations
docker exec -it webappden python manage.py migrate

# Collecter les fichiers statiques
docker exec -it webappden python manage.py collectstatic --noinput

# Créer un superutilisateur
docker exec -it webappden python manage.py createsuperuser
```

L'application sera accessible sur http://votre-serveur:8585

## Configuration LDAP (optionnel)

Pour activer l'authentification LDAP/Active Directory :

1. Dans votre fichier `.env`, configurez :
```env
LDAP_ENABLED=True
LDAP_AUTH_URL=ldap://votre-serveur-ad:389
LDAP_AUTH_SEARCH_BASE=cn=Users,dc=votredomaine,dc=local
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN=votredomaine
LDAP_AUTH_CONNECTION_USERNAME=VotreUserLDAP
LDAP_AUTH_CONNECTION_PASSWORD=VotreMotDePasse
```

2. Les utilisateurs pourront se connecter avec leurs identifiants Active Directory

**Note** : Si `LDAP_ENABLED=False`, l'application utilise l'authentification Django standard.

## Générer une nouvelle SECRET_KEY

Pour générer une nouvelle clé secrète Django :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Tests

Les tests sont automatiquement exécutés via GitHub Actions à chaque push.

Pour lancer les tests localement :
```bash
python manage.py test
```

## Auteurs
* Olivier (https://github.com/olickqc)
* Projet scolaire 2018 - AEC Administration de réseaux et sécurité
* Modernisation 2026

## License
Ce projet est sous licence éducative. Le design front-end provient de Paper Dashboard (MIT License).

## Sources
* Design du front-end: https://github.com/creativetimofficial/paper-dashboard/ - MIT License
* Django Framework: https://www.djangoproject.com/
* Documentation Docker: https://docs.docker.com/

## Documentation

* 📖 [Guide de déploiement Docker (Français)](docs/DOCKER_DEPLOYMENT.md)
* 📖 [Docker Deployment Guide (English)](docs/DOCKER_DEPLOYMENT_EN.md)
* 📝 [Changelog (Français)](CHANGELOG.md)
* 📝 [Changelog (English)](CHANGELOG_EN.md)

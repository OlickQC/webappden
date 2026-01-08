# Changelog

## [2.0.1] - Janvier 2026 - Correctifs fichiers statiques et warnings

### 🐛 Corrections
- **Configuration DEFAULT_AUTO_FIELD** : Ajout de `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'` pour éliminer les warnings Django 4.2
- **Configuration STATICFILES_DIRS** : Ajout du chemin vers `dashboard/static` pour servir correctement les fichiers CSS/JS/images
- **Script entrypoint.sh** : Automatisation de la collecte des fichiers statiques au démarrage du conteneur Docker
- **Volume Docker pour statiques** : Ajout d'un volume persistant pour les fichiers statiques collectés

### 📝 Documentation
- Ajout de l'étape `collectstatic` dans les guides de déploiement
- Documentation sur l'importance de la collecte des fichiers statiques
- Mise à jour de DOCKER_DEPLOYMENT.md avec les nouvelles étapes

## [2.0.0] - Janvier 2026 - Modernisation complète

### 🔒 Sécurité
- Migration complète vers fichiers `.env` pour la gestion des secrets
- Nettoyage de l'historique Git avec `git-filter-repo`
  - Suppression de la SECRET_KEY
  - Suppression des mots de passe LDAP
  - Suppression des informations personnelles (nom, email)
- Ajout de `python-decouple` pour la gestion sécurisée des variables d'environnement
- Configuration dynamique de `ALLOWED_HOSTS`

### ⬆️ Mises à jour majeures
- **Django** : 2.0.5 → 4.2 LTS
- **Python** : Support 3.10, 3.11, 3.12 (fin du support 3.7-3.9)
- **Gunicorn** : 19.8.1 → 22.0.0
- **mysqlclient** : 1.3.12 → 2.2.0
- **ldap3** : 2.5 → 2.9.1
- **django-python3-ldap** : 0.11.1 → 0.15.0
- **pytz** : 2018.4 → 2024.1

### 🔧 Compatibilité Django 4.2
- Migration de `auth_views.login` vers `LoginView.as_view()`
- Correction des imports obsolètes
- Mise à jour de la configuration de la base de données
- Ajout de `STATIC_ROOT` pour la collecte des fichiers statiques

### ✨ Nouvelles fonctionnalités
- **Support Docker complet**
  - `Dockerfile` optimisé pour production
  - `docker-compose.yml` avec service MariaDB intégré
  - Support pour base de données externe
- **Option LDAP activable/désactivable**
  - Variable `LDAP_ENABLED` pour basculer entre auth Django et LDAP
  - Permet le développement local sans serveur LDAP
- **GitHub Actions CI/CD**
  - Tests automatisés sur Python 3.10, 3.11, 3.12
  - Service MySQL pour les tests
  - Vérification automatique à chaque push
- **Documentation complète**
  - README.md étendu avec guides de déploiement
  - DOCKER_DEPLOYMENT.md pour Unraid et autres serveurs
  - Templates .env pour faciliter la configuration

### 📝 Configuration
- Fichiers `.env.example` et `.env.docker` fournis
- Support pour MariaDB distant
- Port configurable (par défaut 8585 pour Docker)
- Variables d'environnement pour tous les paramètres sensibles

### 🐛 Corrections
- Correction du workflow GitHub Actions
- Ajout de l'attente MySQL dans les tests CI
- Installation de `mysql-client` pour les healthchecks
- Configuration correcte des OPTIONS de base de données

---

## [1.0.0] - Mai 2018 - Version initiale

### Fonctionnalités originales
- Application d'intranet pour projet scolaire AEC
- Authentification LDAP/Active Directory
- Gestion d'inventaire d'équipements
- Système de notes (mini-chat)
- Interface avec Paper Dashboard
- Base de données MySQL
- Déploiement avec Gunicorn + NGINX

### Stack technique original
- Python 3.6-3.7
- Django 2.0.5
- MySQL 5.7
- Gunicorn 19.8.1
- NGINX

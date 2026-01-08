# webappden
Intranet application created as a final project for my College Diploma in Network Administration and Security (2018).

**⚠️ Note**: 2018 school project updated in January 2026 to work with modern technologies.

**[🇫🇷 Version française](README.md)**

## Original Goal (2018)
My team consisted of 5 people and my objective was to create an intranet that would authenticate against the project's Active Directory.

## Features
* View inventory of fictional company equipment
* Post notes on the homepage with a simple chat system (without websockets)
* Clean interface (design taken from the internet due to project time constraints)
* Login interface using LDAP to sync Active Directory database with MySQL
* MySQL database table for company inventory and notes

## 2026 Updates

This project was modernized and secured in January 2026. Here are the main changes:

### Security
- ✅ **Migration of secrets to .env files**: Secret key, passwords, and LDAP configuration externalized
- ✅ **Git history cleanup**: Complete removal of sensitive information (secret keys, passwords, personal information) from all commits using git-filter-repo
- ✅ **Added python-decouple**: Secure environment variable management
- ✅ **Configuration via environment variables**: Database, LDAP, SECRET_KEY, DEBUG, ALLOWED_HOSTS

### Dependency Updates
- ✅ **Django 2.0.5 → Django 4.2 LTS**: Migration to Long Term Support version (supported until April 2026)
- ✅ **Python 3.7-3.9 → Python 3.10-3.12**: Support for modern Python versions
- ✅ **Gunicorn 19.8.1 → 22.0.0**: Updated WSGI server
- ✅ **mysqlclient 1.3.12 → 2.2.0**: Modern MySQL driver
- ✅ **ldap3 2.5 → 2.9.1**: Updated LDAP client
- ✅ **django-python3-ldap 0.11.1 → 0.15.0**: Improved LDAP support
- ✅ **pytz 2018.4 → 2024.1**: Up-to-date timezone database

### Django 4.2 Compatibility
- ✅ **Authentication views migration**: `auth_views.login` → `LoginView.as_view()`
- ✅ **Deprecated imports removed**: Removed outdated imports
- ✅ **Dynamic ALLOWED_HOSTS configuration**: Support for multiple domains/IPs
- ✅ **DEFAULT_AUTO_FIELD**: BigAutoField configuration to eliminate warnings
- ✅ **STATICFILES_DIRS**: Proper static files configuration (CSS/JS/images)

### New Features
- ✅ **Complete Docker support**: Dockerfile + docker-compose.yml for containerized deployment
- ✅ **Unraid deployment**: Complete documentation for Compose Manager
- ✅ **Toggleable LDAP option**: `LDAP_ENABLED` variable to switch between Django auth and LDAP
- ✅ **GitHub Actions CI/CD**: Automated tests with Python 3.10, 3.11, and 3.12
- ✅ **Remote MariaDB support**: Flexible database configuration

### Configuration
- ✅ **.env files**: Templates provided (.env.example, .env.docker)
- ✅ **Docker documentation**: Complete deployment guide
- ✅ **Configurable port**: Support for multiple instances

## Tech Stack

### Current Stack (2026)
* **Python 3.10+** (https://www.python.org/)
* **Django 4.2 LTS** (https://www.djangoproject.com/)
* **MariaDB/MySQL 8.0+** (https://www.mysql.com/)
* **Gunicorn 22.0** (https://gunicorn.org/)
* **NGINX** (https://www.nginx.com/)
* **Docker & Docker Compose** (https://www.docker.com/)
* **python-decouple** (https://pypi.org/project/python-decouple/) - Environment variable management
* **django-python3-ldap** (optional) - LDAP/Active Directory authentication

### Original Stack (2018)
* Python 3.6-3.7
* Django 2.0.5
* MySQL 5.7
* Gunicorn 19.8

## Deployment

### Option 1: Local Development (recommended for beginners)

1. **Clone the repository**
```bash
git clone https://github.com/OlickQC/webappden.git
cd webappden
```

2. **Create a virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the template
cp .env.example .env
# Edit the .env file with your values
```

Minimum required variables in `.env`:
```env
SECRET_KEY=your-unique-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=webappden
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

LDAP_ENABLED=False  # Set to True if you have an LDAP server
```

5. **Create the database**
```sql
CREATE DATABASE webappden CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. **Run migrations**
```bash
python manage.py migrate
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Create a superuser**
```bash
python manage.py createsuperuser
```

9. **Start the development server**
```bash
python manage.py runserver
```

The application will be accessible at http://localhost:8000

### Option 2: Docker Deployment (production)

For Docker deployment on Unraid or other servers, see the complete documentation:

📖 **[Docker Deployment Guide](docs/DOCKER_DEPLOYMENT_EN.md)**

Docker quick start:
```bash
# Create .env file with your values
cp .env.docker .env
nano .env

# Start containers
docker-compose up -d

# Run migrations
docker exec -it webappden python manage.py migrate

# Collect static files
docker exec -it webappden python manage.py collectstatic --noinput

# Create a superuser
docker exec -it webappden python manage.py createsuperuser
```

The application will be accessible at http://your-server:8585

## LDAP Configuration (optional)

To enable LDAP/Active Directory authentication:

1. In your `.env` file, configure:
```env
LDAP_ENABLED=True
LDAP_AUTH_URL=ldap://your-ad-server:389
LDAP_AUTH_SEARCH_BASE=cn=Users,dc=yourdomain,dc=local
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN=yourdomain
LDAP_AUTH_CONNECTION_USERNAME=YourLDAPUser
LDAP_AUTH_CONNECTION_PASSWORD=YourPassword
```

2. Users will be able to log in with their Active Directory credentials

**Note**: If `LDAP_ENABLED=False`, the application uses standard Django authentication.

## Generate a new SECRET_KEY

To generate a new Django secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Tests

Tests are automatically run via GitHub Actions on every push.

To run tests locally:
```bash
python manage.py test
```

## Authors
* Olivier (https://github.com/olickqc)
* 2018 School Project - College Diploma in Network Administration and Security
* 2026 Modernization

## License
This project is under educational license. The front-end design comes from Paper Dashboard (MIT License).

## Sources
* Front-end design: https://github.com/creativetimofficial/paper-dashboard/ - MIT License
* Django Framework: https://www.djangoproject.com/
* Docker Documentation: https://docs.docker.com/

## Documentation

* 📖 [Docker Deployment Guide (English)](docs/DOCKER_DEPLOYMENT_EN.md)
* 📖 [Guide de déploiement Docker (Français)](docs/DOCKER_DEPLOYMENT.md)
* 📝 [Changelog (English)](docs/CHANGELOG_EN.md)
* 📝 [Changelog (Français)](docs/CHANGELOG.md)

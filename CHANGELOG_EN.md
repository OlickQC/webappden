# Changelog

## [2.0.1] - January 2026 - Static Files and Warnings Fixes

### 🐛 Fixes
- **DEFAULT_AUTO_FIELD Configuration**: Added `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'` to eliminate Django 4.2 warnings
- **STATICFILES_DIRS Configuration**: Added path to `dashboard/static` to properly serve CSS/JS/image files
- **entrypoint.sh Script**: Automated static file collection on Docker container startup
- **Docker Volume for Static Files**: Added persistent volume for collected static files

### 📝 Documentation
- Added `collectstatic` step in deployment guides
- Documentation on the importance of static file collection
- Updated DOCKER_DEPLOYMENT.md with new steps

## [2.0.0] - January 2026 - Complete Modernization

### 🔒 Security
- Complete migration to `.env` files for secrets management
- Git history cleanup with `git-filter-repo`
  - Removed SECRET_KEY
  - Removed LDAP passwords
  - Removed personal information (name, email)
- Added `python-decouple` for secure environment variable management
- Dynamic `ALLOWED_HOSTS` configuration

### ⬆️ Major Updates
- **Django**: 2.0.5 → 4.2 LTS
- **Python**: Support for 3.10, 3.11, 3.12 (ended support for 3.7-3.9)
- **Gunicorn**: 19.8.1 → 22.0.0
- **mysqlclient**: 1.3.12 → 2.2.0
- **ldap3**: 2.5 → 2.9.1
- **django-python3-ldap**: 0.11.1 → 0.15.0
- **pytz**: 2018.4 → 2024.1

### 🔧 Django 4.2 Compatibility
- Migrated from `auth_views.login` to `LoginView.as_view()`
- Fixed deprecated imports
- Updated database configuration
- Added `STATIC_ROOT` for static file collection

### ✨ New Features
- **Complete Docker Support**
  - Production-optimized `Dockerfile`
  - `docker-compose.yml` with integrated MariaDB service
  - Support for external database
- **Toggleable LDAP Option**
  - `LDAP_ENABLED` variable to switch between Django auth and LDAP
  - Enables local development without LDAP server
- **GitHub Actions CI/CD**
  - Automated tests on Python 3.10, 3.11, 3.12
  - MySQL service for testing
  - Automatic verification on every push
- **Complete Documentation**
  - Extended README.md with deployment guides
  - DOCKER_DEPLOYMENT.md for Unraid and other servers
  - .env templates to facilitate configuration

### 📝 Configuration
- `.env.example` and `.env.docker` files provided
- Support for remote MariaDB
- Configurable port (default 8585 for Docker)
- Environment variables for all sensitive parameters

### 🐛 Fixes
- Fixed GitHub Actions workflow
- Added MySQL wait in CI tests
- Installed `mysql-client` for healthchecks
- Proper database OPTIONS configuration

---

## [1.0.0] - May 2018 - Initial Version

### Original Features
- Intranet application for college diploma project
- LDAP/Active Directory authentication
- Equipment inventory management
- Notes system (mini-chat)
- Interface with Paper Dashboard
- MySQL database
- Deployment with Gunicorn + NGINX

### Original Tech Stack
- Python 3.6-3.7
- Django 2.0.5
- MySQL 5.7
- Gunicorn 19.8.1
- NGINX

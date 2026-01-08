# Guide de Configuration Sécurité

## Vue d'ensemble

Ce guide couvre les paramètres de sécurité pour déployer webappden derrière **Cloudflare** + **NGINX Proxy Manager** avec certificats SSL.

## Est-ce sécuritaire ?

**Réponse courte :** Oui, si correctement configuré.

**Ce que vous obtenez :**
- ✅ **Chiffrement SSL/TLS** (Cloudflare + NGINX Proxy Manager)
- ✅ **Protection DDoS** (Cloudflare)
- ✅ **Django 4.2 LTS moderne** avec correctifs de sécurité
- ✅ **Secrets basés sur l'environnement** (fichiers .env)
- ✅ **Protection CSRF** (intégrée à Django)
- ✅ **Protection XSS** (intégrée à Django + en-têtes navigateur)
- ✅ **Protection injection SQL** (Django ORM)

## Configuration Requise pour la Production

### 1. Variables d'environnement (.env)

**Paramètres critiques pour la production :**

```env
# DOIT ÊTRE FALSE EN PRODUCTION !
DEBUG=False

# Remplacer par votre domaine/IP réel
ALLOWED_HOSTS=webappden.votredomaine.com,192.168.1.40

# REQUIS : Votre/vos domaine(s) réel(s) avec https://
CSRF_TRUSTED_ORIGINS=https://webappden.votredomaine.com

# Paramètres SSL/HTTPS (derrière Cloudflare + NPM)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Cookies sécurisés (REQUIS pour HTTPS)
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Sécurité navigateur
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY
```

### 2. SECRET_KEY

Générer une clé secrète forte et unique :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Ne jamais réutiliser la même SECRET_KEY entre environnements ou projets !**

### 3. Identifiants de base de données

- Utiliser des mots de passe forts pour `DB_PASSWORD` et `DB_ROOT_PASSWORD`
- Ne jamais utiliser les mots de passe par défaut comme "root" ou "password"
- Recommandé : mots de passe de 20+ caractères avec majuscules, minuscules, chiffres et symboles

### 4. Identifiants LDAP (si activé)

- Utiliser un compte de service dédié avec permissions **lecture seule**
- Ne jamais utiliser les identifiants d'administrateur de domaine
- Stocker les identifiants dans `.env`, jamais dans le code

## Couches de Sécurité

### Couche 1 : Cloudflare
- Protection DDoS
- Web Application Firewall (WAF)
- Chiffrement SSL/TLS
- Limitation de débit
- Protection contre les bots

**Configuration :**
- Activer le mode SSL "Full (strict)" dans Cloudflare
- Activer HSTS dans Cloudflare
- Considérer l'activation de Bot Fight Mode

### Couche 2 : NGINX Proxy Manager
- Proxy inverse
- Gestion des certificats SSL
- Limitation de débit supplémentaire (optionnel)

**Configuration :**
```
Domain Names: webappden.votredomaine.com
Scheme: http
Forward Hostname/IP: webappden (nom du conteneur)
Forward Port: 8000
```

**Paramètres SSL :**
- ✅ Force SSL
- ✅ HTTP/2 Support
- ✅ HSTS Enabled
- ✅ HSTS Subdomains

**Avancé :**
```nginx
# Ajouter ces emplacements personnalisés si nécessaire
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header Host $host;
```

### Couche 3 : Application Django
- Protection CSRF
- Protection XSS
- Protection injection SQL (ORM)
- Protection clickjacking
- Gestion sécurisée des sessions
- Application HTTPS

## Liste de Vérification Sécurité

### Avant la Mise en Production

- [ ] `DEBUG=False` en production
- [ ] `SECRET_KEY` forte et unique générée
- [ ] `ALLOWED_HOSTS` défini sur des domaines spécifiques (pas `*`)
- [ ] `CSRF_TRUSTED_ORIGINS` configuré avec votre/vos domaine(s)
- [ ] Tous les paramètres SSL/HTTPS activés
- [ ] Mots de passe de base de données forts
- [ ] Identifiants LDAP sécurisés (si utilisés)
- [ ] Mode SSL Cloudflare : "Full (strict)"
- [ ] SSL activé dans NGINX Proxy Manager
- [ ] Sauvegardes régulières configurées
- [ ] Vérification de sécurité Django réussie : `python manage.py check --deploy`

### Exécuter la Vérification de Sécurité Django

```bash
# Dans votre conteneur ou environnement virtuel
python manage.py check --deploy
```

Cela vous avertira de toute mauvaise configuration de sécurité.

## Vulnérabilités Courantes & Mitigations

### 1. DEBUG=True en Production
**Risque :** Expose les traces de pile, variables d'environnement, requêtes SQL  
**Mitigation :** Toujours définir `DEBUG=False` en production

### 2. SECRET_KEY Faible
**Risque :** Détournement de session, prédiction de jeton CSRF  
**Mitigation :** Utiliser une clé aléatoire cryptographiquement forte (50+ caractères)

### 3. ALLOWED_HOSTS=*
**Risque :** Attaques d'en-tête HTTP Host  
**Mitigation :** Définir uniquement les noms de domaine spécifiques

### 4. CSRF_TRUSTED_ORIGINS Manquant
**Risque :** Contournement de la protection CSRF avec proxy inverse  
**Mitigation :** Définir tous les domaines où l'application est accessible

### 5. Déploiement HTTP uniquement
**Risque :** Attaques man-in-the-middle, vol d'identifiants  
**Mitigation :** Forcer HTTPS avec `SECURE_SSL_REDIRECT=True`

### 6. Cookies non sécurisés
**Risque :** Cookies de session/CSRF transmis via HTTP  
**Mitigation :** `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`

### 7. Injection SQL
**Risque :** Compromission de la base de données  
**Mitigation :** Toujours utiliser Django ORM, jamais de SQL brut avec entrée utilisateur

### 8. XSS (Cross-Site Scripting)
**Risque :** Injection JavaScript, vol d'identifiants  
**Mitigation :** Django échappe automatiquement les templates, ne jamais utiliser `|safe` sur entrée utilisateur

## Durcissement Supplémentaire (Optionnel)

### 1. Liste Blanche IP (niveau Unraid/Docker)

Dans `docker-compose.yml`, restreindre l'accès par IP :

```yaml
services:
  webappden:
    # ... configuration existante
    networks:
      default:
        ipv4_address: 192.168.1.100
    # Accessible uniquement depuis des IPs spécifiques (configurer dans le pare-feu)
```

### 2. Intégration Fail2Ban

Surveiller les journaux Django pour les tentatives de connexion échouées et bannir automatiquement les IPs.

### 3. Authentification à Deux Facteurs

Considérer l'ajout de `django-otp` pour 2FA sur les comptes admin.

### 4. En-têtes de Sécurité

Déjà configurés dans settings.py :
- `X-Frame-Options: DENY` (prévient le clickjacking)
- `X-Content-Type-Options: nosniff` (prévient le MIME sniffing)
- `X-XSS-Protection: 1; mode=block` (filtre XSS du navigateur)
- `Strict-Transport-Security` (HSTS)

### 5. Mises à Jour Régulières

```bash
# Mettre à jour les images Docker régulièrement
docker-compose pull
docker-compose up -d --build

# Mettre à jour les dépendances Python
pip list --outdated
pip install -U django gunicorn mysqlclient
```

## Surveillance & Journalisation

### 1. Activer la Journalisation Django

Déjà configuré pour LDAP. Étendre au besoin :

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/security.log',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
        },
    },
}
```

### 2. Surveiller les Journaux d'Accès

- Journaux d'accès NGINX Proxy Manager
- Analytics Cloudflare
- Journaux Docker : `docker logs -f webappden`

### 3. Alertes de Sécurité

Configurer des alertes pour :
- Tentatives de connexion échouées (10+ en 5 minutes)
- Pics d'erreurs 4xx/5xx
- Modèles de trafic inhabituels

## Réponse aux Incidents

Si compromis :

1. **Immédiatement :** Arrêter le conteneur
   ```bash
   docker-compose down
   ```

2. **Rotation des secrets :**
   - Générer une nouvelle `SECRET_KEY`
   - Changer tous les mots de passe de base de données
   - Changer les mots de passe LDAP

3. **Examiner les journaux :**
   ```bash
   docker logs webappden > incident_logs.txt
   ```

4. **Mettre à jour et redéployer :**
   ```bash
   git pull
   docker-compose up -d --build
   ```

5. **Forcer la déconnexion de tous les utilisateurs :**
   ```bash
   docker exec -it webappden python manage.py clearsessions
   ```

## Ressources

- [Documentation Sécurité Django](https://docs.djangoproject.com/fr/4.2/topics/security/)
- [Liste de Vérification Déploiement Django](https://docs.djangoproject.com/fr/4.2/howto/deployment/checklist/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Directives Sécurité Web Mozilla](https://infosec.mozilla.org/guidelines/web_security)

## Support

Pour les problèmes de sécurité, contactez le mainteneur en privé avant divulgation publique.

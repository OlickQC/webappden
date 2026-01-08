# Security Configuration Guide

## Overview

This guide covers the security settings for deploying webappden behind **Cloudflare** + **NGINX Proxy Manager** with SSL certificates.

## Is it secure?

**Short answer:** Yes, if properly configured.

**What you get:**
- ✅ **SSL/TLS encryption** (Cloudflare + NGINX Proxy Manager)
- ✅ **DDoS protection** (Cloudflare)
- ✅ **Modern Django 4.2 LTS** with security patches
- ✅ **Environment-based secrets** (.env files)
- ✅ **CSRF protection** (Django built-in)
- ✅ **XSS protection** (Django built-in + browser headers)
- ✅ **SQL injection protection** (Django ORM)

## Required Production Configuration

### 1. Environment Variables (.env)

**Critical settings for production:**

```env
# MUST BE FALSE IN PRODUCTION!
DEBUG=False

# Replace with your actual domain/IP
ALLOWED_HOSTS=webappden.yourdomain.com,192.168.1.40

# REQUIRED: Your actual domain(s) with https://
CSRF_TRUSTED_ORIGINS=https://webappden.yourdomain.com

# SSL/HTTPS Settings (behind Cloudflare + NPM)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Secure Cookies (REQUIRED for HTTPS)
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Browser Security
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY
```

### 2. SECRET_KEY

Generate a strong, unique secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Never reuse the same SECRET_KEY across environments or projects!**

### 3. Database Credentials

- Use strong passwords for `DB_PASSWORD` and `DB_ROOT_PASSWORD`
- Never use default passwords like "root" or "password"
- Recommended: 20+ character passwords with mixed case, numbers, and symbols

### 4. LDAP Credentials (if enabled)

- Use a dedicated service account with **read-only** permissions
- Never use Domain Admin credentials
- Store credentials in `.env`, never in code

## Security Layers

### Layer 1: Cloudflare
- DDoS protection
- Web Application Firewall (WAF)
- SSL/TLS encryption
- Rate limiting
- Bot protection

**Configuration:**
- Enable "Full (strict)" SSL mode in Cloudflare
- Enable HSTS in Cloudflare
- Consider enabling Bot Fight Mode

### Layer 2: NGINX Proxy Manager
- Reverse proxy
- SSL certificate management
- Additional rate limiting (optional)

**Configuration:**
```
Domain Names: webappden.yourdomain.com
Scheme: http
Forward Hostname/IP: webappden (container name)
Forward Port: 8000
```

**SSL Settings:**
- ✅ Force SSL
- ✅ HTTP/2 Support
- ✅ HSTS Enabled
- ✅ HSTS Subdomains

**Advanced:**
```nginx
# Add these custom locations if needed
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header Host $host;
```

### Layer 3: Django Application
- CSRF protection
- XSS protection
- SQL injection protection (ORM)
- Clickjacking protection
- Secure session management
- HTTPS enforcement

## Security Checklist

### Before Going Live

- [ ] `DEBUG=False` in production
- [ ] Strong unique `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` set to specific domains (not `*`)
- [ ] `CSRF_TRUSTED_ORIGINS` configured with your domain(s)
- [ ] All SSL/HTTPS settings enabled
- [ ] Strong database passwords
- [ ] LDAP credentials secured (if used)
- [ ] Cloudflare SSL mode: "Full (strict)"
- [ ] NGINX Proxy Manager SSL enabled
- [ ] Regular backups configured
- [ ] Django security check passed: `python manage.py check --deploy`

### Run Django Security Check

```bash
# Inside your container or virtual environment
python manage.py check --deploy
```

This will warn you about any security misconfigurations.

## Common Vulnerabilities & Mitigations

### 1. DEBUG=True in Production
**Risk:** Exposes stack traces, environment variables, SQL queries  
**Mitigation:** Always set `DEBUG=False` in production

### 2. Weak SECRET_KEY
**Risk:** Session hijacking, CSRF token prediction  
**Mitigation:** Use cryptographically strong random key (50+ characters)

### 3. ALLOWED_HOSTS=*
**Risk:** HTTP Host header attacks  
**Mitigation:** Set specific domain names only

### 4. Missing CSRF_TRUSTED_ORIGINS
**Risk:** CSRF protection bypass with reverse proxy  
**Mitigation:** Set all domains where app is accessible

### 5. HTTP-only deployment
**Risk:** Man-in-the-middle attacks, credential theft  
**Mitigation:** Enforce HTTPS with `SECURE_SSL_REDIRECT=True`

### 6. Insecure cookies
**Risk:** Session/CSRF cookies transmitted over HTTP  
**Mitigation:** `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`

### 7. SQL Injection
**Risk:** Database compromise  
**Mitigation:** Always use Django ORM, never raw SQL with user input

### 8. XSS (Cross-Site Scripting)
**Risk:** JavaScript injection, credential theft  
**Mitigation:** Django auto-escapes templates, never use `|safe` on user input

## Additional Hardening (Optional)

### 1. IP Whitelisting (Unraid/Docker level)

In `docker-compose.yml`, restrict access by IP:

```yaml
services:
  webappden:
    # ... existing config
    networks:
      default:
        ipv4_address: 192.168.1.100
    # Only accessible from specific IPs (configure in firewall)
```

### 2. Fail2Ban Integration

Monitor Django logs for failed login attempts and auto-ban IPs.

### 3. Two-Factor Authentication

Consider adding `django-otp` for 2FA on admin accounts.

### 4. Security Headers

Already configured in settings.py:
- `X-Frame-Options: DENY` (prevents clickjacking)
- `X-Content-Type-Options: nosniff` (prevents MIME sniffing)
- `X-XSS-Protection: 1; mode=block` (browser XSS filter)
- `Strict-Transport-Security` (HSTS)

### 5. Regular Updates

```bash
# Update Docker images regularly
docker-compose pull
docker-compose up -d --build

# Update Python dependencies
pip list --outdated
pip install -U django gunicorn mysqlclient
```

## Monitoring & Logging

### 1. Enable Django Logging

Already configured for LDAP. Expand as needed:

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

### 2. Monitor Access Logs

- NGINX Proxy Manager access logs
- Cloudflare Analytics
- Docker logs: `docker logs -f webappden`

### 3. Security Alerts

Set up alerts for:
- Failed login attempts (10+ in 5 minutes)
- 4xx/5xx error spikes
- Unusual traffic patterns

## Incident Response

If compromised:

1. **Immediately:** Stop the container
   ```bash
   docker-compose down
   ```

2. **Rotate secrets:**
   - Generate new `SECRET_KEY`
   - Change all database passwords
   - Change LDAP passwords

3. **Review logs:**
   ```bash
   docker logs webappden > incident_logs.txt
   ```

4. **Update and redeploy:**
   ```bash
   git pull
   docker-compose up -d --build
   ```

5. **Force logout all users:**
   ```bash
   docker exec -it webappden python manage.py clearsessions
   ```

## Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/4.2/topics/security/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)

## Support

For security issues, contact the maintainer privately before public disclosure.

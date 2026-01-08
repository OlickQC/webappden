# Déploiement Docker sur Unraid

## Configuration du Stack dans Compose Manager

### 1. Informations du Stack
- **Stack Name**: `webappden`
- **Stack Directory**: `/mnt/user/appdata/webappden` (ou votre chemin préféré)

### 2. Préparation sur Unraid

#### A. Créer le répertoire du stack
```bash
mkdir -p /mnt/user/appdata/webappden
cd /mnt/user/appdata/webappden
```

#### B. Copier les fichiers nécessaires
Transférez ces fichiers depuis votre PC vers le répertoire Unraid :
- `docker-compose.yml`
- `Dockerfile`
- `.env.docker` (renommer en `.env`)
- Tout le code de l'application

**Méthode recommandée** : Utiliser git sur Unraid (supprimer le docker-compose.yml déjà la)
```bash
cd /mnt/user/appdata/webappden
git clone https://github.com/OlickQC/webappden.git .
```

#### C. Configurer les variables d'environnement
```bash
# Copier le template .env
cp .env.docker .env

# Éditer le fichier .env avec vos valeurs
nano .env
```

**Important** : Modifiez au minimum ces variables :
- `SECRET_KEY` : Générez une nouvelle clé unique
- `DB_ROOT_PASSWORD` : Changez le mot de passe root de la base de données
- `ALLOWED_HOSTS` : Mettez votre IP Unraid ou nom de domaine

### 3. Choix de la base de données

#### Option A : Base de données Docker intégrée (Recommandé pour débuter)
Le `docker-compose.yml` inclut déjà un conteneur MariaDB.
- Utilisez `DB_HOST=db` dans le `.env`
- Les données seront stockées dans un volume Docker persistant

#### Option B : Utiliser votre serveur MariaDB existant (192.168.1.40)
1. Commentez ou supprimez la section `db:` dans `docker-compose.yml`
2. Supprimez la ligne `depends_on: - db` 
3. Dans `.env`, configurez :
   ```
   DB_HOST=192.168.1.40
   DB_PORT=3306
   ```

### 4. Déploiement dans Compose Manager

1. Ouvrez **Compose Manager** dans Unraid
2. Cliquez sur **Add new stack**
3. Remplissez :
   - **Stack name**: `webappden`
   - **Stack directory**: `/mnt/user/appdata/webappden`
4. Cliquez sur **Save**
5. Le plugin détectera automatiquement le `docker-compose.yml`
6. Cliquez sur **Compose Up** pour démarrer

### 5. Migrations et configuration initiale

Après le premier démarrage, exécutez les commandes suivantes :

```bash
# Accéder au conteneur
docker exec -it webappden bash

# Exécuter les migrations
python manage.py migrate

# Collecter les fichiers statiques (CSS, JS, images)
python manage.py collectstatic --noinput

# Créer un superutilisateur (optionnel)
python manage.py createsuperuser

# Quitter le conteneur
exit
```

**Note importante** : La commande `collectstatic` est essentielle pour que les fichiers CSS, JavaScript et images s'affichent correctement.

### 6. Accéder à l'application

L'application sera accessible sur :
- **URL** : `http://VOTRE-IP-UNRAID:8585`
- Exemple : `http://192.168.1.40:8585`

### 7. Configuration NGINX (Optionnel)

Si vous voulez utiliser NGINX comme reverse proxy :

#### A. Avec NGINX Proxy Manager sur Unraid
1. Ajoutez un nouveau Proxy Host
2. Domain Names : `webappden.votredomaine.local`
3. Forward Hostname/IP : `webappden` (nom du conteneur)
4. Forward Port : `8000`
5. Activez WebSocket Support si nécessaire

#### B. Modification du docker-compose.yml
Si vous utilisez NGINX, vous pouvez ne pas exposer le port 8585 :
```yaml
# Commentez la section ports:
# ports:
#   - "8585:8000"
```

Et ajoutez le réseau de NGINX Proxy Manager si nécessaire.

### 8. Commandes utiles

```bash
# Voir les logs
docker-compose logs -f webappden

# Redémarrer le stack
docker-compose restart

# Arrêter le stack
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Reconstruire après modification du code
docker-compose up -d --build
```

### 9. Mise à jour de l'application

```bash
cd /mnt/user/appdata/webappden
git pull
docker-compose up -d --build
```

## Troubleshooting

### Erreur de connexion à la base de données
- Vérifiez que le service `db` est démarré : `docker-compose ps`
- Vérifiez les logs : `docker-compose logs db`
- Vérifiez les credentials dans `.env`

### L'application ne démarre pas
- Vérifiez les logs : `docker-compose logs webappden`
- Vérifiez que toutes les variables d'environnement sont définies dans `.env`

### Erreur de permissions
```bash
chmod -R 755 /mnt/user/appdata/webappden
chown -R nobody:users /mnt/user/appdata/webappden
```

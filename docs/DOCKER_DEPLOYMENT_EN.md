# Docker Deployment on Unraid

## Stack Configuration in Compose Manager

### 1. Stack Information
- **Stack Name**: `webappden`
- **Stack Directory**: `/mnt/user/appdata/webappden` (or your preferred path)

### 2. Preparation on Unraid

#### A. Create the stack directory
```bash
mkdir -p /mnt/user/appdata/webappden
cd /mnt/user/appdata/webappden
```

#### B. Copy necessary files
Transfer these files from your PC to the Unraid directory:
- `docker-compose.yml`
- `Dockerfile`
- `.env.docker` (rename to `.env`)
- All application code

**Recommended method**: Use git on Unraid (remove the existing docker-compose.yml first)
```bash
cd /mnt/user/appdata/webappden
git clone https://github.com/OlickQC/webappden.git .
```

#### C. Configure environment variables
```bash
# Copy the .env template
cp .env.docker .env

# Edit the .env file with your values
nano .env
```

**Important**: Modify at minimum these variables:
- `SECRET_KEY`: Generate a new unique key
- `DB_ROOT_PASSWORD`: Change the database root password
- `ALLOWED_HOSTS`: Set your Unraid IP or domain name

### 3. Database Choice

#### Option A: Integrated Docker Database (Recommended for beginners)
The `docker-compose.yml` already includes a MariaDB container.
- Use `DB_HOST=db` in the `.env`
- Data will be stored in a persistent Docker volume

#### Option B: Use your existing MariaDB server (192.168.1.40)
1. Comment out or remove the `db:` section in `docker-compose.yml`
2. Remove the `depends_on: - db` line
3. In `.env`, configure:
   ```
   DB_HOST=192.168.1.40
   DB_PORT=3306
   ```

### 4. Deployment in Compose Manager

1. Open **Compose Manager** in Unraid
2. Click on **Add new stack**
3. Fill in:
   - **Stack name**: `webappden`
   - **Stack directory**: `/mnt/user/appdata/webappden`
4. Click on **Save**
5. The plugin will automatically detect the `docker-compose.yml`
6. Click on **Compose Up** to start

### 5. Migrations and Initial Configuration

After the first startup, run the following commands:

```bash
# Access the container
docker exec -it webappden bash

# Run migrations
python manage.py migrate

# Collect static files (CSS, JS, images)
python manage.py collectstatic --noinput

# Create a superuser (optional)
python manage.py createsuperuser

# Exit the container
exit
```

**Important note**: The `collectstatic` command is essential for CSS, JavaScript, and image files to display correctly.

### 6. Access the Application

The application will be accessible at:
- **URL**: `http://YOUR-UNRAID-IP:8585`
- Example: `http://192.168.1.40:8585`

### 7. NGINX Configuration (Optional)

If you want to use NGINX as a reverse proxy:

#### A. With NGINX Proxy Manager on Unraid
1. Add a new Proxy Host
2. Domain Names: `webappden.yourdomain.local`
3. Forward Hostname/IP: `webappden` (container name)
4. Forward Port: `8000`
5. Enable WebSocket Support if needed

#### B. Modifying docker-compose.yml
If you're using NGINX, you can skip exposing port 8585:
```yaml
# Comment out the ports section:
# ports:
#   - "8585:8000"
```

And add the NGINX Proxy Manager network if necessary.

### 8. Useful Commands

```bash
# View logs
docker-compose logs -f webappden

# Restart the stack
docker-compose restart

# Stop the stack
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild after code modification
docker-compose up -d --build
```

### 9. Application Updates

#### Via SSH (recommended method)

```bash
# Connect to Unraid via SSH
ssh root@192.168.1.40

# Navigate to the stack folder
cd /mnt/user/appdata/webappden

# Pull latest changes from GitHub
git pull

# Rebuild and restart containers
docker-compose down
docker-compose up -d --build

# Check logs
docker-compose logs -f webappden
```

#### Via Compose Manager (Unraid interface)

1. Open **Compose Manager** in Unraid
2. Find your **webappden** stack
3. Click on **Compose Down** (stop containers)
4. Via SSH, run `git pull` in `/mnt/user/appdata/webappden`
5. Return to Compose Manager
6. Click on **Compose Up** (restart)

**Note**: The container will automatically restart and execute:
- New database migrations
- Collection of updated static files
- Application redeployment

#### Update without rebuild (.env changes only)

If you only modify the `.env` file:

```bash
cd /mnt/user/appdata/webappden
nano .env  # Modify your variables
docker-compose restart webappden
```

Or via Compose Manager:
1. Modify the `.env` via Unraid file editor
2. In Compose Manager, click on **Restart** for the webappden stack

## Troubleshooting

### Database connection error
- Verify that the `db` service is started: `docker-compose ps`
- Check the logs: `docker-compose logs db`
- Verify credentials in `.env`

### Application won't start
- Check the logs: `docker-compose logs webappden`
- Verify that all environment variables are defined in `.env`

### Permission errors
```bash
chmod -R 755 /mnt/user/appdata/webappden
chown -R nobody:users /mnt/user/appdata/webappden
```

#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/var/www/inio_database_web"
VENV="/home/iniodeploy/inio_db_app/venv"
BACKUP_DIR="/var/backups/inio_db"
HEALTH_URL="http://127.0.0.1/"
TS=$(date +%Y%m%d_%H%M%S)

echo "==> [$TS] deploy start"
cd "$APP_DIR"

# Extract only the 3 vars pg_dump needs.
# Avoid `. .env` because the file contains values like `{SQL Server}` that
# would trigger bash brace expansion and fail.
extract_env() {
    grep -E "^$1=" "$APP_DIR/.env" | head -1 | cut -d= -f2- \
        | sed -E 's/^"(.*)"$/\1/;s/^'"'"'(.*)'"'"'$/\1/'
}
DB_NAME=$(extract_env DB_NAME)
DB_USER=$(extract_env DB_USER)
DB_PASSWORD=$(extract_env DB_PASSWORD)
if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
    echo "ERROR: DB_NAME/DB_USER/DB_PASSWORD missing from $APP_DIR/.env" >&2
    exit 1
fi

# shellcheck disable=SC1091
source "$VENV/bin/activate"

echo "==> git pull"
git pull --ff-only

echo "==> pip install"
pip install -r requirements.txt

echo "==> pg_dump backup"
mkdir -p "$BACKUP_DIR"
export PGPASSWORD="$DB_PASSWORD"
pg_dump -h localhost -U "$DB_USER" -d "$DB_NAME" -Fc \
        -f "$BACKUP_DIR/${DB_NAME}_${TS}.dump"
unset PGPASSWORD
# Retain last 14 backups
ls -1t "$BACKUP_DIR"/*.dump 2>/dev/null | tail -n +15 | xargs -r rm --

echo "==> migrate"
python manage.py migrate --no-input

echo "==> check --deploy"
python manage.py check --deploy

echo "==> collectstatic"
python manage.py collectstatic --no-input

echo "==> reload nginx + restart gunicorn"
sudo systemctl reload nginx
sudo systemctl restart gunicorn

echo "==> health check"
for i in 1 2 3 4 5; do
    sleep 3
    code=$(curl -sS -o /dev/null -w "%{http_code}" "$HEALTH_URL" || echo "000")
    if [ "$code" = "200" ]; then
        echo "==> deploy OK (health $code)"
        exit 0
    fi
    echo "  attempt $i: $code"
done

echo "==> deploy FAILED: health check never returned 200"
exit 1

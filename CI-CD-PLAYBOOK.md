# CI/CD Playbook: Django + Azure VM + GitHub Actions

Guía de referencia para replicar este pipeline en proyectos futuros. Basado en la implementación real del repo `inio_database_web`.

---

## 1. La arquitectura (y por qué esta)

```
┌───────────────┐   git push main    ┌──────────────┐
│  Dev laptop   │───────────────────>│    GitHub    │
└───────────────┘                    └──────┬───────┘
                                            │ webhook out
                                            │  (queue job)
                                            ▼
                              ┌─────────────────────────┐
                              │       Azure VM          │
                              │  ┌──────────────────┐   │
                              │  │  Self-hosted     │   │
                              │  │  runner (systemd)│───┼──> deploy.sh
                              │  └──────────────────┘   │       │
                              │  gunicorn + nginx       │       │
                              │  postgres + .env        │       │
                              └─────────────────────────┘       │
                                                                │
                                                                ▼
                                                          [pg_dump]
                                                          [migrate]
                                                          [health check]
```

### La pregunta clave: ¿self-hosted runner o SSH desde GitHub-hosted runner?

| | Self-hosted (elegido) | SSH desde runner de GitHub |
|---|---|---|
| Firewall inbound | **No abre nada** | Debes abrir puerto 22 (aunque sea a IPs de GitHub) |
| Secrets en GitHub | Ninguno necesario | Clave SSH privada + host |
| Corporate/gov networks | ✅ Naturalmente compatible | ❌ Casi siempre bloqueado |
| Costo | Gratis (usa tu VM) | Gratis en repos públicos |
| Acceso al filesystem | Directo (`.env`, venv, sockets) | Todo vía SSH |

**Regla:** en cualquier entorno corporativo/gubernamental usa self-hosted. Solo usa SSH-from-cloud si trabajas con SaaS externo sin restricciones de red.

---

## 2. Los 5 componentes indispensables

1. **`.github/workflows/deploy.yml`** — define trigger y coordina, no ejecuta lógica de negocio.
2. **`deploy.sh`** — la lógica de deploy real (backup, migrate, static, restart, health).
3. **Self-hosted runner** — el "brazo" de GitHub dentro de la VM.
4. **Sudoers rule** — permisos mínimos para reload nginx y restart gunicorn.
5. **Backup directory** — red de seguridad antes de migrar la DB.

**Separación de responsabilidades**: el workflow no debe hacer trabajo pesado. Solo dispara `deploy.sh`. Beneficios:
- Puedes correr `deploy.sh` manualmente en la VM para debug sin GitHub.
- El workflow queda simple (~15 líneas).
- Los cambios en la lógica de deploy no requieren cambiar YAML.

---

## 3. Los archivos con anotaciones

### `deploy.sh` — la lógica

```bash
#!/usr/bin/env bash
set -euo pipefail   # -e: aborta ante error. -u: variables sin definir = error. -o pipefail: falla si algún comando en pipe falla

APP_DIR="/var/www/inio_database_web"
VENV="/home/iniodeploy/inio_db_app/venv"    # SIEMPRE ruta absoluta, nunca ~
BACKUP_DIR="/var/backups/inio_db"
HEALTH_URL="http://127.0.0.1/"

# Extraer solo las vars que necesitamos, sin sourcear el .env entero
# (evita explosiones con valores tipo `DB_DRIVER={SQL Server}`)
extract_env() {
    grep -E "^$1=" "$APP_DIR/.env" | head -1 | cut -d= -f2- \
        | sed -E 's/^"(.*)"$/\1/;s/^'"'"'(.*)'"'"'$/\1/'
}
DB_NAME=$(extract_env DB_NAME)
DB_USER=$(extract_env DB_USER)
DB_PASSWORD=$(extract_env DB_PASSWORD)
# Validar temprano, no en medio del deploy
[ -z "$DB_NAME" ] && { echo "ERROR" >&2; exit 1; }

source "$VENV/bin/activate"

# ORDEN IMPORTANTE:
git pull --ff-only          # 1. Traer código nuevo
pip install -r requirements.txt   # 2. Dependencies antes de migrate
pg_dump ... -f "$BACKUP_DIR/..."  # 3. BACKUP antes de tocar la DB
python manage.py migrate --no-input  # 4. Migraciones
python manage.py check --deploy      # 5. Validaciones (exit != 0 si hay ERROR)
python manage.py collectstatic --no-input  # 6. Static
sudo systemctl reload nginx          # 7. Aplicar nueva config nginx si cambió
sudo systemctl restart gunicorn      # 8. RESTART al final, no antes

# Health check con retries — la app tarda unos segundos en levantar
for i in 1 2 3 4 5; do
    sleep 3
    code=$(curl -sS -o /dev/null -w "%{http_code}" "$HEALTH_URL" || echo "000")
    [ "$code" = "200" ] && exit 0
done
exit 1   # Si nunca respondió 200, el deploy falla visiblemente
```

**Principios detrás:**
- **Backup ANTES de mutate**: pg_dump antes de migrate. Si migrate rompe, tienes el dump.
- **Restart al final**: si algo antes falla, `set -e` aborta antes del restart. Prod sigue corriendo la versión vieja.
- **Health check como decisión pass/fail**: no basta con `restart exit 0`. La app puede arrancar y morir por config error. Solo un curl real confirma que está viva.

### `.github/workflows/deploy.yml` — el coordinador

```yaml
name: Deploy to production

on:
  push:
    branches: [main]        # Auto: cada merge a main
  workflow_dispatch:         # Manual: botón "Run workflow" en la UI para reintentar

concurrency:
  group: production-deploy
  cancel-in-progress: false  # 2 pushes seguidos = 2 deploys en cola, no cancelar el activo

jobs:
  deploy:
    runs-on: [self-hosted, linux, prod]   # Labels del runner registrado
    timeout-minutes: 15                    # Colgada → falla, no infinita

    steps:
      - name: Sync working tree to origin/main
        run: |
          cd /var/www/inio_database_web
          git fetch origin main
          git reset --hard origin/main       # Descarta cualquier edit manual en la VM
          chmod +x deploy.sh

      - name: Run deploy script
        run: /var/www/inio_database_web/deploy.sh
```

**Por qué el paso de sync es crítico:** si alguien edita un archivo directamente en la VM (por ejemplo con `vim deploy.sh`), git ve local mods y `git pull --ff-only` puede fallar. `reset --hard origin/main` garantiza estado limpio en cada deploy.

---

## 4. Checklist de setup para un proyecto nuevo

Orden estricto — algunos pasos dependen del anterior.

### Antes de escribir CI/CD (pre-requisitos en la VM)

- [ ] Django corre bajo systemd (gunicorn.service), no manualmente.
- [ ] Nginx sirve gunicorn vía unix socket.
- [ ] Postgres local con user/pass en `.env`.
- [ ] Repo git clonado en `/var/www/<proyecto>` con usuario dedicado (ej. `deployer`).
- [ ] `.env` en el repo path, permisos 644 (readable por el user).

### Preparar VM para CI/CD

- [ ] `sudo mkdir /var/backups/<proyecto> && sudo chown <user>:<user> /var/backups/<proyecto>`
- [ ] Crear `/etc/sudoers.d/deploy-runner`:
  ```
  <user> ALL=(root) NOPASSWD: /usr/bin/systemctl reload nginx, /usr/bin/systemctl restart gunicorn
  ```
  → `sudo chmod 440 /etc/sudoers.d/deploy-runner && sudo visudo -c`
- [ ] Probar: `sudo -n /usr/bin/systemctl reload nginx` (debe no pedir password).

### Instalar self-hosted runner

- [ ] Ir a `github.com/<org>/<repo>/settings/actions/runners/new` → generar token.
- [ ] En la VM como `<user>`:
  ```bash
  mkdir ~/actions-runner && cd ~/actions-runner
  # curl + tar (los pasos que muestra GitHub)
  ./config.sh --url https://github.com/<org>/<repo> --token XXX \
              --name <vm-name> --labels self-hosted,linux,prod \
              --unattended --replace
  sudo ./svc.sh install <user>
  sudo ./svc.sh start
  ```
- [ ] Verificar en GitHub UI: runner aparece **Idle**.

### Agregar archivos al repo

- [ ] `deploy.sh` en la raíz (adaptar paths).
- [ ] `.github/workflows/deploy.yml` (labels deben coincidir con el runner).
- [ ] Commit + push.

### Primera prueba

- [ ] En Actions, disparar `workflow_dispatch` manualmente antes de confiar en el push automático.
- [ ] Verificar backup nuevo en `/var/backups/`, health check pasando.

---

## 5. Los 6 pitfalls que encontramos (y cómo evitarlos)

| # | Pitfall | Prevención |
|---|---|---|
| 1 | `deploy.sh` viejo con `source ~/venv/bin/activate` (path mal) | **Siempre rutas absolutas en scripts de servicio.** El `~` depende de quién ejecuta. |
| 2 | Sourcing `.env` con `. .env` explota con `DB_DRIVER={SQL Server}` (bash brace expansion) | **No sourcees `.env` completo en bash.** Extrae solo las vars que necesites con grep. O usa python-dotenv desde el venv activo. |
| 3 | Chicken-and-egg: primer deploy usa el script viejo | **Agrega step de sync al workflow** (`git reset --hard origin/main`) o actualiza el script manualmente en la VM antes del primer push. |
| 4 | Migraciones aplicadas en prod pero nunca commiteadas a git | **Disciplina de commit:** `makemigrations` genera archivos → esos archivos son código → deben commitearse ANTES de que el código que los requiere llegue a prod. |
| 5 | `config/settings.py` (archivo) y `config/settings/` (paquete) coexistiendo | **Cuando refactorices a settings modular, elimina el archivo viejo.** Python prefiere silenciosamente el paquete → tu edit al archivo no surte efecto → días perdidos. |
| 6 | Activar HSTS sin HTTPS = usuarios bloqueados 1 año | **Nunca actives `SECURE_HSTS_SECONDS` hasta tener HTTPS estable.** HSTS es un compromiso a nivel navegador que no puedes revertir del server. |

---

## 6. Ciclo de vida de un deploy

```
1. git push origin main
   │
   ▼
2. GitHub recibe commits, evalúa workflow triggers
   │
   ▼
3. GitHub encola job → runner de la VM lo recoge (~2-5s)
   │
   ▼
4. Runner ejecuta step "Sync working tree":
   git fetch origin main
   git reset --hard origin/main    ← código nuevo en disco
   │
   ▼
5. Runner ejecuta step "Run deploy script":
   deploy.sh corre en la VM como <user>
   │
   ├─ pg_dump backup
   ├─ pip install (idempotente si no hay cambios)
   ├─ migrate     ← si falla aquí, prod sigue corriendo versión vieja
   ├─ check --deploy
   ├─ collectstatic
   ├─ reload nginx + restart gunicorn   ← momento del "corte"
   └─ health check (5 intentos × 3s = ~15s)
   │
   ▼
6. Exit code → GitHub UI check verde/rojo
   Notificación por email si falla (config default de GitHub)
```

**Downtime esperado:** ~2-5 segundos durante `restart gunicorn`. Aceptable para apps internas. Para prod público, se necesita blue-green o rolling restart (fuera de este scope).

---

## 7. Estrategia de rollback

**Código malo pero DB OK:**

```bash
git revert <sha_malo>
git push
# Auto-deploy con reversión aplica solo
```

**Migración destructiva:**

```bash
# En la VM, restaurar el dump previo:
ls -lt /var/backups/<proyecto>/    # último dump antes del deploy malo
pg_restore -h localhost -U <user> -d <db> --clean --if-exists <dump>
# Luego revert del código como arriba
```

Los backups viven 14 rotaciones (~2 semanas si deployeas a diario). Suficiente para descubrir bugs de migración.

---

## 8. Qué falta para producción "real"

- **HTTPS con Let's Encrypt** (o cert interno de ACP). Prerrequisito para HSTS y secure cookies.
- **Logging centralizado**: gunicorn/nginx logs a Azure Log Analytics o similar.
- **Monitoring/alertas**: uptime check externo + Prometheus/Grafana para métricas.
- **Blue-green o rolling deploys** si el downtime de 2-5s no es tolerable.
- **Secrets management**: Azure Key Vault en vez de `.env` en disco. Los env vars se inyectan al proceso, no viven en filesystem.
- **Tests en CI**: correr `pytest` en un runner de GitHub-hosted (no self-hosted) antes de mergear a main. El self-hosted solo despliega.

---

## 9. Reglas de oro (para pegar en tu pared)

1. **Migraciones se commitean apenas se generan**, siempre. Sin excepciones.
2. **Rutas absolutas** en cualquier script que corra bajo systemd o cron.
3. **Backup antes de mutate**, siempre. La operación es barata; recuperarse sin backup no lo es.
4. **Restart al final**. Si algo antes falla, la versión vieja sigue viva.
5. **Health check como pass/fail**. Un `systemctl restart` que "no da error" no significa que la app funciona.
6. **Least privilege** en sudoers. Nunca `ALL=(ALL) NOPASSWD:ALL` para un runner.
7. **Separa workflow (coordina) de deploy.sh (ejecuta)**. Testeable por separado.
8. **No sourcees `.env` con bash**. Extrae con grep o usa python-dotenv.
9. **Cuando refactorices settings, elimina el archivo viejo**. Python te va a engañar en silencio.
10. **HSTS solo después de HTTPS estable**. Nunca antes.

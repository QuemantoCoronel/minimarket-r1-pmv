# Evidencia de Ejecución — `S1-PLAT-01` (`SCRUM-290`)

- **Responsable:** D6 — Jhonny Angeles
- **Fecha/Hora (America/Lima):** 2026-10-10 22:03
- **Estado actual:** `VALIDADO EN LOCAL / BLOQUEADO EN REMOTO` (Entorno Docker Compose levantado y verificado desde limpio; pendiente enlace al repositorio remoto de GitHub y fusión con `S1-ARQ-01`).

## 1. Archivos Creados / Modificados
- `Dockerfile`: Imagen base `python:3.12-slim` con `tzdata` (`America/Lima`), `libpq-dev` y `postgresql-client`.
- `.dockerignore`: Exclusión de `.env`, caché, entorno virtual y artefactos locales.
- `docker-compose.yml`: Servicios `db` (`postgres:17-alpine` con `healthcheck` activo) y `web` (espera activa a `manage.py` de `S1-ARQ-01` y ejecución automática de migraciones).
- `.env.example`: Plantilla de configuración externalizada sin secretos.
- `.github/pull_request_template.md`: Plantilla de PR y checklist de revisión alineado con CA/RN/NFR.
- `docs/plataforma/GUIA_ARRANQUE_Y_RAMAS.md`: Guía de arranque limpio, comandos coordinados con CI/migraciones y reglas de ramas protegidas.

## 2. Contrato Entregado a `D3` (CI) y `D4` (Entorno)
- **Variables requeridas (`.env.example`):** `TZ=America/Lima`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST=db`, `POSTGRES_PORT=5432`, `DATABASE_URL`.
- **Servicios levantados:** `db` (`postgres:17-alpine`, puerto `5432`) y `web` (`python:3.12-slim`, puerto `8000`).

## 3. Pruebas Ejecutadas y Resultado Real (Consola Local)

Salida real obtenida al construir y verificar contenedores:
```text
NAME                       IMAGE                   COMMAND                  SERVICE   STATUS                    PORTS
r1-pmv-d6-angeles-db-1     postgres:17-alpine      "docker-entrypoint.s…"   db        Up (healthy)              0.0.0.0:5432->5432/tcp
r1-pmv-d6-angeles-web-1    r1-pmv-d6-angeles-web   "sh -c 'if [ -f mana…"   web       Up                        0.0.0.0:8000->8000/tcp

Python 3.12.15

   TimeZone   
--------------
 America/Lima
(1 row)
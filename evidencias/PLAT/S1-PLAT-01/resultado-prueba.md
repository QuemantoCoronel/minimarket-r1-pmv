# Resultado de Prueba y Consolidación — `S1-PLAT-01` (`SCRUM-290`)

- **Responsable:** Jhonny Luis Angeles Pérez (`D6`)
- **Revisor:** Favio Adriano Velasquez Revilla (`D1`)
- **Rama:** `chore/SCRUM-290-integrar-base-django` (creada desde `origin/main`)
- **Estado:** **VALIDADO (OK)**

## 1. Preflight y Consolidación
- `origin`: `https://github.com/QuemantoCoronel/minimarket-r1-pmv.git`
- Docker Engine `29.7.2` y Docker Compose `v5.5.1`.
- Se conservó íntegramente el historial de `origin/main` (sin `force push`) e integró la base Django real (`app_platform`, `identity`, `catalog`, `cash`, `config`, `manage.py`).
- Se unificó la configuración en `compose.yaml`, `Dockerfile`, `.env.example` y el runner oficial `python manage.py test`.
- Se agregó `.gitattributes` (`*.sh text eol=lf`) y se normalizó `db/init/01-create-runtime-roles.sh` a `LF` para garantizar compatibilidad en entornos Windows/Docker.
- Se retiraron de la raíz los prototipos aislados (`docker-compose.yml`, `templates/` y `tests/` simulados).

## 2. Verificación Ejecutada en Docker y PostgreSQL 17
1. **Chequeo de sistema (`python manage.py check`):**
   `System check identified no issues (0 silenced).`
2. **Migraciones y Semillas en PostgreSQL 17 (`migrate` + `seed_pmv`):**
   Todas las migraciones aplicadas (`OK`) y datos base asegurados (`PMV baseline data ensured: 3 roles, 4 fictional accounts, 1 category, 1 cash register`).
3. **Suite oficial de pruebas (`python manage.py test -v 2`):**
   `Ran 13 tests — OK` (verificado tanto en memoria como contra PostgreSQL 17 real).

# Guía de Arranque Limpio, Flujo de Revisión y Ramas Protegidas (`S1-PLAT-01`)

## 1. Requisitos Previos
- Docker Engine 24+ y Docker Compose v2.
- Git 2.40+.

## 2. Arranque desde Limpio (Zero-to-Running)

1. Preparar variables de entorno:
   `cp .env.example .env`
2. Eliminar volúmenes previos (para garantizar BD vacía al probar desde cero):
   `docker compose down -v --remove-orphans`
3. Construir imágenes sin caché y levantar servicios:
   `docker compose build --no-cache`
   `docker compose up -d`
4. Verificar estado de salud de PostgreSQL 17 y aplicación:
   `docker compose ps`

## 3. Comandos Coordinados con Migraciones (`D2`), CI (`D3`) y Entorno (`D4`)
*(Nota: Estos comandos están documentados para ejecutarse una vez que se integre el esqueleto Django de `S1-ARQ-01`)*:

- Ejecutar migraciones manualmente:
  `docker compose exec -T web python manage.py migrate --noinput`
- Verificar migraciones pendientes (Check para CI `D3`):
  `docker compose exec -T web python manage.py makemigrations --check --dry-run`
- Ejecutar seeds / carga base (cuando `S1-DB-04` esté integrado):
  `docker compose exec -T web python manage.py seed_initial_data`
- Ejecutar suite de pruebas automatizadas:
  `docker compose exec -T web pytest`

## 4. Recomendaciones de Ramas Protegidas en GitHub (`main` / `develop`)

> **Nota de transparencia (`S1-PLAT-01`):** Estas reglas quedan documentadas y listas para aplicar por el administrador del repositorio en GitHub (`Settings -> Branches -> Add branch ruleset`). No se declaran activas remotamente hasta contar con el repositorio y permisos de administración.

### Reglas para la rama `main` (y `develop` si se usa rama de integración):
1. **Require a pull request before merging:** Activado (Mínimo 1 aprobación humana/revisor independiente `*-REV` y `Dismiss stale pull request approvals when new commits are pushed`).
2. **Require status checks to pass before merging:** Activado (Job de build + migraciones en limpio + tests automatizados de `S1-CI-01`).
3. **Require conversation resolution before merging:** Activado.
4. **Do not allow bypassing the above settings:** Activado.
5. **Block force pushes & Restrict deletions:** Activado.

### Convención de Ramas y Commits
- **Ramas de trabajo:** `feat/S1-XXX-XX`, `chore/S1-PLAT-01`, `test/S1-XXX-XX`, `fix/S1-XXX-XX`.
- **Commit de esta tarea:** `chore(S1-PLAT-01): preparar entorno reproducible y flujo de revision`
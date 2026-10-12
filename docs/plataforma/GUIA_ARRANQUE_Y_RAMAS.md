# Guía de Arranque Limpio, Flujo de Revisión y Ramas (`S1-PLAT-01` / `SCRUM-290`)

## 1. Requisitos Previos
- Docker Engine 24+ y Docker Compose v2 (`compose.yaml`).
- Git 2.40+.

## 2. Arranque desde Limpio con Docker y PostgreSQL 17

1. Preparar variables de entorno locales desde la plantilla (sin subir `.env` a Git):
   `Copy-Item .env.example .env` (completar secretos locales en `.env`).
2. Eliminar volúmenes previos para garantizar base de datos vacía:
   `docker compose down -v --remove-orphans`
3. Construir imágenes e iniciar PostgreSQL 17:
   `docker compose build`
   `docker compose up -d db`
4. Ejecutar migraciones con el rol migrador:
   `docker compose --profile tools run --rm migrate`
5. Sembrar cuentas iniciales (idempotente) y levantar el servidor web:
   `docker compose run --rm -e DATABASE_URL="" web python manage.py check`
   `docker compose up -d web`

## 3. Comandos Estándar de Verificación y Pruebas (Runner Único)

- Verificar configuración del proyecto Django:
  `docker compose run --rm -e DATABASE_URL="" web python manage.py check`
- Ejecutar suite oficial de pruebas de Django (runner único del repositorio):
  `docker compose run --rm -e DATABASE_URL="" web python manage.py test -v 2`
- Verificar que no existan migraciones pendientes:
  `docker compose run --rm -e DATABASE_URL="" web python manage.py makemigrations --check --dry-run`
- Ejecutar semillas base (`seed_pmv`):
  `docker compose run --rm web python manage.py seed_pmv`

## 4. Reglas de Ramas e Integración (`main`)
1. **Ramas de trabajo:** Crear siempre desde `origin/main` usando el formato `tipo/SCRUM-123-descripcion-corta`.
2. **Pull Request obligatorio:** Revisión cruzada antes de integrar a `main`, sin secretos y pasando `python manage.py check` y `python manage.py test`.
3. **Prohibido `force push`:** No reescribir historial en `main` ni crear proyectos paralelos.

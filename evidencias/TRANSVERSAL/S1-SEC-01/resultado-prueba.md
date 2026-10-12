# Evidencia — S1-SEC-01 · SCRUM-297

**Título:** Externalizar secretos, roles de BD y separación de ambientes  
**Fecha de actualización:** 2026-10-12  
**Estado recomendado:** `En curso` — no mover a `Finalizada` todavía.

## Entregado

- [`.env.example`](../../../.env.example) sin claves ni contraseñas reales, con variables para aplicación, PostgreSQL, migraciones y semillas.
- [`.gitignore`](../../../.gitignore) excluye `.env`, `.venv`, SQLite local, logs y artefactos de cobertura.
- [`config/env.py`](../../../config/env.py) carga `.env` local sin sobrescribir variables reales del proceso y valida tipos/URLs.
- [`config/settings.py`](../../../config/settings.py) separa `local`, `test`, `demo` y `production`; el perfil de pruebas usa SQLite aislado y el de demo rechaza `DJANGO_DEBUG=true`.
- [`compose.yaml`](../../../compose.yaml) y [`db/init/01-create-runtime-roles.sh`](../../../db/init/01-create-runtime-roles.sh) definen PostgreSQL 17, un usuario de migraciones y uno de aplicación con privilegios separados.
- [`app_platform/test_env.py`](../../../app_platform/test_env.py) verifica que el proceso tenga prioridad sobre `.env`, que se rechacen booleanos inválidos, que el perfil SQLite sea local y que solo se acepten URLs PostgreSQL.
- `db/init/01-create-runtime-roles.sh` revoca acceso público a la base/esquema y privilegios por defecto sobre tablas/secuencias antes de conceder DML al usuario de aplicación.
- [Guía de seguridad](../../../docs/seguridad.md) y [README](../../../README.md) documentan uso, rotación y límites de los secretos.

## Verificación real

```powershell
git check-ignore .env .venv\Scripts\python.exe
```

Salida real:

```text
.env
".venv\\Scripts\\python.exe"
```

La suite local pasó después de estos cambios:

```text
$env:APP_ENV='test'
.\.venv\Scripts\python.exe manage.py test
Found 13 test(s).
Ran 13 tests in 1.312s
OK
```

También pasó:

```text
.\.venv\Scripts\python.exe manage.py check
System check identified no issues (0 silenced).
```

## Pendiente / bloqueo

Docker y PostgreSQL 17 no están instalados en el equipo. Por tanto, **no se ejecutó** Compose ni se verificaron roles/permisos efectivos contra un servidor PostgreSQL. Falta esa evidencia antes de cerrar la subtarea.

## Contrato de integración

- La aplicación usa `DATABASE_URL`; el servicio de migración usa `MIGRATIONS_DATABASE_URL` como rol con DDL.
- La aplicación web usa el usuario limitado de `DATABASE_URL`, sin permisos de migración.
- `.env` nunca se versiona. Toda clave se inyecta por entorno o almacén autorizado.

**Commit sugerido:** `chore(S1-SEC-01): externalizar secretos y separar ambientes`

# Evidencia — S1-SEC-01 · SCRUM-297

**Título:** Externalizar secretos, roles de BD y separación de ambientes  
**Fecha de actualización:** 2026-10-12  
**Estado recomendado:** `Finalizada`.

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

### Revalidación local — 2026-10-12 14:07 (America/Lima)

Se ejecutó nuevamente, con `APP_ENV=test` y una clave efímera de auditoría:

```powershell
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py check
```

Resultado real: `Ran 13 tests ... OK`; el chequeo de Django no reportó problemas.
Durante las pruebas aparecen respuestas `403` esperadas de los casos de autorización;
la suite terminó correctamente. También se verificó que `.env` no existe en el espacio
de trabajo y permanece ignorado por Git.

### Validación efectiva en PostgreSQL — 2026-10-12 14:35–14:40 (America/Lima)

Se creó un clúster desechable de PostgreSQL 18.4 en `D:\r1-pmv-pg18-test`,
aislado del servicio PostgreSQL existente, y se ejecutó dos veces el script real
`db/init/01-create-runtime-roles.sh`. Después se aplicaron todas las migraciones
de Django con `pmv_migrator` y se accedió al esquema con `pmv_app`.

Resultados observados:

```text
pmv_app: superuser=false, createdb=false, createrole=false
pmv_migrator: superuser=false, createdb=false, createrole=false
app_schema_usage=true
app_schema_create=false
app_identity_dml=true
app_sequence_usage=true
public_schema_create=false
migrator_table_owner=14
```

La prueba negativa `CREATE TABLE forbidden_probe(id integer)` ejecutada como
`pmv_app` falló con `permission denied for schema public` y código de salida 1.
El mismo rol pudo insertar, consultar, actualizar y eliminar una fila de una tabla
creada por `pmv_migrator`. La segunda ejecución del script terminó sin errores.

También se ejecutaron desde el entorno virtual ubicado en D:

```text
python manage.py migrate --noinput: OK (PostgreSQL, rol pmv_migrator)
python manage.py showmigrations --plan: todas aplicadas (rol pmv_app)
python manage.py test: 13 pruebas, OK
python manage.py check: sin problemas
secret_scan=clean
```

Docker Desktop sigue sin estar operativo por un problema local de WSL2, pero ya
no bloquea la aceptación de esta subtarea: los privilegios fueron comprobados
contra un servidor PostgreSQL real ejecutando el mismo script montado por Compose.

## Contrato de integración

- La aplicación usa `DATABASE_URL`; el servicio de migración usa `MIGRATIONS_DATABASE_URL` como rol con DDL.
- La aplicación web usa el usuario limitado de `DATABASE_URL`, sin permisos de migración.
- `.env` nunca se versiona. Toda clave se inyecta por entorno o almacén autorizado.

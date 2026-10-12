# R1-PMV

Monolito modular para el recorrido interno de una bodega: autenticación, catálogo, inventario por lotes, caja, ventas y constancias. Esta primera base entrega configuración segura, identidad/autorización y semillas; los casos de negocio se integran por sus subtareas.

## Requisitos

- Python 3.13 para la imagen de demostración; Python 3.12 funciona para la verificación local de esta base.
- Docker Compose y PostgreSQL 17 para ejecutar la topología de demostración.

## Arranque local sin secretos reales

1. Cree su `.env` privado desde `.env.example` y genere un `DJANGO_SECRET_KEY` local. El proyecto lo carga sin sobrescribir variables definidas por el sistema. No suba ese archivo.
2. Para las verificaciones locales, puede dejar `DATABASE_URL` vacío para usar SQLite. Exporte una clave solo en la sesión actual de PowerShell:

   ```powershell
   $env:DJANGO_SECRET_KEY = [guid]::NewGuid().ToString('N')
   .\.venv\Scripts\python.exe manage.py migrate
   ```

3. Defina las tres variables `SEED_*_PASSWORD` solo en su sesión o `.env` privado y ejecute:

   ```powershell
   .\.venv\Scripts\python.exe manage.py seed_pmv
   .\.venv\Scripts\python.exe manage.py runserver
   ```

La salida del comando de semillas no muestra contraseñas. Las cuentas ficticias usan los correos `admin.demo@pmv.invalid`, `almacen.demo@pmv.invalid`, `vendedor.demo@pmv.invalid` e `inactiva.demo@pmv.invalid`.

## PostgreSQL y roles mínimos

1. Complete en `.env` las credenciales de bootstrap, migración y aplicación, y ambas URLs PostgreSQL. No use valores de ejemplo como credenciales reales.
2. Inicie PostgreSQL: `docker compose up -d db`.
3. Aplique el esquema con el rol migrador: `docker compose --profile tools run --rm migrate`.
4. Inicie la aplicación con el rol limitado: `docker compose up web`.

`pmv_migrator` puede crear objetos de esquema. `pmv_app` solo recibe conexión, uso de esquema y los permisos DML/sequence que el migrador otorga por defecto; no debe ejecutar migraciones.

## Verificación

```powershell
$env:DJANGO_SECRET_KEY = 'test-only-key'
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py check --deploy
```

El segundo comando reportará controles que exigen HTTPS si se corre en local; eso es esperado. En `APP_ENV=demo` o `production`, se activan HTTPS/HSTS y cookies seguras; `DJANGO_DEBUG=true` se rechaza al iniciar.

## Límites actuales

- `HU-AUTH-01`: servicio de login, sesión de servidor y autorización por rol están implementados y probados.
- `HU-AUTH-03`: invalidación de sesión está implementada; el descarte atómico de borrador se integrará cuando exista el módulo `sales` y su modelo de borrador.
- Los enlaces protegidos de producto, inventario, caja y ventas son contratos de autorización; aún no contienen sus casos de negocio.

Consulte [docs/seguridad.md](docs/seguridad.md) para las decisiones de seguridad y el traspaso para el equipo.

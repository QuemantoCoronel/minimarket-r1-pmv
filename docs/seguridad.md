# Baseline de seguridad e integración de D5

## Configuración y secretos

- `.env` está ignorado por Git; `.env.example` publica solamente nombres de variables y valores no sensibles.
- `DJANGO_SECRET_KEY` se exige desde el entorno. No hay clave de demostración incrustada en el repositorio.
- Las contraseñas de las cuentas ficticias se reciben al ejecutar `seed_pmv`; no se guardan en modelos, salida, documentación ni commits.
- En `demo` y `production`, no se permite `DJANGO_DEBUG=true`, se exige HTTPS/HSTS y las cookies de sesión/CSRF requieren HTTPS. El proxy debe enviar `X-Forwarded-Proto: https`.
- Los logs aplican una capa de redacción para claves, tokens, cookies, sesiones y CSRF. No se debe registrar un formulario completo ni objetos `request.POST`.

## Identidad y autorización

`Account` tiene una FK obligatoria a `Role`; los únicos códigos sembrados son `ADMIN`, `ALMACENERO` y `VENDEDOR`. El servicio normaliza el correo, verifica el hash Argon2 y el estado activo, y devuelve el mismo mensaje para correo inexistente, contraseña incorrecta o cuenta inactiva.

La autorización se aplica en servidor con `roles_required`, además de ocultar las opciones no permitidas en el menú. Una sesión ausente redirige al ingreso; una sesión autenticada sin rol permitido recibe `403` y no ejecuta el caso de uso.

| Operación | Rol permitido | Contrato de ruta actual |
|---|---|---|
| Registrar producto | `ADMIN` | `/productos/nuevo/` |
| Carga inicial | `ALMACENERO` | `/inventario/carga-inicial/` |
| Abrir turno / ventas | `VENDEDOR` | `/caja/abrir/`, `/ventas/` |

Los módulos que implementen esas operaciones deben conservar los decoradores y volver a validar `request.user` dentro de su servicio transaccional. Nunca aceptarán `role`, `seller_id`, `account_id` o `shift_id` del navegador como autoridad.

## Base de datos

La topología Compose mantiene PostgreSQL unido a `127.0.0.1`, no expuesto a Internet. El bootstrap crea dos usuarios de runtime:

- `pmv_migrator`: conexión, uso y creación de objetos de esquema; solo el servicio `migrate` lo utiliza.
- `pmv_app`: conexión, uso de esquema y permisos DML otorgados por defecto sobre tablas/secuencias creadas por el migrador; lo utiliza `web`.

El usuario `POSTGRES_USER` existe únicamente para inicializar el clúster. Su contraseña, las de los roles runtime y las URLs quedan solo en `.env`. Revocar o rotar un secreto implica actualizar el almacén de secretos/`.env` autorizado y reiniciar los servicios; nunca editar archivos versionados.

## Semillas

`seed_pmv` es transaccional e idempotente: puede ejecutarse dos veces sin duplicar roles, cuatro cuentas ficticias, la categoría activa `Productos enlatados` ni `CAJA-01`. Requiere variables de contraseña solo porque las cuentas se crean con hash seguro. No lo ejecute contra un ambiente no autorizado.

## Checklist manual antes de demostración

- [ ] `.env` no aparece en `git status` ni en el commit.
- [ ] Se usa una `DJANGO_SECRET_KEY` única para cada ambiente.
- [ ] PostgreSQL no publica el puerto fuera de `127.0.0.1`.
- [ ] `migrate` usa la URL de migraciones y `web` la URL limitada de aplicación.
- [ ] Las pruebas de login cubren correo/clave/inactividad con mensaje uniforme.
- [ ] Las operaciones sensibles tienen prueba de solicitud directa denegada y sin mutación.
- [ ] Los módulos de ventas implementan el descarte de borrador en `AUTH-03` antes de declararlo terminado.

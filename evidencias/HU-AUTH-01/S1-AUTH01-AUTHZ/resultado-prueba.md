# Evidencia — S1-AUTH01-AUTHZ · SCRUM-307

**HU:** HU-AUTH-01 · Ingresar con mi cuenta de trabajo
**Inicio real:** 2026-10-12T15:32:49-05:00
**Fin real:** 2026-10-12T15:33:30-05:00
**Responsable:** Walter Luis Colonia Infantas (D5)
**Estado:** Completada

## Implementación entregada

[`identity/authorization.py`](../../../identity/authorization.py) — decorador `roles_required(*allowed_roles)`.

### Matriz de autorización aplicada en servidor

| Operación | Rol requerido | Ruta |
|---|---|---|
| Registrar producto | `ADMIN` | `/productos/nuevo/` |
| Carga inicial de inventario | `ALMACENERO` | `/inventario/carga-inicial/` |
| Abrir turno | `VENDEDOR` | `/caja/abrir/` |
| Ventas | `VENDEDOR` | `/ventas/` |

### Comportamiento del decorador

- **Sesión ausente:** redirige al login (`redirect_to_login`), no devuelve 403.
- **Sesión presente, rol incorrecto:** lanza `PermissionDenied` → respuesta 403. No ejecuta el cuerpo de la vista ni muta datos.
- **Sesión presente, rol correcto:** ejecuta la vista normalmente.

### Menú en dashboard

`identity/templates/identity/dashboard.html` oculta las opciones según el rol. Esta restricción es de UX, **no** es la autorización decisiva — la autorización real ocurre en el decorador de servidor.

## Pruebas ejecutadas

```
python manage.py test identity --verbosity=2
APP_ENV=test  DJANGO_SECRET_KEY=local-test-key

test_direct_operation_is_denied_without_mutating_data ... ok
  (ALMACENERO → /productos/nuevo/ → 403, conteo de cuentas sin cambio)

test_role_matrix_is_enforced_on_direct_urls ... ok
  (cada rol × cada ruta: 200 solo para su operación permitida, 403 para las demás)

test_dashboard_only_shows_authorized_navigation ... ok
  (VENDEDOR ve "Abrir turno", no ve "Registrar producto" ni "Carga inicial")

Ran 17 tests in 3.223s
OK
```

Los `Forbidden (Permission denied)` visibles en la salida son trazas de log esperadas de los casos negativos. No son fallos.

### manage.py check

```
System check identified no issues (0 silenced).
```

## Resultado

**Completada ✅** — Autorización por rol aplicada en servidor. Matriz de 4 rutas verificada con pruebas automatizadas. El menú refleja los permisos pero no es la guardia decisiva.

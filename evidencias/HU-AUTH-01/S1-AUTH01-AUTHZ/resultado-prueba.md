# Evidencia — S1-AUTH01-AUTHZ · SCRUM-307

**HU:** HU-AUTH-01 · Ingresar con mi cuenta  
**Fecha/hora:** 2026-10-11 23:40:16 -05:00  
**Estado recomendado:** `En progreso`.

## Entregado

[`identity/authorization.py`](../../../identity/authorization.py) entrega el decorador `roles_required`. La matriz inicial aplicada en servidor es:

| Operación | Rol | Ruta |
|---|---|---|
| Registrar producto | `ADMIN` | `/productos/nuevo/` |
| Carga inicial | `ALMACENERO` | `/inventario/carga-inicial/` |
| Abrir turno / ventas | `VENDEDOR` | `/caja/abrir/`, `/ventas/` |

Una sesión ausente es redirigida al login; una sesión existente sin rol válido recibe `403`. El menú de [`dashboard.html`](../../../identity/templates/identity/dashboard.html) refleja los permisos, pero no constituye la autorización decisiva.

## Prueba real

- `test_direct_operation_is_denied_without_mutating_data`: una cuenta `ALMACENERO` accedió directamente a la ruta de producto, recibió `403` y el conteo de cuentas no cambió.
- `test_role_matrix_is_enforced_on_direct_urls`: cada rol se probó contra las tres rutas y solo recibió `200` en su operación permitida.

Los `Forbidden (Permission denied)` visibles en salida son resultados esperados de casos negativos. La suite completa terminó `OK`.

## Pendiente / bloqueo

Las rutas protegidas de producto, inventario, caja y ventas son placeholders de integración, no casos de negocio completos. Cuando existan sus servicios, deben reaplicar la validación con el usuario autenticado y añadir pruebas de que no mutan sus propios modelos. No marcar `Hecho` hasta entonces.

**Commit sugerido:** `feat(S1-AUTH01-AUTHZ): aplicar autorizacion por rol en servidor`


# Evidencia — S1-AUTH01-AUTO · SCRUM-308

**HU:** HU-AUTH-01 · Ingresar con mi cuenta de trabajo
**Inicio real:** 2026-10-12T15:32:49-05:00
**Fin real:** 2026-10-12T15:33:30-05:00
**Responsable:** Walter Luis Colonia Infantas (D5)
**Estado:** Completada

## Suite automatizada — cobertura de criterios de aceptación

| CA | Prueba | Resultado |
|---|---|---|
| CA-1: Login válido con correo en cualquier capitalización | `test_active_account_creates_server_session` | ✅ ok |
| CA-2: Correo inexistente → mensaje uniforme, sin sesión | `test_unknown_email_wrong_password_and_inactive_account_share_message` (subTest correo) | ✅ ok |
| CA-2: Contraseña incorrecta → mensaje uniforme, sin sesión | `test_unknown_email_wrong_password_and_inactive_account_share_message` (subTest clave) | ✅ ok |
| CA-3: Cuenta inactiva → mismo mensaje, sin sesión | `test_unknown_email_wrong_password_and_inactive_account_share_message` (subTest inactiva) | ✅ ok |
| CA-4: URL prohibida directa → 403, sin mutación | `test_direct_operation_is_denied_without_mutating_data` | ✅ ok |
| CA-4 (ampliada): Matriz completa 3 roles × 3 rutas | `test_role_matrix_is_enforced_on_direct_urls` | ✅ ok |
| Extra: Correo con formato inválido rechazado antes de tocar BD | `test_invalid_email_is_rejected_before_authentication` | ✅ ok |
| Extra: POST sin CSRF → 403, sesión no creada | `test_login_post_requires_csrf_and_sets_protected_cookies` | ✅ ok |
| Extra: Hash Argon2, nunca texto plano | `test_password_uses_argon2_and_is_never_stored_in_plain_text` | ✅ ok |
| Extra: Dashboard muestra solo opciones del rol | `test_dashboard_only_shows_authorized_navigation` | ✅ ok |
| Extra: Logout invalida sesión, rutas requieren re-login | `test_post_logout_invalidates_session_and_back_route_requires_login` | ✅ ok |

## Comando y resultado real

```
python manage.py test identity --verbosity=2
APP_ENV=test  DJANGO_SECRET_KEY=local-test-key
Base de datos: SQLite en memoria (aislada)

Ran 17 tests in 3.223s
OK
System check identified no issues (0 silenced).
```

## Resultado

**Completada ✅** — Los 4 criterios de aceptación de HU-AUTH-01 cubiertos con pruebas automatizadas verdes. Suite ejecutada sobre base SQLite aislada, sin secretos en evidencia.

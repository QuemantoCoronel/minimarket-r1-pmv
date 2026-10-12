# Evidencia — S1-AUTH01-SVC · SCRUM-306

**HU:** HU-AUTH-01 · Ingresar con mi cuenta de trabajo
**Inicio real:** 2026-10-12T15:32:49-05:00
**Fin real:** 2026-10-12T15:33:30-05:00
**Responsable:** Walter Luis Colonia Infantas (D5)
**Estado:** Completada

## Implementación entregada

| Archivo | Rol |
|---|---|
| [`identity/services.py`](../../../identity/services.py) | Normaliza correo con `Account.normalize_email`, verifica Argon2 con `check_password`, valida `is_active`, devuelve `INVALID_CREDENTIALS_MESSAGE` uniforme para todos los rechazos. Incluye path de tiempo constante para correos inexistentes. |
| [`identity/views.py`](../../../identity/views.py) | Vista POST+GET con CSRF; llama `authenticate_active_account` y `create_server_session`. Redirige al dashboard en éxito. |
| [`identity/models.py`](../../../identity/models.py) | `Account` con unicidad de correo exacto y normalizado, FK obligatoria a `Role`. |
| [`identity/forms.py`](../../../identity/forms.py) | `LoginForm` con `EmailField` (valida formato antes de tocar la BD). |

### Contrato de `authenticate_active_account`

- Normaliza el correo (casefold + strip).
- Si el correo no existe: ejecuta `set_password` para igualar tiempo de respuesta, retorna `AuthenticationResult(account=None)`.
- Si la cuenta está inactiva o la contraseña no coincide: retorna `AuthenticationResult(account=None)`.
- Solo en éxito: retorna `AuthenticationResult(account=account)`.
- **El mensaje de error es siempre el mismo** para los tres rechazos.

### Contrato de `create_server_session`

- Usa `django.contrib.auth.login` (rota el ID de sesión).
- Almacena solo `role_code` en sesión de servidor.
- Nunca expone contraseña, hash, ni identificador de cuenta al cliente.

## Pruebas ejecutadas

```
python manage.py test identity --verbosity=2
APP_ENV=test  DJANGO_SECRET_KEY=local-test-key

test_active_account_creates_server_session ... ok
test_unknown_email_wrong_password_and_inactive_account_share_message ... ok
test_password_uses_argon2_and_is_never_stored_in_plain_text ... ok
test_login_post_requires_csrf_and_sets_protected_cookies ... ok
test_invalid_email_is_rejected_before_authentication ... ok

(+ 12 tests de otras subtareas de identity, todos ok)

Ran 17 tests in 3.223s
OK
```

### manage.py check

```
System check identified no issues (0 silenced).
```

## Resultado

**Completada ✅** — Servicio de autenticación con mensaje uniforme, sesión de servidor y hash Argon2 verificados en suite automatizada.

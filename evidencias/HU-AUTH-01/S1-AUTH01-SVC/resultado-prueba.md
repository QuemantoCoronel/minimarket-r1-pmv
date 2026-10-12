# Evidencia — S1-AUTH01-SVC · SCRUM-306

**HU:** HU-AUTH-01 · Ingresar con mi cuenta  
**Fecha/hora:** 2026-10-11 23:40:16 -05:00  
**Estado recomendado:** `En revisión`.

## Entregado

- [`identity/services.py`](../../../identity/services.py) normaliza correo, verifica Argon2, valida cuenta activa y devuelve el mensaje único `Correo o contraseña incorrectos` para los tres rechazos.
- `create_server_session` usa `django.contrib.auth.login`, rota la sesión y registra solo el código de rol en sesión de servidor.
- [`identity/views.py`](../../../identity/views.py) expone el formulario POST con CSRF; no autentica ni decide roles en cliente.
- [`identity/models.py`](../../../identity/models.py) aplica unicidad de correo exacto y normalizado y exige un rol.

## Pruebas reales

Pruebas ejecutadas dentro de `identity.tests.AuthenticationAndAuthorizationTests`:

- `test_active_account_creates_server_session` — correo normalizado, redirect y sesión persistida.
- `test_unknown_email_wrong_password_and_inactive_account_share_message` — correo inexistente, contraseña incorrecta y cuenta inactiva con el mismo mensaje.

Resultado general: `Ran 8 tests in 1.663s` y `OK`.

## Riesgos / dependencia

La prueba usa cuentas ficticias y SQLite aislado. Falta ejecutarla en la topología PostgreSQL y CI cuando se habiliten. No se registraron claves, hashes ni cookies en la evidencia.

**Commit sugerido:** `feat(S1-AUTH01-SVC): autenticar cuentas activas con mensaje uniforme`


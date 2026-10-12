# Evidencia — S1-SEC-02 · SCRUM-298

**Título:** Baseline de seguridad de aplicación  
**Fecha/hora de cierre:** 2026-10-12 (America/Lima)
**Estado recomendado:** `Finalizada`.

## Entregado

- Hash principal Argon2 y sesión de Django del lado servidor en [`config/settings.py`](../../../config/settings.py).
- Cookies `HttpOnly`, `SameSite=Lax`, CSRF nativo, `X-Frame-Options: DENY`, `nosniff` y política de referer.
- En `demo`/`production`: HTTPS obligatorio, HSTS y cookies seguras; soporte explícito para proxy mediante `X-Forwarded-Proto`.
- Filtro de redacción para contraseña, token, CSRF, cookie y sesión en [`app_platform/logging.py`](../../../app_platform/logging.py).
- Autorización centralizada de servidor en [`identity/authorization.py`](../../../identity/authorization.py); ninguna ruta protegida confía en ocultar enlaces.

## Verificación real

El chequeo de seguridad de Django en perfil demo terminó sin avisos:

```text
System check identified no issues (0 silenced).
```

La suite local ejecutó casos de acceso directo prohibido y recibió `403` esperado sin mutar el conteo de cuentas.

Se agregaron casos negativos explícitos para:

- Hash Argon2 y ausencia de contraseña en texto plano.
- Rechazo de login sin token CSRF y aceptación con token válido.
- Cookies de sesión y CSRF con `HttpOnly` y `SameSite=Lax`.
- Rechazo de correo con formato inválido antes de autenticar.
- Redacción de contraseñas, tokens CSRF, identificadores de sesión y cabeceras `Authorization` en formatos query, JSON y encabezados HTTP.
- Matriz de autorización directa con respuesta `403` para roles no permitidos.

La prueba de correo inválido detectó que la plantilla no mostraba errores de campo;
se corrigió `identity/templates/identity/login.html` para presentarlos.

Resultado final:

```text
python manage.py test
Found 18 test(s).
Ran 18 tests in 1.287s
OK

python manage.py check
System check identified no issues (0 silenced).

APP_ENV=demo python manage.py check --deploy
System check identified no issues (0 silenced).
```

## Límite del baseline

La subtarea define y prueba el baseline disponible en el Sprint 1. Cuando producto,
carga, caja y venta incorporen nuevos formularios o servicios transaccionales, sus
propias subtareas deberán conservar este baseline y añadir pruebas negativas específicas.
Ese trabajo futuro no invalida el baseline ya comprobado aquí.

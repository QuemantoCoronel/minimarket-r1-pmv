# Evidencia — S1-SEC-02 · SCRUM-298

**Título:** Baseline de seguridad de aplicación  
**Fecha/hora:** 2026-10-11 23:40:16 -05:00  
**Estado recomendado:** `En progreso` — baseline implementado; falta cobertura cuando se integren todos los módulos.

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

La suite local ejecutó casos de acceso directo prohibido y recibió `403` esperado sin mutar el conteo de cuentas. Resultado total: `8` pruebas, `OK`.

## Pendiente / límite

No se puede cerrar como seguridad integral mientras producto, carga, caja y venta sean contratos de ruta sin sus servicios de negocio. Al integrarlos, cada operación debe conservar la autorización en vista **y** validarla de nuevo en su servicio transaccional. Falta también una prueba HTTP explícita de CSRF contra formularios de los módulos futuros.

**Commit sugerido:** `feat(S1-SEC-02): establecer baseline de seguridad de aplicacion`


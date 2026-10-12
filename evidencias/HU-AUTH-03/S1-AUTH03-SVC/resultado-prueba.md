# Evidencia parcial — S1-AUTH03-SVC · SCRUM-312

**HU:** HU-AUTH-03 · Salir de mi cuenta  
**Fecha/hora:** 2026-10-11 23:40:16 -05:00  
**Estado recomendado:** `Bloqueado`.

## Único comportamiento entregado

[`identity/views.py`](../../../identity/views.py) implementa confirmación de salida por POST con CSRF, invalida la sesión usando `django.contrib.auth.logout` y redirige al login.

Prueba real: `test_post_logout_invalidates_session_and_back_route_requires_login` verificó que, tras POST de salida, no permanece `_auth_user_id` en la sesión y una URL de ventas exige login nuevamente. Resultado: aprobado dentro de una suite de 8 pruebas.

## No entregado — no cerrar la subtarea

No existen todavía modelos/servicios de borrador de venta ni turno. Por tanto, no se implementó ni probó:

- advertencia y confirmación con líneas de borrador;
- descarte atómico de líneas sin modificar stock/caja;
- preservación de turno y propiedad del vendedor;
- reingreso del propietario y bloqueo de otro vendedor.

La dependencia real es la integración de `sales` y `cash` (borrador y turno). Esta ficha se adjunta solo para trazabilidad del logout básico, no como evidencia de cumplimiento de CA 1–3.

**Commit sugerido para el avance parcial:** `feat(S1-AUTH03-SVC): invalidar sesion de forma segura`


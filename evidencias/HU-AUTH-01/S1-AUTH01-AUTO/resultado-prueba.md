# Evidencia — S1-AUTH01-AUTO · SCRUM-308

**HU:** HU-AUTH-01 · Ingresar con mi cuenta  
**Fecha/hora:** 2026-10-11 23:40:16 -05:00  
**Estado recomendado:** `En revisión`.

## Cobertura automatizada ejecutada

| CA | Prueba | Resultado |
|---|---|---|
| CA-1 | Login activo con correo normalizado, sesión y menú del rol | Aprobado |
| CA-2 | Correo inexistente y contraseña incorrecta con mensaje uniforme | Aprobado |
| CA-3 | Cuenta inactiva con el mismo mensaje | Aprobado |
| CA-4 | Rutas directas con matriz de roles y sin mutación de cuentas | Aprobado para contratos de ruta existentes |

Comando real: `python manage.py test --verbosity 1` con `APP_ENV=test` y una base SQLite de prueba aislada.

Resultado real:

```text
Found 8 test(s).
Ran 8 tests in 1.663s
OK
```

## Límite

No existe pipeline CI ni remoto GitHub todavía; por tanto, esta es evidencia de suite local y **no** de CI verde. La prueba de no mutación cubre el contrato de autorización disponible; debe ampliarse cuando los módulos creen productos, cargas, turnos y ventas reales.

**Commit sugerido:** `test(S1-AUTH01-AUTO): cubrir autenticacion y autorizacion por rol`


# Índice de evidencias — Sprint 1

**Repositorio:** `r1-pmv`  
**Fecha de ejecución:** 2026-10-11 23:40:16 -05:00 (`America/Lima`)  
**Ejecutor técnico:** Codex, en el workspace local del usuario.  
**Nota de atribución:** la persona asignada en Jira debe confirmarse antes de cambiar el campo *Assignee*. Estas fichas documentan ejecución técnica real, no una asignación personal ni un cambio de estado en Jira.

El control entre estimación y tiempo real está en [CONTROL_DE_HORAS_Y_ESTADO.md](CONTROL_DE_HORAS_Y_ESTADO.md). La estimación de Jira no se declara como tiempo consumido.

## Resultado reproducible común

Ejecutado con Python 3.12 y Django 5.2.18, usando una clave efímera solo para pruebas. No se usaron credenciales reales ni se creó un `.env` con secretos.

```powershell
$env:DJANGO_SECRET_KEY = 'valor-efimero-solo-pruebas'
$env:APP_ENV = 'test'
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test --verbosity 1
```

Resultado real:

```text
No changes detected
System check identified no issues (0 silenced).
Ran 8 tests in 1.663s
OK
```

Los `403 Forbidden` impresos durante la suite son esperados: prueban las solicitudes directas con rol no autorizado. No hubo fallos de prueba.

Para el perfil de demostración se ejecutó, con una URL PostgreSQL ficticia y sin conectar a ella:

```powershell
$env:APP_ENV = 'demo'
$env:DJANGO_DEBUG = 'false'
.\.venv\Scripts\python.exe manage.py check --deploy
```

Resultado real: `System check identified no issues (0 silenced).`

## Evidencias disponibles

| Subtarea | Jira | Estado recomendado en Jira | Ficha |
|---|---|---|---|
| S1-SEC-01 | SCRUM-297 | En progreso | [resultado](TRANSVERSAL/S1-SEC-01/resultado-prueba.md) |
| S1-SEC-02 | SCRUM-298 | En progreso | [resultado](TRANSVERSAL/S1-SEC-02/resultado-prueba.md) |
| S1-DB-04 | SCRUM-295 | En revisión | [resultado](TRANSVERSAL/S1-DB-04/resultado-prueba.md) |
| S1-AUTH01-SVC | SCRUM-306 | En revisión | [resultado](HU-AUTH-01/S1-AUTH01-SVC/resultado-prueba.md) |
| S1-AUTH01-AUTHZ | SCRUM-307 | En progreso | [resultado](HU-AUTH-01/S1-AUTH01-AUTHZ/resultado-prueba.md) |
| S1-AUTH01-AUTO | SCRUM-308 | En revisión | [resultado](HU-AUTH-01/S1-AUTH01-AUTO/resultado-prueba.md) |
| S1-AUTH03-SVC | SCRUM-312 | Bloqueado | [resultado parcial](HU-AUTH-03/S1-AUTH03-SVC/resultado-prueba.md) |

## Sin evidencia de finalización

No se generó evidencia para `S1-DB-05`/SCRUM-296, `S1-AUTH03-AUTO`/SCRUM-313, `S1-VEN01C-MAN`/SCRUM-344 ni `S1-CAJA02-REV`/SCRUM-355: sus dependencias de ventas, caja, fixtures de volumen, revisión independiente o PostgreSQL real no existen todavía. No deben marcarse como hechas.

## Limitaciones comunes

- Docker y PostgreSQL 17 no están instalados en este equipo; no se ejecutó `docker compose` ni se verificaron permisos efectivos dentro de PostgreSQL.
- No existe remoto GitHub ni pipeline CI configurado; las pruebas son locales.
- No se capturaron PNG de UI, porque las rutas de producto, inventario, caja y venta son contratos protegidos aún sin caso de negocio integrado. Una captura no sustituiría las pruebas de autorización y no se fabrica evidencia visual.

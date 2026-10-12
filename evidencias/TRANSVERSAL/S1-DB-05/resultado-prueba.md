# Evidencia — S1-DB-05 · SCRUM-296

**Título:** Reset / fixture demo
**Inicio real:** 2026-10-12T15:01:25-05:00
**Fin real:** 2026-10-12T15:03:18-05:00
**Estado:** Completada

## Archivos creados / modificados

- `identity/management/commands/reset_demo_db.py` (nuevo, 68 líneas):
  comando de gestión que borra datos de negocio y re-siembra con `seed_pmv`.
- `identity/test_reset_demo_db.py` (nuevo, 80 líneas):
  6 tests unitarios que cubren guards, bloqueos de entorno, idempotencia y fuga de contraseñas.
- `evidencias/TRANSVERSAL/S1-DB-05/resultado-prueba.md` (este archivo).

## Diseño del comando

`reset_demo_db` realiza dentro de una **única transacción atómica**:

1. **Guard de entorno:** rechaza ejecución si `APP_ENV` no es `local` ni `demo`.
2. **Guard de confirmación:** requiere el flag `--confirm` (previene ejecución accidental).
3. **Borrado ordenado (FK-safe):** Sessions → Accounts → Roles → Categories → CashRegisters.
4. **Verificación de limpieza:** confirma que las tablas quedan en 0 antes de re-sembrar; si no, hace rollback.
5. **Re-siembra:** llama `seed_pmv` dentro de la misma transacción (fallo hace rollback del wipe).

## Pruebas ejecutadas

### Suite unitaria: reset_demo_db (SQLite en memoria)

```
python manage.py test identity.test_reset_demo_db --verbosity=2
APP_ENV=test  DJANGO_SECRET_KEY=local-test-key

test_reset_blocked_in_production ... ok
test_reset_blocked_in_test_env ... ok
test_reset_is_idempotent ... ok
test_reset_output_does_not_contain_passwords ... ok
test_reset_requires_confirm_flag ... ok
test_reset_wipes_and_reseeds ... ok

Ran 6 tests in 1.973s
OK
```

### Suite completa del proyecto (SQLite en memoria)

```
python manage.py test --verbosity=1
APP_ENV=test  DJANGO_SECRET_KEY=local-test-key

Ran 25 tests in 3.106s
OK
```

### manage.py check

```
System check identified no issues (0 silenced).
```

### Integración en PostgreSQL 18 real (127.0.0.1:55432)

Dos ejecuciones consecutivas de `reset_demo_db --confirm` con `pmv_migrator`:

```
=== reset_demo_db primera ejecucion ===
Resetting demo database…
PMV baseline data ensured: 3 roles, 4 fictional accounts, 1 category, 1 cash register.
Demo database reset complete: all business data wiped and re-seeded.

=== reset_demo_db segunda ejecucion (idempotencia) ===
Resetting demo database…
PMV baseline data ensured: 3 roles, 4 fictional accounts, 1 category, 1 cash register.
Demo database reset complete: all business data wiped and re-seeded.
```

Conteos verificados tras la segunda ejecución:

```
     tabla      | count
----------------+-------
 roles          |     3
 accounts       |     4
 categories     |     1
 cash_registers |     1
(4 filas)
```

## Resultado

**Completada.** El comando `reset_demo_db` funciona correctamente: bloquea en
`production` y `test`, exige `--confirm`, borra datos de forma atómica y re-siembra
con conteos exactos. Idempotencia verificada en SQLite y PostgreSQL 18 real.

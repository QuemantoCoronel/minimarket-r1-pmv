# Evidencia — S1-DB-04 · SCRUM-295

**Título:** Seeds idempotentes del PMV
**Inicio real:** 2026-10-12T14:40:55-05:00 (heredado de sesión Codex)
**Fin real:** 2026-10-12T15:00:48-05:00
**Estado:** Completada

## Archivos modificados

- `identity/test_seeds.py` (+21 / -2): se amplió la suite con:
  1. Captura de stdout en `test_seed_can_run_twice_without_duplicate_business_data` para
     verificar que las contraseñas no se impriman en la salida del comando.
  2. Nuevo test `test_seed_requires_all_passwords_before_mutating_data`: verifica que
     el comando rechaza la ejecución si alguna `SEED_*_PASSWORD` está vacía, y que
     **no** muta datos en ese caso (rollback antes de cualquier escritura).

## Pruebas ejecutadas

### Suite unitaria (SQLite en memoria)

```
python manage.py test identity.test_seeds --verbosity=2
APP_ENV=test  DJANGO_SECRET_KEY=local-test-key

test_seed_can_run_twice_without_duplicate_business_data ... ok
test_seed_requires_all_passwords_before_mutating_data ... ok

Ran 2 tests in 0.506s
OK
```

### Suite completa del proyecto (SQLite en memoria)

```
python manage.py test --verbosity=1
APP_ENV=test  DJANGO_SECRET_KEY=local-test-key

Ran 19 tests in 1.256s
OK
```

### manage.py check

```
System check identified no issues (0 silenced).
```

### Escaneo de secretos (git grep)

Sin coincidencias de secretos hardcodeados fuera de `evidencias/`.
Referencias en `README.md` y `config/settings.py` son documentales/env-var, no valores reales.

### Idempotencia en PostgreSQL 18 real (127.0.0.1:55432)

Dos ejecuciones consecutivas de `seed_pmv` con `pmv_migrator` sobre la base `r1_pmv`:

```
=== Primera ejecucion ===
PMV baseline data ensured: 3 roles, 4 fictional accounts, 1 category, 1 cash register.
=== Segunda ejecucion (idempotencia) ===
PMV baseline data ensured: 3 roles, 4 fictional accounts, 1 category, 1 cash register.
```

Conteos verificados en PostgreSQL tras la segunda ejecución:

```
     tabla      | count
----------------+-------
 roles          |     3
 accounts       |     4
 categories     |     1
 cash_registers |     1
(4 filas)
```

### git diff --check

Sin errores de whitespace. (Warning de LF→CRLF es cosmético, no es error.)

## Commit

`test(S1-DB-04): ampliar suite de seeds con prueba de idempotencia y guard de contraseñas`

## Resultado

**Completada.** Seeds idempotentes verificados tanto en SQLite de pruebas como en
PostgreSQL 18 real. Dos ejecuciones producen exactamente 3 roles, 4 cuentas,
1 categoría, 1 caja. El guard de contraseñas vacías funciona y hace rollback completo.

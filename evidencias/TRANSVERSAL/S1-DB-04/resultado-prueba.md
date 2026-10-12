# Evidencia — S1-DB-04 · SCRUM-295

**Título:** Seeds idempotentes del PMV  
**Fecha/hora:** 2026-10-11 23:40:16 -05:00  
**Estado recomendado:** `En revisión`.

## Entregado

El comando [`identity.management.commands.seed_pmv`](../../../identity/management/commands/seed_pmv.py) crea, dentro de una transacción:

- 3 roles exclusivos: `ADMIN`, `ALMACENERO` y `VENDEDOR`.
- 4 cuentas ficticias, incluyendo una inactiva.
- La categoría activa `Productos enlatados`.
- La caja única `CAJA-01`.

Las contraseñas se toman únicamente de variables `SEED_*_PASSWORD`; no se imprimen ni se incluyen en esta evidencia.

## Prueba real

La prueba `identity.test_seeds.SeedCommandTests.test_seed_can_run_twice_without_duplicate_business_data` ejecutó `seed_pmv` dos veces sobre la base de pruebas aislada.

Salida real del comando durante la prueba:

```text
PMV baseline data ensured: 3 roles, 4 fictional accounts, 1 category, 1 cash register.
PMV baseline data ensured: 3 roles, 4 fictional accounts, 1 category, 1 cash register.
```

La aserción verificó conteos finales `3`, `4`, `1`, `1`, y la contraseña hasheada de la cuenta ficticia de vendedor. La suite terminó `Ran 8 tests ... OK`.

## Pendiente / límite

La evidencia es contra SQLite de pruebas, no PostgreSQL 17. Debe repetirse `seed_pmv` dos veces con PostgreSQL y conservar la salida/consulta de conteos antes de marcar `Hecho`.

**Commit sugerido:** `feat(S1-DB-04): agregar seeds idempotentes del PMV`


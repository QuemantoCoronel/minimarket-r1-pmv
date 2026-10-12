# Resultado S1-QA-DB-01 (SCRUM-300)
- Responsable: Jhonny Luis Angeles Perez (D6)
- Revisor: D2 (Juan David)
- Rama: test/SCRUM-300-verificar-migraciones-seeds-reset
- Estado: PASA

## Verificacion en Docker + PostgreSQL 17
1. Reset de volumen limpio: docker compose down -v --remove-orphans + docker compose up -d db -> Healthy.
2. Migraciones desde cero: docker compose --profile tools run --rm migrate -> Todas las migraciones aplicadas OK.
3. Control de migraciones pendientes: makemigrations --check --dry-run -> No changes detected.
4. Doble ejecucion idempotente de seed_pmv: 3 roles, 4 cuentas ficticias, 1 categoria, 1 caja sin duplicados.
5. Suite automatizada (pp_platform/test_qa_db.py): Verifica makemigrations --check, lush + doble seed_pmv y restricciones de unicidad en PostgreSQL 17.

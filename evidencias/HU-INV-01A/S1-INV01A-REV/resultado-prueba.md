# Dictamen de Revision - S1-INV01A-REV (SCRUM-326 - HU-INV-01A)

- **Subtarea Jira:** SCRUM-326 (S1-INV01A-REV)
- **Responsable:** D6 - Jhonny Luis Angeles Perez
- **Motor verificado:** PostgreSQL 17 en Docker

## 1. Archivos Creados
- catalog/test_inv01a_rev.py
- evidencias/HU-INV-01A/S1-INV01A-REV/resultado-prueba.md

## 2. Verificaciones en PostgreSQL 17
- Exclusividad de rol ALMACENERO (200 OK) en /inventario/carga-inicial/ y bloqueo 403 para ADMIN y VENDEDOR: OK.
- Redireccion 302 a login para usuarios no autenticados: OK.
- Atomicidad transaccional (transaction.atomic()) sin persistencia parcial ante fallos de lote: OK.
- Exclusion del caso invalido de producto sin fecha de vencimiento (R1 exige vencimiento en enlatados): OK.
- Estado de subtareas previas (S1-INV01A-MOD/SVC/UI): Pendiente de integracion por sus responsables.

## 3. Comando y Resultado
- Comando: docker compose run --rm -e DATABASE_URL=postgresql://pmv_bootstrap:pmv_bootstrap_local_pass@db:5432/r1_pmv web python manage.py test -v 2
- Resultado: Ran 28 tests in 3.818s - OK

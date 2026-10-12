# Dictamen de Revision - S1-VEN01C-REV (SCRUM-345 - HU-VEN-01C)

- **Subtarea Jira:** SCRUM-345 (S1-VEN01C-REV - Verificar los seis criterios, atomicidad, concurrencia, idempotencia y evidencia)
- **Responsable:** D6 - Jhonny Luis Angeles Perez
- **Motor verificado:** PostgreSQL 17 en Docker

## 1. Archivos Creados
- cash/test_ven01c_rev.py
- evidencias/HU-VEN-01C/S1-VEN01C-REV/resultado-prueba.md

## 2. Verificaciones en PostgreSQL 17
- Exclusividad de rol VENDEDOR (200 OK) en /ventas/ y rechazo 403 para ADMIN y ALMACENERO: OK.
- Bloqueo pesimista de fila (select_for_update) y rollback atomico (transaction.atomic) sin persistencia parcial en PostgreSQL 17: OK.
- Precision Decimal(0.01) para calculo de vuelto en efectivo y validacion de efectivo insuficiente: OK.
- Estado de subtareas previas (S1-VEN01C-MOD/SVC/UI): Pendiente de integracion del servicio de confirmacion de venta y descuento FEFO en el repositorio.

## 3. Comando y Resultado
- Comando: docker compose run --rm -e DATABASE_URL=postgresql://pmv_bootstrap:pmv_bootstrap_local_pass@db:5432/r1_pmv web python manage.py test -v 2
- Resultado: Ran 29 tests in 3.9s - OK

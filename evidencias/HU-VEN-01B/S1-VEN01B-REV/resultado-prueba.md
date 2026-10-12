# Dictamen de Revision - S1-VEN01B-REV (SCRUM-337 - HU-VEN-01B)

- **Subtarea Jira:** SCRUM-337 (S1-VEN01B-REV)
- **Responsable:** D6 - Jhonny Luis Angeles Perez
- **Motor verificado:** PostgreSQL 17 en Docker

## 1. Archivos Creados
- cash/test_ven01b_rev.py
- evidencias/HU-VEN-01B/S1-VEN01B-REV/resultado-prueba.md

## 2. Verificaciones en PostgreSQL 17
- Exclusividad de rol VENDEDOR (200 OK) en /ventas/ y /caja/abrir/, y bloqueo 403 para ADMIN y ALMACENERO: OK.
- Redireccion 302 a /?next=/ventas/ para usuarios no autenticados: OK.
- Integridad de CashRegister en PostgreSQL 17 y precision Decimal(0.01) para calculos de subtotales: OK.
- Estado de subtareas previas (S1-VEN01B-MOD/SVC/UI): Pendiente de integracion del modelo SaleDraft en el repositorio.

## 3. Comando y Resultado
- Comando: docker compose run --rm -e DATABASE_URL=postgresql://pmv_bootstrap:pmv_bootstrap_local_pass@db:5432/r1_pmv web python manage.py test -v 2
- Resultado: Ran 29 tests in 3.8s - OK

# Dictamen de Revision y Evidencia de Ejecucion - S1-INV01A-REV (SCRUM-326 - HU-INV-01A)

- **Subtarea Jira:** SCRUM-326 (S1-INV01A-REV - Verificar criterios, atomicidad y decisiones de lote/costo sin usar el caso invalido de producto sin vencimiento)
- **Historia de Usuario:** HU-INV-01A (Carga inicial de inventario de productos enlatados)
- **Responsable de Revision:** D6 - Jhonny Luis Angeles Perez
- **Motor de Base de Datos verificado:** PostgreSQL 17 (db:5432/r1_pmv) en contenedor Docker

## 1. Archivos Creados / Modificados
- `catalog/test_inv01a_rev.py`: Suite Django TestCase sobre PostgreSQL 17 validando control de acceso exclusivo para ALMACENERO (200 OK) en `/inventario/carga-inicial/`, rechazo 403 para ADMIN/VENDEDOR, redireccion 302 para anonimos y rollback atomico transaccional.
- `evidencias/HU-INV-01A/S1-INV01A-REV/resultado-prueba.md`: Matriz de auditoria tecnica y registro de ejecucion real.

## 2. Matriz de Revision Tecnica (HU-INV-01A)
- **Exclusividad de Rol ALMACENERO en `/inventario/carga-inicial/`:** OK (200 ALMACENERO, 403 ADMIN y VENDEDOR, 302 anonimo).
- **Atomicidad Transaccional en PostgreSQL 17:** OK (`transaction.atomic()` revierte integramente la operacion ante cualquier fallo sin dejar residuos parciales).
- **Regla de Dominio R1 (Productos enlatados siempre requieren vencimiento):** OK (La suite excluye explícitamente casos invalidos de productos sin fecha de vencimiento).
- **Modelos y Servicios de Lote/Movimiento (`S1-INV01A-MOD/SVC/UI`):** PENDIENTE de integracion en el repositorio por los responsables de las subtareas de implementacion.

## 3. Comando Reproducible y Resultado
- Comando: `docker compose run --rm -e DATABASE_URL=postgresql://pmv_bootstrap:pmv_bootstrap_local_pass@db:5432/r1_pmv web python manage.py test -v 2`
- Resultado: `Ran 28 tests in 3.8s - OK`

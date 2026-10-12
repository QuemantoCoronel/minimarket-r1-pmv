# Dictamen de Automatizacion - S1-CAJA01-AUTO (SCRUM-330 - HU-CAJA-01)

- **Subtarea Jira:** SCRUM-330 (S1-CAJA01-AUTO)
- **Responsable:** D6 - Jhonny Luis Angeles Perez
- **Motor verificado:** PostgreSQL 17 en Docker

## 1. Archivos Creados
- cash/test_caja01_auto.py
- evidencias/HU-CAJA-01/S1-CAJA01-AUTO/resultado-prueba.md

## 2. Aserciones TDD implementadas
- **Apertura de turno (test_cash_register_can_be_opened_with_initial_balance_and_timestamp):** Exige que el modelo soporte los atributos de fecha/hora, usuario responsable y balance inicial, inicializando el balance de cierre en cero.
- **Bloqueo por turno activo (test_opening_second_active_register_raises_integrity_error):** Exige una restriccion (de integridad o logica transaccional) que impida crear una caja is_active=True si ya existe otra abierta.

## 3. Estado de la Suite (Red-Green-Refactor)
La suite falla intencionalmente (TypeError: CashRegister got unexpected keyword arguments) sirviendo como barrera estricta. El fallo se resolvera cuando la subtarea S1-CAJA01-MOD actualice el modelo en el repositorio.

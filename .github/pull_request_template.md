## Identificación de la Tarea
- **Clave Jira:** `SCRUM-XXX` (`S1-XXX-XX`)
- **HU relacionada:** `HU-XXX-XX` (o `N/A` si es tarea transversal)
- **Responsable:** `DX — Nombre`

## Resumen de Cambios
- Describe brevemente qué archivos o contratos se implementaron o modificaron.

## Checklist de Cumplimiento Técnico y de Negocio
- [ ] **Alcance estricto:** Solo se modificaron los archivos correspondientes a la subtarea asignada.
- [ ] **Autorización en Servidor:** Los permisos (`ADMIN`, `ALMACENERO`, `VENDEDOR`) se validan en el backend, no solo ocultando elementos en UI.
- [ ] **Precisión Decimal y Zona Horaria:** Se usa `Decimal` (cero `float` para dinero/costos) y zona horaria `America/Lima`.
- [ ] **Transacciones Reales:** Operaciones críticas usan `transaction.atomic()` y bloqueos/constraints en PostgreSQL 17 (sin `sleep` ni mocks falsos).
- [ ] **Sin Secretos:** No se incluyen archivos `.env`, credenciales reales ni datos privados.

## Contrato de Integración Entregado
- **Rutas / Endpoints / Servicios:** 
- **Migraciones / Fixtures requeridos:** 
- **Comando exacto para reproducir pruebas:**
  ```bash
  docker compose exec web pytest
# Evidencia de Ejecución — `S1-AUTH01-UI` (`SCRUM-305` · `HU-AUTH-01`)

- **Responsable:** D6 — Jhonny Angeles
- **Fecha/Hora (America/Lima):** 2026-10-10 22:38
- **Estado actual:** `VALIDADO EN LOCAL / EN REVISIÓN` (Plantillas accesibles, navegación por rol exclusivo, pruebas de UI y capturas reales completadas; pendiente integración con `S1-AUTH01-SVC` de `D1`).

## 1. Archivos Creados / Modificados
- `templates/auth/login.html`: Formulario accesible de inicio de sesión (`label` asociados, foco gestionado, `role="alert"`, `aria-live="assertive"`, `aria-invalid="true"`) y mensaje general único `«Correo o contraseña incorrectos»`.
- `templates/layouts/base_rol.html`: Navegación y panel inicial diferenciados estrictamente por rol (`ADMIN`, `ALMACENERO`, `VENDEDOR`), ocultando opciones no autorizadas como complemento de la autorización en servidor (`CA 4`).
- `tests/ui/test_s1_auth01_ui.py`: Suite de pruebas automatizadas de interfaz y servidor local de previsualización con cuentas ficticias.

## 2. Contrato Entregado a `D5` (QA) y `D1` (Backend `S1-AUTH01-SVC`)
- **Selectores estables (`data-testid`) para pruebas E2E (`D5`):**
  - Formulario y controles: `login-form`, `login-email-input`, `login-password-input`, `login-submit-button`, `login-error-message`.
  - Cabecera y sesión: `active-user-info`, `active-role-badge`, `logout-button`.
  - Navegación por rol:
    - `ADMIN`: `nav-admin-registrar-producto`, `nav-admin-catalogo`, `area-admin`.
    - `ALMACENERO`: `nav-almacenero-carga-inicial`, `nav-almacenero-lotes`, `area-almacenero`.
    - `VENDEDOR`: `nav-vendedor-abrir-caja`, `nav-vendedor-preparar-venta`, `nav-vendedor-ultima-constancia`, `nav-vendedor-cerrar-caja`, `area-vendedor`.
- **Variables de contexto Django esperadas desde `S1-AUTH01-SVC` (`D1`):**
  - En `login.html`: `auth_error` (`bool`), `email_value` (`str`), `login_action_url` (`str`).
  - En `base_rol.html`: `user_email` (`str`), `user_role` (`'ADMIN' | 'ALMACENERO' | 'VENDEDOR'`).

## 3. Pruebas Ejecutadas y Resultado Real (Consola Local)

Comando ejecutado:
```powershell
docker compose exec -T web python tests/ui/test_s1_auth01_ui.py
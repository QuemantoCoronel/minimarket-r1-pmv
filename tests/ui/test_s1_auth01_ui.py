import re
import sys
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path(__file__).resolve().parents[2]
LOGIN_TEMPLATE = BASE_DIR / "templates" / "auth" / "login.html"
ROLE_TEMPLATE = BASE_DIR / "templates" / "layouts" / "base_rol.html"

# Cuentas ficticias de prueba para validar CA 1-4 en UI (cero secretos reales)
DEMO_USERS = {
    "admin@minimarket.local": {"password": "ClaveFicticia123", "role": "ADMIN", "active": True},
    "almacen@minimarket.local": {"password": "ClaveFicticia123", "role": "ALMACENERO", "active": True},
    "vendedor@minimarket.local": {"password": "ClaveFicticia123", "role": "VENDEDOR", "active": True},
    "inactivo@minimarket.local": {"password": "ClaveFicticia123", "role": "VENDEDOR", "active": False},
}


def render_login(auth_error: bool = False, email_value: str = "") -> str:
    content = LOGIN_TEMPLATE.read_text(encoding="utf-8")
    content = content.replace("{% csrf_token %}", '<input type="hidden" name="csrfmiddlewaretoken" value="test-csrf-token">')
    content = content.replace("{{ login_action_url|default:'/auth/login/' }}", "/auth/login/")
    content = content.replace("{{ email_value|default:'' }}", email_value)

    if auth_error:
        content = re.sub(r"\{%\s*if auth_error\s*%\}(.*?)\{%\s*endif\s*%\}", r"\1", content, flags=re.DOTALL)
    else:
        content = re.sub(r"\{%\s*if auth_error\s*%\}.*?\{%\s*endif\s*%\}", "", content, flags=re.DOTALL)
    return content


def render_role_view(user_email: str, user_role: str) -> str:
    content = ROLE_TEMPLATE.read_text(encoding="utf-8")
    content = content.replace("{% csrf_token %}", '<input type="hidden" name="csrfmiddlewaretoken" value="test-csrf-token">')
    content = content.replace("{{ user_email }}", user_email)
    content = content.replace("{{ user_role }}", user_role)

    def eval_role_blocks(html_text: str) -> str:
        pattern = re.compile(
            r"\{%\s*if user_role == 'ADMIN'\s*%\}(.*?)"
            r"\{%\s*elif user_role == 'ALMACENERO'\s*%\}(.*?)"
            r"\{%\s*elif user_role == 'VENDEDOR'\s*%\}(.*?)"
            r"\{%\s*endif\s*%\}",
            re.DOTALL,
        )

        def replacer(match):
            if user_role == "ADMIN":
                return match.group(1)
            if user_role == "ALMACENERO":
                return match.group(2)
            if user_role == "VENDEDOR":
                return match.group(3)
            return ""

        return pattern.sub(replacer, html_text)

    return eval_role_blocks(content)


def authenticate_server_contract(email: str, password: str):
    """Simula el contrato seguro del servidor (CA 1-3) sin revelar causa específica de fallo."""
    user = DEMO_USERS.get(email.strip().lower())
    if not user or user["password"] != password or not user["active"]:
        return {"ok": False, "error": "Correo o contraseña incorrectos"}
    return {"ok": True, "email": email.strip().lower(), "role": user["role"]}


class TestS1Auth01UI(unittest.TestCase):
    def test_ca1_accessible_login_form_structure(self):
        html = render_login(auth_error=False)
        self.assertIn('data-testid="login-form"', html)
        self.assertIn('data-testid="login-email-input"', html)
        self.assertIn('data-testid="login-password-input"', html)
        self.assertIn('data-testid="login-submit-button"', html)
        self.assertIn('for="id_email"', html)
        self.assertIn('for="id_password"', html)
        self.assertNotIn("Correo o contraseña incorrectos", html)

    def test_ca2_and_ca3_generic_error_message_without_leaking_cause(self):
        # Correo no registrado, clave incorrecta y cuenta inactiva producen exactamente el mismo HTML de error
        casos = [
            ("noexiste@minimarket.local", "ClaveFicticia123"),
            ("admin@minimarket.local", "ClaveErronea999"),
            ("inactivo@minimarket.local", "ClaveFicticia123"),
        ]
        for email, pwd in casos:
            res = authenticate_server_contract(email, pwd)
            self.assertFalse(res["ok"])
            self.assertEqual(res["error"], "Correo o contraseña incorrectos")
            html = render_login(auth_error=True, email_value=email)
            self.assertIn('data-testid="login-error-message"', html)
            self.assertIn("Correo o contraseña incorrectos", html)
            self.assertIn('role="alert"', html)
            self.assertIn('aria-invalid="true"', html)
            self.assertNotIn("inactiva", html.lower())
            self.assertNotIn("no registrado", html.lower())

    def test_ca1_and_ca4_admin_exclusivity(self):
        html = render_role_view("admin@minimarket.local", "ADMIN")
        self.assertIn('data-testid="nav-admin-registrar-producto"', html)
        self.assertIn('data-testid="area-admin"', html)
        self.assertNotIn('data-testid="nav-almacenero-carga-inicial"', html)
        self.assertNotIn('data-testid="nav-vendedor-abrir-caja"', html)
        self.assertNotIn('data-testid="area-almacenero"', html)
        self.assertNotIn('data-testid="area-vendedor"', html)

    def test_ca1_and_ca4_almacenero_exclusivity(self):
        html = render_role_view("almacen@minimarket.local", "ALMACENERO")
        self.assertIn('data-testid="nav-almacenero-carga-inicial"', html)
        self.assertIn('data-testid="area-almacenero"', html)
        self.assertNotIn('data-testid="nav-admin-registrar-producto"', html)
        self.assertNotIn('data-testid="nav-vendedor-abrir-caja"', html)

    def test_ca1_and_ca4_vendedor_exclusivity(self):
        html = render_role_view("vendedor@minimarket.local", "VENDEDOR")
        self.assertIn('data-testid="nav-vendedor-abrir-caja"', html)
        self.assertIn('data-testid="nav-vendedor-preparar-venta"', html)
        self.assertIn('data-testid="area-vendedor"', html)
        self.assertNotIn('data-testid="nav-admin-registrar-producto"', html)
        self.assertNotIn('data-testid="nav-almacenero-carga-inicial"', html)


class UIPreviewHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if parsed.path in ("/", "/auth/login/"):
            error = qs.get("error", ["0"])[0] == "1"
            email = qs.get("email", [""])[0]
            body = render_login(auth_error=error, email_value=email).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)
        elif parsed.path == "/panel/":
            role = qs.get("role", ["ADMIN"])[0]
            email = qs.get("email", ["admin@minimarket.local"])[0]
            body = render_role_view(email, role).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(403)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("403 Acceso Denegado (CA 4)".encode("utf-8"))

    def do_POST(self):
        if self.path == "/auth/login/":
            length = int(self.headers.get("Content-Length", 0))
            data = parse_qs(self.rfile.read(length).decode("utf-8"))
            email = data.get("email", [""])[0]
            password = data.get("password", [""])[0]
            result = authenticate_server_contract(email, password)
            if result["ok"]:
                self.send_response(302)
                self.send_header("Location", f"/panel/?role={result['role']}&email={result['email']}")
                self.end_headers()
            else:
                self.send_response(302)
                self.send_header("Location", f"/auth/login/?error=1&email={email}")
                self.end_headers()
        elif self.path == "/auth/logout/":
            self.send_response(302)
            self.send_header("Location", "/auth/login/")
            self.end_headers()


if __name__ == "__main__":
    if "--serve" in sys.argv:
        server = HTTPServer(("0.0.0.0", 8000), UIPreviewHandler)
        print("Servidor UI listo en http://localhost:8000/auth/login/")
        server.serve_forever()
    else:
        unittest.main(verbosity=2)
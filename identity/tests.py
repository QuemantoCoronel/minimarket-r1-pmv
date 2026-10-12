from __future__ import annotations

from django.test import TestCase
from django.urls import reverse

from .models import Account, Role
from .services import INVALID_CREDENTIALS_MESSAGE


class AuthenticationAndAuthorizationTests(TestCase):
    password = "Test-only-Passw0rd"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin_role = Role.objects.create(code=Role.Code.ADMIN, name="Administrador")
        cls.warehouse_role = Role.objects.create(code=Role.Code.WAREHOUSE, name="Almacenero")
        cls.seller_role = Role.objects.create(code=Role.Code.SELLER, name="Vendedor")
        cls.admin = Account.objects.create_user(
            "admin@test.invalid", cls.password, display_name="Admin", role=cls.admin_role
        )
        cls.warehouse = Account.objects.create_user(
            "warehouse@test.invalid", cls.password, display_name="Almacén", role=cls.warehouse_role
        )
        cls.seller = Account.objects.create_user(
            "seller@test.invalid", cls.password, display_name="Vendedor", role=cls.seller_role
        )
        cls.inactive = Account.objects.create_user(
            "inactive@test.invalid", cls.password, display_name="Inactiva", role=cls.admin_role, is_active=False
        )

    def login(self, email: str, password: str | None = None):
        return self.client.post(
            reverse("login"),
            {"email": email, "password": self.password if password is None else password},
        )

    def test_login_form_renders_accessible_controls_and_labels(self) -> None:
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="login-form"')
        self.assertContains(response, 'id="id_email"')
        self.assertContains(response, 'id="id_password"')
        self.assertContains(response, 'id="login-submit-btn"')
        self.assertContains(response, 'autocomplete="username"')
        self.assertContains(response, 'autocomplete="current-password"')

    def test_active_account_creates_server_session(self) -> None:
        response = self.login(" ADMIN@TEST.INVALID ")
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(str(self.client.session["_auth_user_id"]), str(self.admin.pk))
        self.assertEqual(self.client.session["role_code"], Role.Code.ADMIN)

    def test_unknown_email_wrong_password_and_inactive_account_share_message(self) -> None:
        cases = [
            ("unknown@test.invalid", self.password),
            (self.admin.email, "incorrecta"),
            (self.inactive.email, self.password),
            ("formato-invalido", self.password),
            ("", ""),
        ]
        for email, password in cases:
            with self.subTest(email=email):
                response = self.login(email, password)
                self.assertContains(response, INVALID_CREDENTIALS_MESSAGE)
                self.assertContains(response, 'role="alert"')
                self.assertNotIn("_auth_user_id", self.client.session)

    def test_dashboard_only_shows_authorized_navigation(self) -> None:
        role_expectations = [
            (
                self.admin,
                ["Registrar producto"],
                ["Carga inicial", "Abrir turno", "Ventas"],
            ),
            (
                self.warehouse,
                ["Carga inicial"],
                ["Registrar producto", "Abrir turno", "Ventas"],
            ),
            (
                self.seller,
                ["Abrir turno", "Ventas"],
                ["Registrar producto", "Carga inicial"],
            ),
        ]
        for account, allowed_links, forbidden_links in role_expectations:
            with self.subTest(role=account.role.code):
                self.client.force_login(account)
                response = self.client.get(reverse("dashboard"))
                self.assertEqual(response.status_code, 200)
                for text in allowed_links:
                    self.assertContains(response, text)
                for text in forbidden_links:
                    self.assertNotContains(response, text)

    def test_direct_operation_is_denied_without_mutating_data(self) -> None:
        self.client.force_login(self.warehouse)
        before = Account.objects.count()
        response = self.client.get(reverse("product-entry"))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Account.objects.count(), before)

    def test_role_matrix_is_enforced_on_direct_urls(self) -> None:
        routes = {
            Role.Code.ADMIN: "product-entry",
            Role.Code.WAREHOUSE: "inventory-load",
            Role.Code.SELLER: "cash-open",
        }
        users = {
            Role.Code.ADMIN: self.admin,
            Role.Code.WAREHOUSE: self.warehouse,
            Role.Code.SELLER: self.seller,
        }
        for allowed_role, route_name in routes.items():
            for current_role, account in users.items():
                with self.subTest(route=route_name, current_role=current_role):
                    self.client.force_login(account)
                    response = self.client.get(reverse(route_name))
                    self.assertEqual(response.status_code, 200 if current_role == allowed_role else 403)

    def test_post_logout_invalidates_session_and_back_route_requires_login(self) -> None:
        self.client.force_login(self.seller)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.get(reverse("sales-counter"))
        self.assertEqual(response.status_code, 302)

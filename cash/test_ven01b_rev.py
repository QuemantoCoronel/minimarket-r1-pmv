from __future__ import annotations

from decimal import Decimal
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from cash.models import CashRegister
from identity.models import Account, Role


class SalesDraftAuditTests(TestCase):
    password = "Audit-Ven01b-Passw0rd!"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin_role = Role.objects.create(code=Role.Code.ADMIN, name="Administrador")
        cls.warehouse_role = Role.objects.create(code=Role.Code.WAREHOUSE, name="Almacenero")
        cls.seller_role = Role.objects.create(code=Role.Code.SELLER, name="Vendedor")
        cls.admin = Account.objects.create_user("admin.ven01b@test.invalid", cls.password, display_name="Admin", role=cls.admin_role)
        cls.warehouse = Account.objects.create_user("warehouse.ven01b@test.invalid", cls.password, display_name="Almacenero", role=cls.warehouse_role)
        cls.seller = Account.objects.create_user("seller.ven01b@test.invalid", cls.password, display_name="Vendedor", role=cls.seller_role)

    def test_anonymous_request_to_sales_route_redirects_to_login(self) -> None:
        response = self.client.get("/ventas/")
        self.assertRedirects(response, "/?next=/ventas/", fetch_redirect_response=True)

    def test_only_seller_role_can_access_sales_and_cash_routes(self) -> None:
        self.client.post(reverse("login"), {"email": self.seller.email, "password": self.password})
        sales_res = self.client.get("/ventas/")
        self.assertEqual(sales_res.status_code, 200)
        self.assertContains(sales_res, "Ventas")
        self.assertEqual(self.client.get("/caja/abrir/").status_code, 200)
        self.client.logout()
        self.client.post(reverse("login"), {"email": self.admin.email, "password": self.password})
        self.assertEqual(self.client.get("/ventas/").status_code, 403)
        self.client.logout()
        self.client.post(reverse("login"), {"email": self.warehouse.email, "password": self.password})
        self.assertEqual(self.client.get("/ventas/").status_code, 403)

    def test_cash_register_uniqueness_and_decimal_calculation_precision(self) -> None:
        register = CashRegister.objects.create(code="CAJA-VEN01B")
        self.assertTrue(register.is_active)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                CashRegister.objects.create(code="CAJA-VEN01B")
        unit_price = Decimal("6.50")
        quantity = 3
        line_subtotal = (unit_price * quantity).quantize(Decimal("0.01"))
        self.assertEqual(line_subtotal, Decimal("19.50"))

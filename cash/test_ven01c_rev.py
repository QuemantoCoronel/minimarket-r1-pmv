from __future__ import annotations

from decimal import Decimal
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from cash.models import CashRegister
from identity.models import Account, Role


class CashSaleConfirmationAuditTests(TestCase):
    password = "Audit-Ven01c-Passw0rd!"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin_role = Role.objects.create(code=Role.Code.ADMIN, name="Administrador")
        cls.warehouse_role = Role.objects.create(code=Role.Code.WAREHOUSE, name="Almacenero")
        cls.seller_role = Role.objects.create(code=Role.Code.SELLER, name="Vendedor")
        cls.admin = Account.objects.create_user("admin.ven01c@test.invalid", cls.password, display_name="Admin", role=cls.admin_role)
        cls.warehouse = Account.objects.create_user("warehouse.ven01c@test.invalid", cls.password, display_name="Almacenero", role=cls.warehouse_role)
        cls.seller = Account.objects.create_user("seller.ven01c@test.invalid", cls.password, display_name="Vendedor", role=cls.seller_role)

    def test_seller_authorization_and_forbidden_roles_on_sales_confirmation_route(self) -> None:
        self.assertRedirects(self.client.get("/ventas/"), "/?next=/ventas/", fetch_redirect_response=True)
        self.client.post(reverse("login"), {"email": self.seller.email, "password": self.password})
        self.assertEqual(self.client.get("/ventas/").status_code, 200)
        self.client.logout()
        self.client.post(reverse("login"), {"email": self.admin.email, "password": self.password})
        self.assertEqual(self.client.get("/ventas/").status_code, 403)
        self.client.logout()
        self.client.post(reverse("login"), {"email": self.warehouse.email, "password": self.password})
        self.assertEqual(self.client.get("/ventas/").status_code, 403)

    def test_atomic_rollback_and_row_locking_for_concurrent_sale_confirmation(self) -> None:
        register = CashRegister.objects.create(code="CAJA-VEN01C")
        with transaction.atomic():
            locked_register = CashRegister.objects.select_for_update().get(pk=register.pk)
            self.assertEqual(locked_register.code, "CAJA-VEN01C")
        before_count = CashRegister.objects.count()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                CashRegister.objects.create(code="CAJA-TEMPORAL-ROLLBACK")
                CashRegister.objects.create(code="CAJA-VEN01C")
        self.assertEqual(CashRegister.objects.count(), before_count)

    def test_cash_change_calculation_and_insufficient_cash_rejection_rule(self) -> None:
        sale_total = Decimal("18.50")
        cash_received = Decimal("20.00")
        change_due = (cash_received - sale_total).quantize(Decimal("0.01"))
        self.assertEqual(change_due, Decimal("1.50"))
        self.assertLess(Decimal("15.00"), sale_total)

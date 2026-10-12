from __future__ import annotations

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category
from identity.models import Account, Role


class InitialInventoryLoadAuditTests(TestCase):
    password = "Audit-Inv01a-Passw0rd!"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin_role = Role.objects.create(code=Role.Code.ADMIN, name="Administrador")
        cls.warehouse_role = Role.objects.create(code=Role.Code.WAREHOUSE, name="Almacenero")
        cls.seller_role = Role.objects.create(code=Role.Code.SELLER, name="Vendedor")
        cls.admin = Account.objects.create_user("admin.inv01a@test.invalid", cls.password, display_name="Admin", role=cls.admin_role)
        cls.warehouse = Account.objects.create_user("warehouse.inv01a@test.invalid", cls.password, display_name="Almacenero", role=cls.warehouse_role)
        cls.seller = Account.objects.create_user("seller.inv01a@test.invalid", cls.password, display_name="Vendedor", role=cls.seller_role)

    def test_anonymous_request_to_initial_inventory_load_redirects_to_login(self) -> None:
        response = self.client.get("/inventario/carga-inicial/")
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_only_warehouse_role_can_access_initial_inventory_load_route(self) -> None:
        self.client.post(reverse("login"), {"email": self.warehouse.email, "password": self.password})
        warehouse_res = self.client.get("/inventario/carga-inicial/")
        self.assertEqual(warehouse_res.status_code, 200)
        self.assertContains(warehouse_res, "Carga inicial")
        self.client.logout()
        self.client.post(reverse("login"), {"email": self.admin.email, "password": self.password})
        self.assertEqual(self.client.get("/inventario/carga-inicial/").status_code, 403)
        self.client.logout()
        self.client.post(reverse("login"), {"email": self.seller.email, "password": self.password})
        self.assertEqual(self.client.get("/inventario/carga-inicial/").status_code, 403)

    def test_atomic_rollback_prevents_partial_persistence_on_batch_error(self) -> None:
        initial_count = Category.objects.count()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Category.objects.create(name="Conservas Lote A")
                Category.objects.create(name="CONSERVAS LOTE A")
        self.assertEqual(Category.objects.count(), initial_count)

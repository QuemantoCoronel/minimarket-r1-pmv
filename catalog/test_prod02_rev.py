from __future__ import annotations

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category
from identity.models import Account, Role


class ProductRegistrationAuditTests(TestCase):
    """
    Suite de auditoría técnica S1-PROD02-REV (SCRUM-320 - HU-PROD-02).
    Verifica en PostgreSQL real los controles de autorización por rol en /productos/nuevo/,
    la persistencia y normalización en el módulo catalog y el estado del contrato de modelo.
    """

    password = "Audit-Only-Passw0rd!"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin_role = Role.objects.create(code=Role.Code.ADMIN, name="Administrador")
        cls.warehouse_role = Role.objects.create(code=Role.Code.WAREHOUSE, name="Almacenero")
        cls.seller_role = Role.objects.create(code=Role.Code.SELLER, name="Vendedor")

        cls.admin = Account.objects.create_user(
            "admin.prod02@test.invalid", cls.password, display_name="Admin Catálogo", role=cls.admin_role
        )
        cls.warehouse = Account.objects.create_user(
            "warehouse.prod02@test.invalid", cls.password, display_name="Almacenero", role=cls.warehouse_role
        )
        cls.seller = Account.objects.create_user(
            "seller.prod02@test.invalid", cls.password, display_name="Vendedor", role=cls.seller_role
        )

    def test_anonymous_user_cannot_access_product_registration_route(self) -> None:
        response = self.client.get("/productos/nuevo/")
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_only_admin_role_is_authorized_on_product_registration_route(self) -> None:
        self.client.post(reverse("login"), {"email": self.admin.email, "password": self.password})
        admin_response = self.client.get("/productos/nuevo/")
        self.assertEqual(admin_response.status_code, 200)
        self.assertContains(admin_response, "Registrar producto")

        self.client.logout()
        self.client.post(reverse("login"), {"email": self.warehouse.email, "password": self.password})
        warehouse_response = self.client.get("/productos/nuevo/")
        self.assertEqual(warehouse_response.status_code, 403)

        self.client.logout()
        self.client.post(reverse("login"), {"email": self.seller.email, "password": self.password})
        seller_response = self.client.get("/productos/nuevo/")
        self.assertEqual(seller_response.status_code, 403)

    def test_catalog_category_persistence_and_casefold_uniqueness_in_db(self) -> None:
        category = Category.objects.create(name="  Conservas de Pescado  ")
        self.assertEqual(category.name, "Conservas de Pescado")
        self.assertEqual(category.name_normalized, "conservas de pescado")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Category.objects.create(name="CONSERVAS DE PESCADO")
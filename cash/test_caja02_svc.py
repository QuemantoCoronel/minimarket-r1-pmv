from decimal import Decimal
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase
from cash.models import CashRegister
from cash.services import close_cash_register
from identity.models import Account, Role


class CashCloseServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.seller_role = Role.objects.create(code=Role.Code.SELLER, name="Vendedor")
        cls.seller1 = Account.objects.create_user(
            "v1@test.invalid", "Passw0rd!123", display_name="Vendedor 1", role=cls.seller_role
        )
        cls.seller2 = Account.objects.create_user(
            "v2@test.invalid", "Passw0rd!123", display_name="Vendedor 2", role=cls.seller_role
        )

    def setUp(self) -> None:
        self.register = CashRegister.objects.create(code="CAJA-SVC-1", is_active=True)
        self.register.opened_by = self.seller1
        self.register.opening_balance = Decimal("100.00")

    def test_seller_owner_authorization(self) -> None:
        with self.assertRaisesMessage(PermissionDenied, "Solo el vendedor que abrio el turno puede cerrarlo."):
            close_cash_register(self.register, self.seller2)

    def test_prevent_double_close(self) -> None:
        self.register.is_active = False
        with self.assertRaisesMessage(ValidationError, "La caja ya esta cerrada."):
            close_cash_register(self.register, self.seller1)

    def test_prevent_close_with_active_drafts(self) -> None:
        with self.assertRaisesMessage(ValidationError, "No se puede cerrar la caja si existen borradores"):
            close_cash_register(self.register, self.seller1, has_active_drafts=True)

    def test_calculate_confirmed_movements(self) -> None:
        closed_reg = close_cash_register(self.register, self.seller1, confirmed_sales_total=Decimal("50.00"))
        self.assertFalse(closed_reg.is_active)
        self.assertEqual(closed_reg.closing_balance, Decimal("150.00"))
        self.assertIsNotNone(closed_reg.closed_at)

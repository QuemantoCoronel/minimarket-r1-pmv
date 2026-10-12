from __future__ import annotations

from io import StringIO
from unittest.mock import patch

from django.core.management.base import CommandError
from django.core.management import call_command
from django.test import TestCase

from cash.models import CashRegister
from catalog.models import Category
from identity.models import Account, Role


class SeedCommandTests(TestCase):
    @patch.dict(
        "os.environ",
        {
            "SEED_ADMIN_PASSWORD": "Test-only-Admin1",
            "SEED_WAREHOUSE_PASSWORD": "Test-only-Warehouse1",
            "SEED_SELLER_PASSWORD": "Test-only-Seller1",
        },
        clear=False,
    )
    def test_seed_can_run_twice_without_duplicate_business_data(self) -> None:
        output = StringIO()
        call_command("seed_pmv", stdout=output)
        call_command("seed_pmv", stdout=output)
        self.assertEqual(Role.objects.count(), 3)
        self.assertEqual(Account.objects.count(), 4)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(CashRegister.objects.count(), 1)
        self.assertTrue(Account.objects.get(email_normalized="vendedor.demo@pmv.invalid").check_password("Test-only-Seller1"))
        self.assertNotIn("Test-only-Admin1", output.getvalue())
        self.assertNotIn("Test-only-Warehouse1", output.getvalue())
        self.assertNotIn("Test-only-Seller1", output.getvalue())

    @patch.dict(
        "os.environ",
        {"SEED_ADMIN_PASSWORD": "", "SEED_WAREHOUSE_PASSWORD": "", "SEED_SELLER_PASSWORD": ""},
        clear=False,
    )
    def test_seed_requires_all_passwords_before_mutating_data(self) -> None:
        with self.assertRaisesMessage(CommandError, "Missing required seed password environment variables"):
            call_command("seed_pmv")

        self.assertEqual(Role.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(CashRegister.objects.count(), 0)

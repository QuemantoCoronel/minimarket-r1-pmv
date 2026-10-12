from __future__ import annotations

from unittest.mock import patch

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
        call_command("seed_pmv")
        call_command("seed_pmv")
        self.assertEqual(Role.objects.count(), 3)
        self.assertEqual(Account.objects.count(), 4)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(CashRegister.objects.count(), 1)
        self.assertTrue(Account.objects.get(email_normalized="vendedor.demo@pmv.invalid").check_password("Test-only-Seller1"))


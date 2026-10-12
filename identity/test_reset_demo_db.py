"""Tests for the reset_demo_db management command (S1-DB-05)."""
from __future__ import annotations

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from cash.models import CashRegister
from catalog.models import Category
from identity.models import Account, Role


_SEED_ENV = {
    "SEED_ADMIN_PASSWORD": "Test-only-Admin1",
    "SEED_WAREHOUSE_PASSWORD": "Test-only-Warehouse1",
    "SEED_SELLER_PASSWORD": "Test-only-Seller1",
    "APP_ENV": "demo",
}


class ResetDemoDbTests(TestCase):
    """Tests for reset_demo_db command."""

    @patch.dict("os.environ", _SEED_ENV, clear=False)
    def test_reset_requires_confirm_flag(self) -> None:
        """Running without --confirm raises CommandError and mutates nothing."""
        # Populate a baseline first so we can check it stays intact.
        call_command("seed_pmv")
        self.assertEqual(Role.objects.count(), 3)

        with self.assertRaisesMessage(CommandError, "Safety flag missing"):
            call_command("reset_demo_db")

        # Data must still be intact — no accidental wipe.
        self.assertEqual(Role.objects.count(), 3)

    @patch.dict("os.environ", {**_SEED_ENV, "APP_ENV": "production"}, clear=False)
    def test_reset_blocked_in_production(self) -> None:
        """reset_demo_db raises CommandError in APP_ENV=production."""
        with self.assertRaisesMessage(CommandError, "not allowed in APP_ENV='production'"):
            call_command("reset_demo_db", confirm=True)

    @patch.dict("os.environ", {**_SEED_ENV, "APP_ENV": "test"}, clear=False)
    def test_reset_blocked_in_test_env(self) -> None:
        """reset_demo_db raises CommandError in APP_ENV=test."""
        with self.assertRaisesMessage(CommandError, "not allowed in APP_ENV='test'"):
            call_command("reset_demo_db", confirm=True)

    @patch.dict("os.environ", _SEED_ENV, clear=False)
    def test_reset_wipes_and_reseeds(self) -> None:
        """After reset, DB has exactly the baseline counts (no duplicates, no leftovers)."""
        # Seed first, then add extra dirty rows.
        call_command("seed_pmv")
        extra_role = Role.objects.create(code="EXTRA", name="Extra Role")
        self.assertEqual(Role.objects.count(), 4)

        output = StringIO()
        call_command("reset_demo_db", confirm=True, stdout=output)

        self.assertEqual(Role.objects.count(), 3)
        self.assertEqual(Account.objects.count(), 4)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(CashRegister.objects.count(), 1)
        self.assertFalse(Role.objects.filter(code="EXTRA").exists())

    @patch.dict("os.environ", _SEED_ENV, clear=False)
    def test_reset_is_idempotent(self) -> None:
        """Running reset_demo_db twice leaves exactly the baseline counts."""
        output = StringIO()
        call_command("reset_demo_db", confirm=True, stdout=output)
        call_command("reset_demo_db", confirm=True, stdout=output)

        self.assertEqual(Role.objects.count(), 3)
        self.assertEqual(Account.objects.count(), 4)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(CashRegister.objects.count(), 1)

    @patch.dict("os.environ", _SEED_ENV, clear=False)
    def test_reset_output_does_not_contain_passwords(self) -> None:
        """stdout must never expose the seed passwords."""
        output = StringIO()
        call_command("reset_demo_db", confirm=True, stdout=output)
        content = output.getvalue()
        self.assertNotIn("Test-only-Admin1", content)
        self.assertNotIn("Test-only-Warehouse1", content)
        self.assertNotIn("Test-only-Seller1", content)

from io import StringIO; from django.core.management import call_command; from django.db import IntegrityError, transaction; from django.test import TestCase; from cash.models import CashRegister; from catalog.models import Category; from identity.models import Account, Role
class DatabaseMigrationSeedResetTests(TestCase):
    def test_no_pending_migrations(self):
        call_command("makemigrations", check=True, dry_run=True, stdout=StringIO())
    def test_seed_idempotency_after_reset(self):
        call_command("flush", interactive=False, stdout=StringIO())
        call_command("seed_pmv", stdout=StringIO())
        call_command("seed_pmv", stdout=StringIO())
        self.assertEqual(Role.objects.count(), 3)
        self.assertEqual(Account.objects.count(), 4)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(CashRegister.objects.count(), 1)
    def test_unique_constraints_enforced(self):
        call_command("seed_pmv", stdout=StringIO())
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Role.objects.create(code="ADMIN", name="Duplicado")

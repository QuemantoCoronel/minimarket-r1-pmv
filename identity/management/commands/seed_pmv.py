"""Idempotent, non-secret PMV baseline data command."""
from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from cash.models import CashRegister
from catalog.models import Category
from identity.models import Account, Role


class Command(BaseCommand):
    help = "Creates idempotent roles, fictional accounts, canned-product category, and the single cash register."

    role_definitions = (
        (Role.Code.ADMIN, "Administrador"),
        (Role.Code.WAREHOUSE, "Almacenero"),
        (Role.Code.SELLER, "Vendedor"),
    )
    accounts = (
        ("admin.demo@pmv.invalid", "Administrador Demo", Role.Code.ADMIN, "SEED_ADMIN_PASSWORD", True),
        ("almacen.demo@pmv.invalid", "Almacenero Demo", Role.Code.WAREHOUSE, "SEED_WAREHOUSE_PASSWORD", True),
        ("vendedor.demo@pmv.invalid", "Vendedor Demo", Role.Code.SELLER, "SEED_SELLER_PASSWORD", True),
        ("inactiva.demo@pmv.invalid", "Cuenta Inactiva Demo", Role.Code.ADMIN, "SEED_ADMIN_PASSWORD", False),
    )

    def handle(self, *args, **options) -> None:
        # Environment is read at execution time, never copied into settings or output.
        import os

        missing = [key for key in {item[3] for item in self.accounts} if not os.environ.get(key)]
        if missing:
            raise CommandError("Missing required seed password environment variables: " + ", ".join(sorted(missing)))

        with transaction.atomic():
            roles = {}
            for code, name in self.role_definitions:
                role, _ = Role.objects.update_or_create(code=code, defaults={"name": name})
                roles[code] = role

            for email, display_name, role_code, password_env, is_active in self.accounts:
                account, created = Account.objects.get_or_create(
                    email_normalized=Account.normalize_email(email),
                    defaults={
                        "email": email,
                        "display_name": display_name,
                        "role": roles[role_code],
                        "is_active": is_active,
                    },
                )
                changed = (
                    account.email != email
                    or account.display_name != display_name
                    or account.role_id != roles[role_code].id
                    or account.is_active != is_active
                )
                if created or changed:
                    account.email = email
                    account.display_name = display_name
                    account.role = roles[role_code]
                    account.is_active = is_active
                    account.set_password(os.environ[password_env])
                    account.save()

            Category.objects.update_or_create(
                name_normalized="productos enlatados",
                defaults={"name": "Productos enlatados", "is_active": True},
            )
            CashRegister.objects.update_or_create(code="CAJA-01", defaults={"is_active": True})

        self.stdout.write(self.style.SUCCESS("PMV baseline data ensured: 3 roles, 4 fictional accounts, 1 category, 1 cash register."))

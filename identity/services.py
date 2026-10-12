"""Identity services keep authentication decisions on the server."""
from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest

from .models import Account

INVALID_CREDENTIALS_MESSAGE = "Correo o contraseña incorrectos"


@dataclass(frozen=True)
class AuthenticationResult:
    account: Account | None

    @property
    def authenticated(self) -> bool:
        return self.account is not None


def authenticate_active_account(email: str, password: str) -> AuthenticationResult:
    """Authenticate without revealing whether email, password, or activity failed."""
    normalized = Account.normalize_email(email)
    account = Account.objects.select_related("role").filter(email_normalized=normalized).first()
    if account is None:
        # Keep a comparable Argon2 verification path for unknown accounts.
        Account().set_password(password)
        return AuthenticationResult(account=None)
    if not account.is_active or not check_password(password, account.password):
        return AuthenticationResult(account=None)
    return AuthenticationResult(account=account)


def create_server_session(request: HttpRequest, account: Account) -> None:
    """Rotate the session id and store only server-side identity context."""
    login(request, account, backend="django.contrib.auth.backends.ModelBackend")
    request.session["role_code"] = account.role.code


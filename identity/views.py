from __future__ import annotations

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .authorization import roles_required
from .forms import LoginForm
from .models import Role
from .services import INVALID_CREDENTIALS_MESSAGE, authenticate_active_account, create_server_session


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = LoginForm(request.POST or None)
    status_code = 200
    if request.method == "POST":
        if form.is_valid():
            result = authenticate_active_account(
                form.cleaned_data["email"], form.cleaned_data["password"]
            )
            if result.authenticated:
                create_server_session(request, result.account)
                return redirect("dashboard")
        form.errors.clear()
        form.add_error(None, INVALID_CREDENTIALS_MESSAGE)
    return render(request, "identity/login.html", {"form": form}, status=status_code)


@login_required
@require_GET
def dashboard(request):
    return render(request, "identity/dashboard.html")


@login_required
@require_http_methods(["GET", "POST"])
def logout_view(request):
    """AUTH-03 draft disposal is added once the sales domain is integrated."""
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return render(request, "identity/logout_confirm.html")


@roles_required(Role.Code.ADMIN)
@require_GET
def product_entry(request):
    return render(request, "identity/protected_placeholder.html", {"operation": "Registrar producto"})


@roles_required(Role.Code.WAREHOUSE)
@require_GET
def inventory_load(request):
    return render(request, "identity/protected_placeholder.html", {"operation": "Carga inicial"})


@roles_required(Role.Code.SELLER)
@require_GET
def cash_open(request):
    return render(request, "identity/protected_placeholder.html", {"operation": "Abrir turno"})


@roles_required(Role.Code.SELLER)
@require_GET
def sales_counter(request):
    return render(request, "identity/protected_placeholder.html", {"operation": "Ventas"})

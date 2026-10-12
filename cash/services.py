from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from django.db import transaction

def close_cash_register(register, user, has_active_drafts=False, confirmed_sales_total=0):
    """Servicio de dominio para cierre de caja (S1-CAJA02-SVC)"""
    if not register.is_active:
        raise ValidationError("La caja ya esta cerrada.")

    opened_by = getattr(register, "opened_by", user)
    if opened_by != user:
        raise PermissionDenied("Solo el vendedor que abrio el turno puede cerrarlo.")

    if has_active_drafts:
        raise ValidationError("No se puede cerrar la caja si existen borradores con lineas activas.")

    with transaction.atomic():
        register.is_active = False
        opening_balance = getattr(register, "opening_balance", 0)
        setattr(register, "closing_balance", opening_balance + confirmed_sales_total)
        setattr(register, "closed_at", timezone.now())
        # register.save() # Se habilitara cuando la subtarea MOD agregue los campos a la DB
    return register

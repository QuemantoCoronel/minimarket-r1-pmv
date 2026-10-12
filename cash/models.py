from __future__ import annotations

import uuid

from django.db import models


class CashRegister(models.Model):
    """The single cash register seed; shifts are delivered by HU-CAJA-01."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.code


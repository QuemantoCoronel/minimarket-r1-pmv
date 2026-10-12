from __future__ import annotations

import uuid

from django.db import models


class Category(models.Model):
    """Foundation category needed by the R1 product registration flow."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    name_normalized = models.CharField(max_length=120, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name_normalized"]

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.strip()
        self.name_normalized = self.name.casefold()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


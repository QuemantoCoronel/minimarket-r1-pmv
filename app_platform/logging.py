"""Logging guards: metadata may be logged, secrets and credentials may not."""
from __future__ import annotations

import logging
import re


class RedactSensitiveDataFilter(logging.Filter):
    patterns = (
        re.compile(r"(?i)(password|token|secret|csrf|session|cookie)=([^\s&]+)"),
        re.compile(r"(?i)(authorization:\s*bearer)\s+\S+"),
    )

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        for pattern in self.patterns:
            message = pattern.sub(r"\1=[REDACTED]", message)
        record.msg = message
        record.args = ()
        return True


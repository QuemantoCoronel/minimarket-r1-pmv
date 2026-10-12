"""Logging guards: metadata may be logged, secrets and credentials may not."""
from __future__ import annotations

import logging
import re


class RedactSensitiveDataFilter(logging.Filter):
    patterns = (
        re.compile(
            r'''(?ix)
            (
                ["']?
                (?:password|password1|password2|token|secret|api[_-]?key|
                   csrf|csrfmiddlewaretoken|csrftoken|session|sessionid|cookie)
                ["']?\s*[:=]\s*
            )
            (?:"[^"]*"|'[^']*'|[^\s,;&}]+)
            '''
        ),
        re.compile(r"(?i)(authorization\s*:\s*(?:bearer|basic)\s+)\S+"),
    )

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        for pattern in self.patterns:
            message = pattern.sub(r"\1[REDACTED]", message)
        record.msg = message
        record.args = ()
        return True

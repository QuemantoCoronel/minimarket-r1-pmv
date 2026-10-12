"""Negative checks for the application security baseline (S1-SEC-02)."""

from __future__ import annotations

import logging

from django.conf import settings
from django.test import SimpleTestCase

from .logging import RedactSensitiveDataFilter


class SecurityConfigurationTests(SimpleTestCase):
    def test_cookie_session_and_header_baseline_is_enabled(self) -> None:
        self.assertEqual(settings.SESSION_ENGINE, "django.contrib.sessions.backends.db")
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, "Lax")
        self.assertTrue(settings.CSRF_COOKIE_HTTPONLY)
        self.assertEqual(settings.CSRF_COOKIE_SAMESITE, "Lax")
        self.assertEqual(settings.X_FRAME_OPTIONS, "DENY")
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertEqual(settings.SECURE_REFERRER_POLICY, "same-origin")

    def test_logging_filter_redacts_query_json_cookie_and_authorization_values(self) -> None:
        secrets = ("query-pass", "json-token", "session-value", "bearer-value", "basic-value")
        message = (
            'password=query-pass {"csrfmiddlewaretoken":"json-token"} '
            "Cookie: sessionid=session-value; Authorization: Bearer bearer-value "
            "Authorization: Basic basic-value"
        )
        record = logging.LogRecord("security-test", logging.INFO, __file__, 1, message, (), None)

        self.assertTrue(RedactSensitiveDataFilter().filter(record))

        rendered = record.getMessage()
        for secret in secrets:
            self.assertNotIn(secret, rendered)
        self.assertGreaterEqual(rendered.count("[REDACTED]"), len(secrets))

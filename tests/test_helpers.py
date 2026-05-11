from datetime import datetime, timezone

import pytest

from app import redact_passwords
from app.routes import parse_date, safe_float, safe_int


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, None),
        ("72.5", 72.5),
        ("0", 0.0),
        ("not-a-number", None),
        ("", None),
    ],
)
def test_safe_float(value, expected):
    assert safe_float(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, None),
        ("45", 45),
        ("0", 0),
        ("3.7", None),
        ("bad", None),
    ],
)
def test_safe_int(value, expected):
    assert safe_int(value) == expected


def test_parse_date_now():
    result = parse_date("now")
    assert isinstance(result, datetime)
    assert result.tzinfo == timezone.utc


def test_parse_date_iso_utc_string():
    result = parse_date("2024-01-15 12:30:45")
    assert result == datetime(2024, 1, 15, 12, 30, 45, tzinfo=timezone.utc)


def test_parse_date_invalid():
    assert parse_date("not-a-date") is None


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("http://x?foo=1&password=secret&bar=2", "http://x?foo=1&password=[REDACTED]&bar=2"),
        ("PASSWORD=abc&x=1", "PASSWORD=[REDACTED]&x=1"),
        (123, 123),
    ],
)
def test_redact_passwords(raw, expected):
    assert redact_passwords(raw) == expected

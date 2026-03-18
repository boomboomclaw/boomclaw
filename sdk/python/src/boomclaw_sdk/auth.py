"""HMAC-SHA256 signature computation and verification for the Boomclaw SDK."""

from __future__ import annotations

import hashlib
import hmac
import time


def compute_signature(
    secret: str,
    method: str,
    path: str,
    timestamp: str,
    body: str = "",
) -> str:
    """Compute an HMAC-SHA256 request signature.

    The canonical message format is::

        METHOD\\nPATH\\nTIMESTAMP\\nBODY

    Returns the hex-encoded signature string.
    """
    message = f"{method}\n{path}\n{timestamp}\n{body}"
    return hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def compute_webhook_signature(
    secret: str,
    event_type: str,
    timestamp: str,
    body: str,
) -> str:
    """Compute an HMAC-SHA256 webhook signature.

    The canonical message format is::

        EVENT_TYPE\\nTIMESTAMP\\nBODY

    Returns the hex-encoded signature string.
    """
    message = f"{event_type}\n{timestamp}\n{body}"
    return hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_webhook_signature(
    secret: str,
    headers: dict,
    body: str,
) -> bool:
    """Verify an incoming webhook request signature.

    Expected headers:

    * ``X-Boomclaw-Signature`` -- hex-encoded HMAC-SHA256
    * ``X-Boomclaw-Event`` -- event type string
    * ``X-Boomclaw-Timestamp`` -- unix timestamp string

    Returns ``True`` when the signature is valid.
    """
    signature = headers.get("X-Boomclaw-Signature") or headers.get("x-boomclaw-signature")
    event_type = headers.get("X-Boomclaw-Event") or headers.get("x-boomclaw-event")
    timestamp = headers.get("X-Boomclaw-Timestamp") or headers.get("x-boomclaw-timestamp")

    if not all([signature, event_type, timestamp]):
        return False

    expected = compute_webhook_signature(secret, event_type, timestamp, body)
    return hmac.compare_digest(signature, expected)


def current_timestamp() -> str:
    """Return the current unix timestamp as a string."""
    return str(int(time.time()))

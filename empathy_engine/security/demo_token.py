import base64
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass
from typing import Any


DEFAULT_DEMO_TOKEN_TTL_SECONDS = 300


class DemoTokenError(ValueError):
    """Raised when a demo access token cannot be trusted."""


@dataclass(frozen=True)
class DemoTokenClaims:
    issued_at: int
    expires_at: int
    nonce: str


def _b64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _canonical_payload(claims: dict[str, Any]) -> bytes:
    return json.dumps(claims, separators=(",", ":"), sort_keys=True).encode("utf-8")


def create_demo_token(
    secret: str,
    *,
    ttl_seconds: int = DEFAULT_DEMO_TOKEN_TTL_SECONDS,
    now: int | None = None,
    nonce: str | None = None,
) -> str:
    if not secret or not secret.strip():
        raise ValueError("Demo token secret must not be empty")
    if ttl_seconds <= 0:
        raise ValueError("Demo token TTL must be positive")

    issued_at = int(time.time() if now is None else now)
    payload = {
        "iat": issued_at,
        "exp": issued_at + int(ttl_seconds),
        "nonce": nonce or secrets.token_urlsafe(24),
    }
    encoded_payload = _b64url_encode(_canonical_payload(payload))
    signature = hmac.new(
        secret.encode("utf-8"),
        encoded_payload.encode("ascii"),
        hashlib.sha256,
    ).digest()
    return f"{encoded_payload}.{_b64url_encode(signature)}"


def validate_demo_token(
    token: str,
    secret: str,
    *,
    max_ttl_seconds: int = DEFAULT_DEMO_TOKEN_TTL_SECONDS,
    now: int | None = None,
) -> DemoTokenClaims:
    if not secret or not secret.strip():
        raise ValueError("Demo token secret must not be empty")
    if max_ttl_seconds <= 0:
        raise ValueError("Demo token max TTL must be positive")
    if not token or "." not in token:
        raise DemoTokenError("Demo token is missing or malformed")

    encoded_payload, encoded_signature = token.split(".", 1)
    expected_signature = hmac.new(
        secret.encode("utf-8"),
        encoded_payload.encode("ascii"),
        hashlib.sha256,
    ).digest()

    try:
        received_signature = _b64url_decode(encoded_signature)
    except (ValueError, TypeError) as error:
        raise DemoTokenError("Demo token signature is malformed") from error

    if not hmac.compare_digest(received_signature, expected_signature):
        raise DemoTokenError("Demo token signature is invalid")

    try:
        payload = json.loads(_b64url_decode(encoded_payload))
    except (ValueError, TypeError, json.JSONDecodeError) as error:
        raise DemoTokenError("Demo token payload is malformed") from error

    issued_at = int(payload["iat"])
    expires_at = int(payload["exp"])
    nonce = str(payload["nonce"])
    current_time = int(time.time() if now is None else now)

    if not nonce:
        raise DemoTokenError("Demo token nonce is missing")
    if expires_at - issued_at > max_ttl_seconds:
        raise DemoTokenError("Demo token TTL exceeds the allowed maximum")
    if issued_at > current_time + 30:
        raise DemoTokenError("Demo token issued timestamp is in the future")
    if expires_at <= current_time:
        raise DemoTokenError("Demo token has expired")

    return DemoTokenClaims(issued_at=issued_at, expires_at=expires_at, nonce=nonce)

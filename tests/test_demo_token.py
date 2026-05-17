import base64
import json

import pytest

from empathy_engine.security.demo_token import (
    DEFAULT_DEMO_TOKEN_TTL_SECONDS,
    DemoTokenError,
    create_demo_token,
    validate_demo_token,
)


def decode_payload(token: str) -> dict:
    encoded_payload = token.split(".", 1)[0]
    padding = "=" * (-len(encoded_payload) % 4)
    return json.loads(base64.urlsafe_b64decode(encoded_payload + padding))


def test_demo_token_contains_required_claims_and_validates():
    token = create_demo_token("secret", now=1_000, nonce="nonce-1")

    payload = decode_payload(token)
    claims = validate_demo_token(token, "secret", now=1_100)

    assert payload == {
        "exp": 1_000 + DEFAULT_DEMO_TOKEN_TTL_SECONDS,
        "iat": 1_000,
        "nonce": "nonce-1",
    }
    assert claims.issued_at == 1_000
    assert claims.expires_at == 1_300
    assert claims.nonce == "nonce-1"


def test_demo_token_rejects_tampering_and_wrong_secret():
    token = create_demo_token("secret", now=1_000, nonce="nonce-1")
    tampered = token[:-1] + ("A" if token[-1] != "A" else "B")

    with pytest.raises(DemoTokenError):
        validate_demo_token(tampered, "secret", now=1_100)

    with pytest.raises(DemoTokenError):
        validate_demo_token(token, "other-secret", now=1_100)


def test_demo_token_rejects_expired_or_future_tokens():
    token = create_demo_token("secret", ttl_seconds=300, now=1_000, nonce="nonce-1")
    future_token = create_demo_token("secret", ttl_seconds=300, now=2_000, nonce="nonce-2")
    long_token = create_demo_token("secret", ttl_seconds=600, now=1_000, nonce="nonce-3")

    with pytest.raises(DemoTokenError):
        validate_demo_token(token, "secret", now=1_301)

    with pytest.raises(DemoTokenError):
        validate_demo_token(future_token, "secret", now=1_000)

    with pytest.raises(DemoTokenError):
        validate_demo_token(long_token, "secret", max_ttl_seconds=300, now=1_100)


def test_demo_token_rejects_missing_values():
    with pytest.raises(ValueError):
        create_demo_token("")

    with pytest.raises(ValueError):
        create_demo_token("secret", ttl_seconds=0)

    with pytest.raises(DemoTokenError):
        validate_demo_token("", "secret")

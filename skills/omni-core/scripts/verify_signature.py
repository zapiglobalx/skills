"""Verify the x-webhook-signature header of a Z-API Omni webhook.

Follows https://developer.omni.z-api.io/webhooks/signature.md:
HMAC-SHA256 over "t\ntopic\npartition\noffset\nbody", hex, constant-time compare,
timestamp tolerance of 300 seconds. The body must be the raw bytes as received,
decompressed if the request was gzipped.

Usage in a web framework: pass request headers (case-insensitive mapping) and the raw body.
"""

import gzip
import hashlib
import hmac
import time

TOLERANCE_SECONDS = 300


def _header(headers, name):
    for key, value in headers.items():
        if key.lower() == name:
            return value
    return None


def verify(headers, raw_body: bytes, secret: str, now: float | None = None) -> bool:
    signature = _header(headers, "x-webhook-signature")
    idempotency = _header(headers, "x-idempotency-key")
    if not signature or not idempotency:
        return False

    if (_header(headers, "content-encoding") or "").lower() == "gzip":
        raw_body = gzip.decompress(raw_body)

    parts = dict(p.split("=", 1) for p in signature.split(",") if "=" in p)
    t, v1 = parts.get("t"), parts.get("v1")
    if not t or not v1 or not t.isdigit():
        return False

    now = time.time() if now is None else now
    if abs(now - int(t)) > TOLERANCE_SECONDS:
        return False

    # topic may itself contain ":", so split partition and offset from the right
    topic, partition, offset = idempotency.rsplit(":", 2)
    canonical = "\n".join([t, topic, partition, offset]).encode() + b"\n" + raw_body
    expected = hmac.new(secret.encode(), canonical, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, v1)


if __name__ == "__main__":
    # Self-test with a made-up secret and payload.
    secret = "0" * 64
    body = b'{"messageEventType":"NEW_MESSAGE"}'
    t = str(int(time.time()))
    canonical = "\n".join([t, "messages", "3", "42"]).encode() + b"\n" + body
    v1 = hmac.new(secret.encode(), canonical, hashlib.sha256).hexdigest()
    headers = {"X-Webhook-Signature": f"t={t},v1={v1}", "X-Idempotency-Key": "messages:3:42"}
    assert verify(headers, body, secret)
    assert not verify(headers, body + b" ", secret)
    assert not verify(headers, body, secret, now=int(t) + 301)
    print("ok")

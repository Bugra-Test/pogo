"""Protocol/authentication scaffolding for the B architecture.

This module deliberately does NOT contain Pokémon GO proprietary credentials,
keys, certificates, or an authentication bypass. It provides a clean place to
add a legally obtained device protocol implementation for interoperability
testing.
"""
from dataclasses import dataclass
import hashlib
import hmac


@dataclass
class DeviceIdentity:
    bluetooth_address: str = ""
    device_key_hex: str = ""
    certificate_hex: str = ""

    def validate(self):
        if self.device_key_hex and len(self.device_key_hex) != 32:
            raise ValueError("device_key_hex must contain 16 bytes (32 hex chars).")
        if self.certificate_hex and len(self.certificate_hex) % 2:
            raise ValueError("certificate_hex must contain an even number of hex chars.")


def hmac_sha256(key: bytes, message: bytes) -> bytes:
    """Generic helper for a protocol implementation supplied by the user."""
    return hmac.new(key, message, hashlib.sha256).digest()


def build_test_frame(payload: bytes) -> bytes:
    """Simple test frame used by this project; not a proprietary game frame."""
    if len(payload) > 255:
        raise ValueError("Payload too large")
    return bytes([0x56, 0x50, len(payload)]) + payload

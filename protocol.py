"""Protocol layer placeholder for future GO Plus-compatible implementation.

This module intentionally does not contain device authentication keys or
implementation intended to bypass proprietary authentication.
"""

SERVICE_UUID = "0000bbef-0000-1000-8000-00805f9b34fb"
RX_UUID = "0000bbf0-0000-1000-8000-00805f9b34fb"
TX_UUID = "0000bbf1-0000-1000-8000-00805f9b34fb"


def build_test_packet(payload: bytes) -> bytes:
    """Return a raw payload for local BLE/GATT testing."""
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError("payload bytes veya bytearray olmalı")
    return bytes(payload)

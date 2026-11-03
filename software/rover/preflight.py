"""Startup checks that do not touch GPIO."""

from __future__ import annotations

import os
import sys


def env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def pi_model() -> str | None:
    path = "/proc/device-tree/model"
    try:
        with open(path, "rb") as handle:
            text = handle.read().replace(b"\x00", b"").decode("utf-8", "replace").strip()
    except OSError:
        return None
    return text or None


def version_tuple(text: str) -> tuple[int, int]:
    parts: list[int] = []
    for chunk in text.split("."):
        digits = ""
        for char in chunk:
            if char.isdigit():
                digits += char
            else:
                break
        if digits == "":
            break
        parts.append(int(digits))
        if len(parts) == 2:
            break
    while len(parts) < 2:
        parts.append(0)
    return parts[0], parts[1]


def package_version(module, dist_name: str) -> str:
    """gpiozero 2.0.1 publishes its version via package metadata, not __version__."""
    version = getattr(module, "__version__", None)
    if isinstance(version, str) and version.strip():
        return version.strip()
    try:
        from importlib.metadata import version as dist_version

        return dist_version(dist_name)
    except Exception:
        return "0"


def gpiozero_report() -> tuple[bool, str]:
    try:
        import gpiozero
    except ImportError:
        return False, "not installed (sudo apt install python3-gpiozero python3-lgpio)"
    version = package_version(gpiozero, "gpiozero")
    if version_tuple(version) < (2, 0):
        return False, f"{version} is too old for Pi 5 (need 2.0 or newer)"
    return True, version


def picamera2_report() -> tuple[bool, str]:
    try:
        import picamera2  # noqa: F401
    except ImportError:
        return False, "not installed (sudo apt install python3-picamera2)"
    return True, "importable"


def require_gpiozero() -> None:
    ok, detail = gpiozero_report()
    if ok:
        return
    print("gpiozero: " + detail, file=sys.stderr)
    print("This project uses gpiozero. RPi.GPIO does not work on a Pi 5.", file=sys.stderr)
    raise SystemExit(1)

"""Save one JPEG from the Camera Module 3.

Live preview on the Pi is `rpicam-hello` (installed with the OS). This module
only takes a still, so a missing camera does not affect driving.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pins

log = logging.getLogger(__name__)


def capture_jpeg(path: str | Path, mock: bool = False) -> Path:
    """Write one JPEG to `path`. In mock mode the file is a stand-in, not a photo."""
    dest = Path(path)
    if mock:
        dest.write_bytes(b"\xff\xd8mock-camera\xff\xd9")
        return dest

    try:
        from picamera2 import Picamera2
    except ImportError as exc:
        raise RuntimeError(
            "picamera2 is not installed. On the Pi run: "
            "sudo apt install python3-picamera2"
        ) from exc

    picam2 = Picamera2()
    try:
        config = picam2.create_still_configuration(main={"size": pins.CAMERA_SIZE})
        picam2.configure(config)
        picam2.start()
        time.sleep(1.0)
        _set_autofocus(picam2)
        time.sleep(0.4)
        picam2.capture_file(str(dest))
    finally:
        try:
            picam2.stop()
        except Exception:
            log.debug("camera stop failed", exc_info=True)
        try:
            picam2.close()
        except Exception:
            log.debug("camera close failed", exc_info=True)
    return dest


def _set_autofocus(picam2) -> None:
    """Camera Module 3 can focus. If this board cannot, the still is still saved."""
    try:
        from libcamera import controls

        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    except Exception:
        log.info("continuous autofocus was not set; saving the still anyway")

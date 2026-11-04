#!/usr/bin/env python3
"""Drive from the terminal.

Interactive:

    python3 scripts/drive.py

One command until Ctrl+C:

    python3 scripts/drive.py forward
    python3 scripts/drive.py back
    python3 scripts/drive.py left
    python3 scripts/drive.py right

Run for a fixed time, then stop:

    python3 scripts/drive.py forward --seconds 1

Stop and exit:

    python3 scripts/drive.py stop

ROVER_MOCK=1 uses fake pins and a fixed 1.5 m reading.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rover.controller import COMMANDS, Rover, normalize_command
from rover.preflight import require_gpiozero

HELP = """commands: forward, back, left, right, stop, status, quit
forward pauses below the stop distance and continues when the path is clear
"""


def format_status(body: dict) -> str:
    distance = "—" if body["distance_cm"] is None else f"{body['distance_cm']:.0f} cm"
    moving = body["moving"]
    if body["requested"] == "forward" and not body["accepted"]:
        moving = "paused"
    return (
        f"moving={moving} requested={body['requested']} "
        f"distance={distance} blocked={body['blocked']} {body['message']}"
    )


def hold(rover: Rover, seconds: float | None) -> None:
    next_print = 0.0
    started = time.monotonic()
    while True:
        now = time.monotonic()
        if seconds is not None and now - started >= seconds:
            return
        if now >= next_print:
            print(format_status(rover.status()), flush=True)
            next_print = now + 0.5
        time.sleep(0.05)


def interactive(rover: Rover) -> None:
    print(HELP, end="")
    while True:
        try:
            line = input("rover> ")
        except EOFError:
            print()
            return
        line = line.strip().lower()
        if line == "":
            continue
        if line in {"quit", "exit", "q"}:
            return
        if line == "help":
            print(HELP, end="")
            continue
        if line == "status":
            print(format_status(rover.status()))
            continue
        try:
            print(format_status(rover.command(line)))
        except ValueError as exc:
            print(exc)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Drive Kakuji's rover from the terminal.")
    parser.add_argument(
        "command",
        nargs="?",
        help="forward, back, left, right, or stop. Omit for an interactive prompt.",
    )
    parser.add_argument(
        "--seconds",
        type=float,
        default=None,
        help="hold the command for this many seconds, then stop",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.seconds is not None and args.seconds < 0:
        print("--seconds must be >= 0", file=sys.stderr)
        return 2
    command = None
    if args.command:
        try:
            command = normalize_command(args.command)
        except ValueError as exc:
            print(exc, file=sys.stderr)
            print("commands: " + ", ".join(sorted(COMMANDS)), file=sys.stderr)
            return 2

    require_gpiozero()
    rover = Rover.create()
    try:
        if command is None:
            interactive(rover)
            return 0
        if command == "stop" and args.seconds is None:
            print(format_status(rover.command("stop")))
            return 0
        print(format_status(rover.command(command)))
        try:
            hold(rover, args.seconds)
        except KeyboardInterrupt:
            print("\nstopping")
        print(format_status(rover.command("stop")))
        return 0
    except KeyboardInterrupt:
        print("\nstopping")
        return 0
    finally:
        rover.close()
        print("motors stopped")


if __name__ == "__main__":
    raise SystemExit(main())

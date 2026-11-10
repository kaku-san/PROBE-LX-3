#!/usr/bin/env python3
"""Default: OFF-only check. --motor A/B/both: one 0.25-second unloaded pulse.

For this reviewed Pi 5 bench wiring only. The operator must separately confirm
motor supply power and clear shafts before a --motor invocation. No repeats.
"""
import argparse
import signal
import subprocess
import time

import lgpio

ENABLES = (18, 13)
DIRECTIONS = (17, 27, 22, 23)
PINS = ENABLES + DIRECTIONS
CHANNELS = {"A": (18, 17, 27), "B": (13, 22, 23)}
PULSE_US = 250_000


def require_ok(result):
    if isinstance(result, int) and result < 0:
        raise RuntimeError(f"GPIO returned error {result}")
    return result


def stopped_by_signal(signum, frame):
    raise SystemExit(f"Stopped by signal {signum}")


def restore_static_low():
    # These reviewed pins were unclaimed before this one-shot tool.
    # Keep outputs actively LOW after the kernel line requests are released.
    for group in (ENABLES, DIRECTIONS):
        subprocess.run(
            ["pinctrl", "set", ",".join(map(str, group)), "op", "pd", "dl"],
            check=True, timeout=3,
        )
    result = subprocess.run(
        ["pinctrl", "get", ",".join(map(str, PINS))],
        capture_output=True, text=True, check=True, timeout=3,
    )
    rows = result.stdout.strip().splitlines()
    if len(rows) != 6 or any("op dl pd | lo" not in row for row in rows):
        raise RuntimeError("OFF-state verification failed: " + result.stdout)
    print(result.stdout, end="", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--motor", choices=("A", "B", "both"), default=None)
    args = parser.parse_args()
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGALRM):
        signal.signal(sig, stopped_by_signal)
    signal.alarm(5)
    handle = None
    claimed = []
    cleanup_errors = []
    try:
        handle = require_ok(lgpio.gpiochip_open(0))
        info = lgpio.gpio_get_chip_info(handle)
        if not isinstance(info, (list, tuple)) or "pinctrl-rp1" not in info:
            raise RuntimeError(f"Unexpected GPIO chip: {info!r}")
        for pin in PINS:  # Enables are always claimed LOW first.
            require_ok(lgpio.gpio_claim_output(
                handle, pin, level=0, lFlags=lgpio.SET_PULL_DOWN))
            claimed.append(pin)
        if any(lgpio.gpio_read(handle, pin) != 0 for pin in PINS):
            raise RuntimeError("Initial OFF-state check failed")
        print("ALL SIX MOTOR CONTROLS LOW", flush=True)
        if args.motor is None:
            print("CHECK ONLY: no HIGH levels or motor pulse requested", flush=True)
            return
        selected = ("A", "B") if args.motor == "both" else (args.motor,)
        for channel in selected:
            enable, forward, reverse = CHANNELS[channel]
            require_ok(lgpio.gpio_write(handle, forward, 1))
        print(f"ONE PULSE: motor(s) {','.join(selected)}, 0.25 seconds each", flush=True)
        # Finite library-timed pulse; zero cycles (infinite) is never used.
        for channel in selected:
            require_ok(lgpio.tx_pulse(
                handle, CHANNELS[channel][0], PULSE_US, 20_000, pulse_cycles=1))
        deadline = time.monotonic() + 1.5
        while any(require_ok(lgpio.tx_busy(handle, CHANNELS[channel][0], lgpio.TX_PWM))
                  for channel in selected):
            if time.monotonic() > deadline:
                raise TimeoutError("Pulse did not finish on time")
            time.sleep(0.01)
        print("PULSE FINISHED; stopping all motor controls", flush=True)
    finally:
        signal.alarm(0)
        if handle is not None:
            for pin in ENABLES:
                if pin in claimed:
                    try:
                        # lgpio rejects a zero-duration stop if no PWM is active.
                        # Only cancel a running pulse. A finite pulse may finish
                        # between the busy check and stop, so handle that race.
                        if require_ok(lgpio.tx_busy(handle, pin, lgpio.TX_PWM)):
                            try:
                                require_ok(lgpio.tx_pulse(handle, pin, 0, 0))
                            except Exception as exc:
                                if ("bad PWM micros" not in str(exc) or
                                        require_ok(lgpio.tx_busy(
                                            handle, pin, lgpio.TX_PWM))):
                                    raise
                    except Exception as exc:
                        cleanup_errors.append(str(exc))
            for pin in PINS:
                if pin in claimed:
                    try:
                        require_ok(lgpio.gpio_write(handle, pin, 0))
                    except Exception as exc:
                        cleanup_errors.append(str(exc))
            try:
                require_ok(lgpio.gpiochip_close(handle))
            except Exception as exc:
                cleanup_errors.append(str(exc))
        if len(claimed) == len(PINS):
            restore_static_low()
        if cleanup_errors:
            raise RuntimeError("STOP/CLEANUP ISSUE: " + "; ".join(cleanup_errors))


if __name__ == "__main__":
    main()

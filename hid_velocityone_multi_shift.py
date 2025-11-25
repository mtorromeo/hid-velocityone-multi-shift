#!/usr/bin/env python3
import argparse
import logging
from typing import Literal

from evdev import AbsInfo, UInput, ecodes

import hid

# Modalità controller
MODE_H_PATTERN = 0
MODE_SEQUENTIAL = 1
MODE_HANDBRAKE = 2

MODE_NAMES = {
    MODE_H_PATTERN: "H-Pattern",
    MODE_SEQUENTIAL: "Sequential",
    MODE_HANDBRAKE: "Handbrake"
}

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='HID driver for Turtle Beach VelocityOne Multi-Shift')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output (DEBUG level)')
    args = parser.parse_args()

    # Configura logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(message)s',
    )
    logger = logging.getLogger(__name__)

    # Crea dispositivo virtuale gamepad
    capabilities = {
        ecodes.EV_KEY: [
            ecodes.BTN_TRIGGER,     # Gear 1
            ecodes.BTN_THUMB,       # Gear 2
            ecodes.BTN_THUMB2,      # Gear 3
            ecodes.BTN_TOP,         # Gear 4
            ecodes.BTN_TOP2,        # Gear 5
            ecodes.BTN_PINKIE,      # Gear 6
            ecodes.BTN_BASE,        # Gear 7
            ecodes.BTN_BASE2,       # Gear R (Reverse)
            ecodes.BTN_BASE3,       # Shift UP
            ecodes.BTN_BASE4,       # Shift DOWN
            ecodes.BTN_BASE5,       # High/Low
        ],
        ecodes.EV_ABS: [
            (ecodes.ABS_Y, AbsInfo(value=0, min=0, max=65535, fuzz=0, flat=0, resolution=0)),  # Handbrake
        ],
    }

    ui = UInput(capabilities, name='Turtle Beach VelocityOne Multi-Shift', version=0x1)

    logger.debug("Virtual gamepad device created!")
    logger.debug("Name: Turtle Beach VelocityOne Multi-Shift")

    device = hid.device()
    device.open(0x10f5, 0x7096)

    logger.debug("Driver running... (press Ctrl+C to exit)")

    last_gear_state: int = 0
    last_button_state: int = 0
    last_handbrake: int = 0
    current_mode: None | Literal[0, 1, 2]  = None  # Initial default mode

    try:
        while True:
            data = device.read(64)

            if not data:
                continue

            # Ignore invalid packets
            if len(data) < 5:
                continue

            # Report ID 36 (64 bytes): telemetry with mode info
            if data[0] == 36 and len(data) == 64:
                # Detect mode from bytes 18 and 63 combination
                new_mode = None
                if data[18] == 4 and data[63] == 0:
                    new_mode = MODE_H_PATTERN
                elif data[18] == 0 and data[63] == 1:
                    new_mode = MODE_SEQUENTIAL
                elif data[18] == 8 and data[63] == 2:
                    new_mode = MODE_HANDBRAKE

                if new_mode is not None and new_mode != current_mode:
                    current_mode = new_mode
                    logger.debug(f"Mode: {MODE_NAMES[current_mode]}")

                continue

            # Report ID 1 (input state)
            if data[0] != 1 or len(data) != 5:
                continue

            # Handle gears (Byte 1)
            gear_state = data[1]
            if gear_state != last_gear_state:
                gear_buttons = [
                    ecodes.BTN_TRIGGER,  # Gear 1
                    ecodes.BTN_THUMB,    # Gear 2
                    ecodes.BTN_THUMB2,   # Gear 3
                    ecodes.BTN_TOP,      # Gear 4
                    ecodes.BTN_TOP2,     # Gear 5
                    ecodes.BTN_PINKIE,   # Gear 6
                    ecodes.BTN_BASE,     # Gear 7
                    ecodes.BTN_BASE2,    # Gear R
                ]

                for i, btn in enumerate(gear_buttons):
                    old_state = (last_gear_state >> i) & 1
                    new_state = (gear_state >> i) & 1
                    if old_state != new_state:
                        ui.write(ecodes.EV_KEY, btn, new_state)
                        ui.syn()
                        gear_name = ["1", "2", "3", "4", "5", "6", "7", "R"][i]
                        logger.debug(f"Gear {gear_name}: {'PRESSED' if new_state else 'RELEASED'}")

                last_gear_state = gear_state

            # Handle buttons (Byte 2)
            button_state = data[2]
            if button_state != last_button_state:
                button_map = [
                    (0x01, ecodes.BTN_BASE4, "Shift UP"),
                    (0x02, ecodes.BTN_BASE3, "Shift DOWN"),
                    (0x04, ecodes.BTN_BASE5, "High/Low"),
                ]

                for mask, btn, name in button_map:
                    old_state = 1 if (last_button_state & mask) else 0
                    new_state = 1 if (button_state & mask) else 0
                    if old_state != new_state:
                        ui.write(ecodes.EV_KEY, btn, new_state)
                        ui.syn()
                        logger.debug(f"{name}: {'PRESSED' if new_state else 'RELEASED'}")

                last_button_state = button_state

            # Handle handbrake (Byte 3-4)
            handbrake_value = data[3] | (data[4] << 8)
            if handbrake_value != last_handbrake:
                ui.write(ecodes.EV_ABS, ecodes.ABS_Y, handbrake_value)
                ui.syn()
                handbrake_percent = (handbrake_value / 65535.0) * 100
                logger.debug(f"Handbrake: {handbrake_value} ({handbrake_percent:.1f}%)")
                last_handbrake = handbrake_value

            last_handbrake = handbrake_value

    except KeyboardInterrupt:
        logger.debug("Driver terminated by user")
    finally:
        ui.close()
        device.close()
        logger.debug("Device closed")

if __name__ == "__main__":
    main()

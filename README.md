# HID VelocityOne Multi-Shift Driver

Userspace HID driver for the [Turtle Beach VelocityOne Multi-Shift](https://eu.turtlebeach.com/products/velocity-one-multi-shift) racing shifter.

## Description

This project provides a Linux userspace driver for the Turtle Beach VelocityOne Multi-Shift controller. It maps the raw HID reports to a virtual gamepad device using `uinput`, making it compatible with games and simulators.

### Features
- **Full Input Mapping**: Supports all 7 gears + Reverse, High/Low range button, Sequential shift (Up/Down), and Handbrake (Analog axis).
- **Automatic Mode Detection**: Detects and switches behavior based on the physical controller mode (H-Pattern, Sequential, Handbrake).
- **Virtual Device**: Creates a standard `uinput` gamepad device named "Turtle Beach VelocityOne Multi-Shift".

## Requirements

- Python 3.10+
- `hidapi`
- `evdev`
- Access to `/dev/uinput` and the HID device (usually requires root or udev rules)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mtorromeo/hid-velocityone-multi-shift.git
   cd hid-velocityone-multi-shift
   ```

2. Install project in a python virtual environment:
   ```bash
   pip install .
   ```

## Usage

Run the driver (usually requires root privileges for `uinput` access):

```bash
sudo python hid_velocityone_multi_shift.py
```

### Options

- `-v`, `--verbose`: Enable verbose output (DEBUG level) to see input events and mode changes in the terminal.

## License

This project is licensed under the **GPL-2.0-or-later** license. This license was chosen specifically to allow this code to be used as a reference or directly ported for a future upstream Linux kernel driver implementation.

## Affiliate links

Consider using this affiliate links to sponsor the project.

- [amazon.it](https://amzn.to/4rjgJza)
- [amazon.de](https://amzn.to/4og6XLi)
- [amazon.co.uk](https://amzn.to/4rr3gWi)

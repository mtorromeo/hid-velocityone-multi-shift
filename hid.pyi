"""Type stubs for hidapi library (based on Cython implementation)"""

from typing import Any, TypedDict

__version__: str

class DeviceInfoDict(TypedDict, total=False):
    path: bytes
    vendor_id: int
    product_id: int
    serial_number: str
    release_number: int
    manufacturer_string: str
    product_string: str
    usage_page: int
    usage: int
    interface_number: int
    bus_type: int

def enumerate(vendor_id: int = 0, product_id: int = 0) -> list[DeviceInfoDict]:
    """Return a list of discovered HID devices.

    The fields of dict are:
     - 'path'
     - 'vendor_id'
     - 'product_id'
     - 'serial_number'
     - 'release_number'
     - 'manufacturer_string'
     - 'product_string'
     - 'usage_page'
     - 'usage'
     - 'interface_number'

    :param vendor_id: Vendor id to look for, default = 0
    :param product_id: Product id to look for, default = 0
    :return: List of device dictionaries
    """
    ...

def version_str() -> str:
    """Return a runtime version string of the hidapi C library.

    :return: version string of library
    """
    ...

class device:
    """Device class.

    A device instance can be used to read from and write to a HID device.
    """

    def open(self, vendor_id: int = 0, product_id: int = 0, serial_number: str | None = None) -> None:
        """Open the connection.

        :param vendor_id: Vendor id to connect to, default = 0
        :param product_id: Product id to connect to, default = 0
        :param serial_number: Serial number string
        :raises IOError: If open failed
        :raises RuntimeError: If already open
        """
        ...

    def open_path(self, path: bytes) -> None:
        """Open connection by path.

        :param path: Path to device
        :raises IOError: If open failed
        :raises RuntimeError: If already open
        """
        ...

    def close(self) -> None:
        """Close connection.

        This should always be called after opening a connection.
        """
        ...

    def write(self, buff: bytes | list[int] | Any) -> int:
        """Accept a list of integers (0-255) and send them to the device.

        :param buff: Data to write (must be convertible to `bytes`)
        :return: Write result
        :raises ValueError: If not open
        """
        ...

    def set_nonblocking(self, v: int) -> int:
        """Set the nonblocking flag.

        :param v: Flag value (1 or 0, True or False)
        :return: Flag result
        :raises ValueError: If not open
        """
        ...

    def read(self, max_length: int, timeout_ms: int = 0) -> list[int]:
        """Return a list of integers (0-255) from the device up to max_length bytes.

        :param max_length: Maximum number of bytes to read
        :param timeout_ms: Number of milliseconds until timeout (default: no timeout)
        :return: Read bytes as list of integers
        :raises ValueError: If not open
        :raises IOError: If read error
        """
        ...

    def get_manufacturer_string(self) -> str:
        """Return manufacturer string (e.g. vendor name).

        :return: Manufacturer string
        :raises ValueError: If connection is not opened
        :raises IOError: If get manufacturer string error
        """
        ...

    def get_product_string(self) -> str:
        """Return product string (e.g. device description).

        :return: Product string
        :raises ValueError: If connection is not opened
        :raises IOError: If get product string error
        """
        ...

    def get_serial_number_string(self) -> str:
        """Return serial number.

        :return: Serial number string
        :raises ValueError: If connection is not opened
        :raises IOError: If get serial number string error
        """
        ...

    def get_indexed_string(self, index: int) -> str:
        """Return indexed string.

        :param index: String index
        :return: Indexed string
        :raises ValueError: If connection is not opened
        :raises IOError: If get indexed string error
        """
        ...

    def send_feature_report(self, buff: bytes | list[int] | Any) -> int:
        """Accept a list of integers (0-255) and send them to the device.

        :param buff: Data to send (must be convertible into bytes)
        :return: Send result
        :raises ValueError: If not open
        """
        ...

    def get_report_descriptor(self) -> list[int]:
        """Return the HID Report Descriptor for this device.

        :return: Report descriptor as list of integers
        :raises ValueError: If connection is not opened
        :raises IOError: If read error
        """
        ...

    def get_feature_report(self, report_num: int, max_length: int) -> list[int]:
        """Receive feature report.

        :param report_num: Report number
        :param max_length: Maximum length to read
        :return: Incoming feature report as list of integers
        :raises ValueError: If connection is not opened
        :raises IOError: If read error
        """
        ...

    def get_input_report(self, report_num: int, max_length: int) -> list[int]:
        """Get input report.

        :param report_num: Report number
        :param max_length: Maximum length to read
        :return: Input report as list of integers
        :raises ValueError: If connection is not opened
        :raises IOError: If read error
        """
        ...

    def error(self) -> str:
        """Get error from device, or global error if no device is opened.

        :return: Error string
        :raises IOError: If error occurred
        """
        ...

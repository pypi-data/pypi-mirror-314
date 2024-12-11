from ..api.tool_identity import ToolIdentity
from ..rpc import RPCClient


class USBSerial:
    """A USB Serial Tool"""

    def __init__(self, rpc: RPCClient, tool_id: str):
        self._tool_id = ToolIdentity(tool_id=tool_id)
        self._rpc = rpc

    @property
    def is_available(self) -> bool:
        """Whether the usb serial device is available for read/write operations"""
        return self._rpc.tools_usb_serial_is_available(self._tool_id)

    def write(self, data: bytes) -> int | None:
        """
        Write the given bytes to the USB serial device

        Returns the number of bytes written for tools which support this feature.
        Otherwise, returns None.
        """
        return self._rpc.tools_usb_serial_write(self._tool_id, data).count

    def read(self, count: int) -> bytes:
        """Read count bytes from the USB serial device"""
        return self._rpc.tools_usb_serial_read(self._tool_id, count)

    @property
    def descriptors(self) -> dict[str, str]:
        """The usb device descriptors"""
        return self._rpc.tools_usb_serial_get_descriptors(self._tool_id)

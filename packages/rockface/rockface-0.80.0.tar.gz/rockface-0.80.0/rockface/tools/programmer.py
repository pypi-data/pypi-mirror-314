from io import IOBase

from ..api.tool_identity import ToolIdentity
from ..rpc import ReadableByteStream, RPCClient


class ByteStreamEnforcer(IOBase):
    """Ensure that the wrapped file-like object produces bytes

    If it doesn't, then it raises a TypeError with the given error message."""

    def __init__(self, src: ReadableByteStream, err_msg: str):
        self._src = src
        self._err_msg = err_msg

    def read(self, size: int = -1) -> bytes:
        "Read bytes from the wrapped file"
        res = self._src.read(size)

        if not isinstance(res, bytes):
            raise TypeError(self._err_msg)

        return res


class Programmer:
    "A Programmer"

    def __init__(self, rpc: RPCClient, tool_id: str):
        self._rpc = rpc
        self._tool_id = ToolIdentity(tool_id=tool_id)

    def reset_target(self) -> None:
        "Reset the target connected to the device"
        self._rpc.tools_programmer_reset_target(self._tool_id)

    def flash_file(self, src: ReadableByteStream) -> None:
        "Flash the target with the given file"
        enforced = ByteStreamEnforcer(
            src, "flash_file requires a file-like object opened in binary mode"
        )
        self._rpc.tools_programmer_flash(self._tool_id, enforced)

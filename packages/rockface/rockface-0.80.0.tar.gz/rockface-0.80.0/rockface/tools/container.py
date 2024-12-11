from collections.abc import Callable
from functools import partial
from io import BytesIO

from ..api.tool_identity import ToolIdentity
from ..rpc import RPCClient


class ContainerError(Exception):
    """Error caused by incorrect use of the ContainerTool"""


class _FileLikeCache:
    """Caches the file-like object retrieved by the supplied getter."""

    def __init__(self, getter: Callable[[], BytesIO]) -> None:
        self._cached: BytesIO | None = None
        self._getter = getter

    def get(self) -> BytesIO:
        """Get the cached file-like object"""
        if self._cached is None:
            self._cached = self._getter()
        return self._cached

    @classmethod
    def from_byte_producer(cls, fn: Callable[[], bytes]) -> "_FileLikeCache":
        """Construct from a function which produces bytes."""
        return cls(lambda: BytesIO(fn()))


class Job:
    def __init__(self, tool_id: ToolIdentity, rpc: RPCClient) -> None:
        self._tool_id = tool_id
        self._rpc = rpc
        self._stdout = _FileLikeCache.from_byte_producer(
            partial(self._rpc.tools_container_get_stdout, self._tool_id)
        )
        self._stderr = _FileLikeCache.from_byte_producer(
            partial(self._rpc.tools_container_get_stderr, self._tool_id)
        )

    @property
    def is_running(self) -> bool:
        """Whether the container is running"""

        return self._rpc.tools_container_get_state(self._tool_id).running

    def kill(self) -> None:
        """Send SIGKILL to the container"""

        self._signal("kill")

    def terminate(self) -> None:
        """Send SIGTERM to the container"""

        self._signal("term")

    def _signal(self, signal: str) -> None:
        """Send a signal to the container"""

        self._rpc.tools_container_signal(self._tool_id, signal)

    @property
    def stdout(self) -> BytesIO:
        """Get stdout from the container"""
        return self._stdout.get()

    @property
    def stderr(self) -> BytesIO:
        """Get stderr from the container"""
        return self._stderr.get()

    @property
    def return_code(self) -> int:
        """The return code of the job"""
        state = self._rpc.tools_container_get_state(self._tool_id)
        if state.return_code is None:
            raise ContainerError("Can't get the return code of a running container")
        return state.return_code


class ContainerTool:
    """A Container Tool"""

    def __init__(self, rpc: RPCClient, tool_id: str):
        self._tool_id = ToolIdentity(tool_id=tool_id)
        self._rpc = rpc

    def run(
        self,
        container: str,
        command: list[str],
        username: str | None = None,
        password: str | None = None,
    ) -> Job:
        """Run the command in the container"""

        self._rpc.tools_container_run(
            self._tool_id, container, command, username, password
        )
        return Job(self._tool_id, self._rpc)

    def reset(self) -> None:
        """Reset the tool"""

        self._rpc.rig_tools_reset(self._tool_id)

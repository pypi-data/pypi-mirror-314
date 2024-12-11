import os
import socket
import sys
from dataclasses import dataclass
from functools import cached_property
from types import TracebackType
from typing import Any, Callable

from .client import APIParams, RigInfo, RockfaceClient
from .rpc import RPCClient
from .tools.container import ContainerTool
from .tools.gpio import GPIOTool
from .tools.logic_analyser import LogicAnalyser
from .tools.programmer import Programmer
from .tools.psu import PSUTool
from .tools.usb_serial import USBSerial


@dataclass(frozen=True)
class RigSelector:
    "A description of a method of selecting a rig"

    name: str | None = None

    def matches(self, rig_info: RigInfo) -> bool:
        return self.name == rig_info.name


tool_factories = {
    "gpio": GPIOTool,
    "programmer": Programmer,
    "logic_analyser": LogicAnalyser,
    "psu": PSUTool,
    "serial": USBSerial,
    "container": ContainerTool,
}


class BoundRig:
    """A rockface rig

    This class is not intended to be instantiated directly.  Use the
    ``Rig`` class to get an instance of this class.
    """

    def __init__(
        self,
        rpc: RPCClient,
        info: RigInfo,
        tool_factories: dict[str, Any] = tool_factories,
    ):
        self._tool_factories = tool_factories
        self._rpc: RPCClient | None = rpc
        self._info = info

    @classmethod
    def from_unlocked_rpc(cls, unlocked_rpc: RPCClient, info: RigInfo) -> "BoundRig":
        owner = f"{socket.gethostname()}-{os.getpid()}"
        token = unlocked_rpc.rig_lock_acquire(owner)
        rpc = unlocked_rpc.clone_with_rig_lock_token(token)
        return cls(rpc, info)

    @classmethod
    def from_selector(
        cls,
        selector: RigSelector,
        rockface_client: RockfaceClient,
    ) -> "BoundRig":
        matching_rigs = (rig for rig in rockface_client.rigs if selector.matches(rig))
        try:
            rig = next(matching_rigs)
        except StopIteration:
            raise LookupError(f"No rig found matching {selector}")
        return cls.from_unlocked_rpc(rig.build_rpc(), rig)

    def __enter__(self) -> "BoundRig":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.release()

    def release(self) -> None:
        "Release the lock on this rig"
        if self._rpc is None:
            raise Exception("Rig lock is already released")

        self._rpc.rig_lock_release()
        self._rpc = None

    def __del__(self) -> None:
        if hasattr(self, "_rpc") and self._rpc is not None:
            self.release()

    @property
    def info(self) -> RigInfo:
        return self._info

    @property
    def name(self) -> str:
        "The name of the rig"
        assert self._info is not None
        return self._info.name

    @cached_property
    def tools(self) -> dict[str, Any]:
        "The set of tools we have on the rig"
        assert self._rpc is not None
        resp = self._rpc.rig_tools_list()
        tools = {}

        for desc in resp:
            if desc.kind not in self._tool_factories:
                print(  # noqa: T201
                    f"Warning: tool type '{desc.kind}' is ignored by this version of the rockface library.",
                    file=sys.stderr,
                )
                continue
            tool = self._tool_factories[desc.kind](self._rpc, desc.id)
            tools[desc.id] = tool

        return tools


class Rig:
    """'Construction' class for a rig

    To construct, use the ``find_by_name`` classmethod.

    This method will find your rig, acquire a lock on it, and
    return the rig to you to use.

    Use the returned Rig as a context manager to scope the lock
    within your code:

      with Rig.find_by_name("parrot") as rig:
          # Use ``rig`` to do whatever you like
          ...

    If you don't want to use this as a context manager, you don't
    have to, but the lock will only be dropped when the returned
    rig object is garbage collected, which can result in surprising
    situations.

    Taking the lock can be delegated to a later point in time
    by providing the ``lock=False`` parameter.  Use the resulting
    object as a context manager to lock the rig:

      rig = Rig.find_by_name("cheese")
      with rig:
          # `rig` is locked within this context
    """

    def __init__(self, *args: Any, **kw: Any) -> None:
        self._args = args
        self._kw = kw
        self._bound: BoundRig | None = None

    def __enter__(self) -> "BoundRig":
        "Select and lock a rig"
        if self._bound is not None:
            raise Exception("Rig is already bound")
        self._bound = BoundRig.from_selector(*self._args, **self._kw)
        return self._bound

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        "Release the locked rig"
        if self._bound is not None:
            self._bound.release()
            self._bound = None

    @classmethod
    def _by_selector(
        cls,
        selector: RigSelector,
        lock: bool = True,
        bound_rig_factory: Callable[..., BoundRig] = BoundRig.from_selector,
        rockface_client_factory: Callable[..., RockfaceClient] = RockfaceClient,
        api_key: str | None = None,
        api_base_url: str | None = None,
    ) -> "Rig | BoundRig":
        "Use the given selector to find the rig"
        kw = {"api_key": api_key, "api_base_url": api_base_url}
        api_params = APIParams(**{k: v for k, v in kw.items() if v is not None})
        client = rockface_client_factory(api_params)
        if lock:
            "Lock the rig immediately"
            return bound_rig_factory(selector, rockface_client=client)
        return cls(selector, rockface_client=client)

    @classmethod
    def find_by_name(cls, name: str, lock: bool = True, **kw: Any) -> "Rig | BoundRig":
        "Use the rig with the given name"
        selector = RigSelector(name=name)
        return cls._by_selector(selector, lock=lock, **kw)

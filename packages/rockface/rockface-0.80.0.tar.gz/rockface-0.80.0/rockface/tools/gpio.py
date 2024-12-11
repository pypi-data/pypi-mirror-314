__all__ = [
    "PlaylistEntry",
    "PlaylistState",
    "SignalConfig",
    "SignalMode",
    "SignalState",
    "GPIOTool",
    "Signal",
    "Playlist",
]

from datetime import timedelta

from ..api.tool_identity import ToolIdentity
from ..api.tools.gpio import (
    PlaylistEntry,
    PlaylistState,
    SignalConfig,
    SignalMode,
    SignalState,
)
from ..rpc import RPCClient


class GPIOTool:
    "A GPIO tool"

    def __init__(self, rpc: RPCClient, tool_id: str):
        self._rpc = rpc
        self._tool_id = ToolIdentity(tool_id=tool_id)

        signal_names = self._rpc.tools_gpio_get_signals(self._tool_id)
        self._signals = {
            name: Signal(name, self._rpc, self._tool_id) for name in signal_names
        }

    def reset(self) -> None:
        """Reset the device

        All GPIO pins will be restored to their default state"""
        self._rpc.rig_tools_reset(self._tool_id)

    @property
    def signals(self) -> dict[str, "Signal"]:
        """A dict of the signals available on this GPIO tool

        The keys of this dictionary are the names of the signals.
        The values are Signal objects."""
        return self._signals

    def play(self, playlist: "Playlist") -> None:
        "Play the given playlist"
        self._rpc.tools_gpio_playlist_play(self._tool_id, playlist._entries)

    @property
    def playlist_running(self) -> bool:
        "Whether a playlist is currently running"
        state = self._rpc.tools_gpio_playlist_get_state(self._tool_id)
        return state == PlaylistState.PLAYING

    def stop_playlist(self) -> None:
        "Stop any currently running playlist"
        self._rpc.tools_gpio_playlist_stop(self._tool_id)


class Signal:
    "A signal on a GPIO tool"

    def __init__(self, name: str, rpc: RPCClient, tool_id: ToolIdentity):
        self._name = name
        self._tool_id = tool_id
        self._rpc = rpc

    @property
    def state(self) -> SignalState:
        """The state of the signal

        See SignalState type for the possible states.  Setting this
        property will modify the state of the signal."""
        return self._rpc.tools_gpio_signal_get_state(self._name, self._tool_id)

    @state.setter
    def state(self, value: SignalState) -> None:
        self._rpc.tools_gpio_signal_set_state(self._name, value, self._tool_id)

    @property
    def config(self) -> SignalConfig:
        """The signal configuration

        See the SignalConfig type for details.  Setting this property
        will modify the signal configuration."""
        return self._rpc.tools_gpio_signal_get_configuration(self._name, self._tool_id)

    @config.setter
    def config(self, config: SignalConfig) -> None:
        self._rpc.tools_gpio_signal_configure(self._name, config, self._tool_id)


class Playlist:
    "A series of timed changes in signal values"

    def __init__(self) -> None:
        self._entries: list[PlaylistEntry] = []

    def set_active(self, signal: str | Signal) -> None:
        """Add an entry to the playlist that makes the given signal active"""
        self._set_state(signal, SignalState.ACTIVE)

    def set_inactive(self, signal: str | Signal) -> None:
        """Add an entry to the playlist that makes the given signal inactive"""
        self._set_state(signal, SignalState.INACTIVE)

    def _set_state(self, signal: str | Signal, state: SignalState) -> None:
        if isinstance(signal, Signal):
            n = signal._name
        else:
            n = signal

        entry = PlaylistEntry(signal=n, state=state)
        self._entries.append(entry)

    def delay(self, delay: timedelta) -> None:
        """Add a time delay to the playlist"""
        try:
            last = self._entries[-1]
        except IndexError:
            raise ValueError("A playlist cannot begin with a delay")

        last.delay_ms += int(delay / timedelta(milliseconds=1))

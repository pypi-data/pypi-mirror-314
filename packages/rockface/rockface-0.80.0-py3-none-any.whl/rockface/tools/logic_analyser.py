from dataclasses import dataclass

import polars as pl

from ..api.tool_identity import ToolIdentity
from ..api.tools.logic_analyser import RecordingState
from ..rpc import RPCClient


@dataclass(frozen=True)
class Recording:
    """
    A recording made with the logic analyser tool

    sample_rate_hz: the sampling frequency that was used (Hz)
    data: a polars DataFrame with one column per signal
    """

    sample_rate_hz: int
    data: pl.DataFrame


class LogicAnalyser:
    "A logic analyser tool"

    def __init__(self, rpc: RPCClient, tool_id: str):
        self._rpc = rpc
        self._tool_id = ToolIdentity(tool_id=tool_id)

    def reset(self) -> None:
        """Reset the tool

        Any existing data stored in the tool will be erased,
        and any running recording session will be stopped."""
        self._rpc.rig_tools_reset(self._tool_id)

    def start_recording(
        self, signals: list[str], sample_rate_hz: int, samples: int
    ) -> None:
        """Start a recording

        Request that the logic analyser records the given signals
        at the given sample rate for the given number of samples."""
        self._rpc.tools_logic_analyser_start_recording(
            self._tool_id, signals, sample_rate_hz, samples
        )

    @property
    def data(self) -> Recording:
        "Retrieve the last recording made"
        rec = self._rpc.tools_logic_analyser_get_data(self._tool_id)

        return Recording(
            sample_rate_hz=rec["sample_rate_hz"],
            data=pl.DataFrame(rec["samples"], orient="row", schema=rec["signals"]),
        )

    @property
    def is_recording(self) -> bool:
        "Whether or not the device is currently recording"
        r = self._rpc.tools_logic_analyser_get_recording_state(self._tool_id)
        return r == RecordingState.RECORDING

    @property
    def signals(self) -> tuple[str, ...]:
        "The names of the signals that this tool can record"
        r = self._rpc.tools_logic_analyser_get_signals(self._tool_id)
        return tuple(r)

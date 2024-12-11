from enum import Enum

from pydantic import BaseModel


class SignalListModel(BaseModel):
    "List of signals"

    __root__: list[str]


class SampleRatesModel(BaseModel):
    "List of sample rates (Hz)"

    __root__: list[int]


class RecordingState(str, Enum):
    "Logic analyser recording state"

    IDLE = "idle"
    RECORDING = "recording"


class RecordingStateModel(BaseModel):
    "Model for the response from the tools.logic_analyser.get_recording_state endpoint"

    __root__: RecordingState


class StartRecordingParams(BaseModel):
    "Parameters for the tools.logic_analyser.start_recording endpoint"

    tool_id: str
    signals: list[str]
    sample_rate_hz: int
    samples: int


class Recording(BaseModel):
    """A recording made with a logic analyser"""

    # The names of the signals that were sampled
    signals: tuple[str, ...]
    sample_rate_hz: int

    # The samples that were taken in the recording.
    # Indexing: samples[sample_number][signal_index]
    # Where signame_index is the index into the signals
    # tuple from above.
    samples: tuple[tuple[bool, ...], ...]

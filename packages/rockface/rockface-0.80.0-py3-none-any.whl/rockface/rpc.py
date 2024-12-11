import base64
import time
from typing import Any, Protocol

import requests
from pydantic import parse_obj_as

from .api import rig as api_rig
from .api import rig_lock as api_rig_lock
from .api.quantity import Quantity, QuantityRequest
from .api.tool_identity import ToolIdentity
from .api.tools import container as api_container
from .api.tools import gpio as api_gpio
from .api.tools import logic_analyser as api_la
from .api.tools import psu as api_psu
from .api.tools import usb_serial as api_usb_serial


class ReadableByteStream(Protocol):
    "Protocol for a file-like object that produces bytes when read"

    def read(self, size: int) -> bytes:
        pass


MultiPartFile = tuple[str, ReadableByteStream, str]


class RPCClient:
    "Adapter for interacting with the rockface HTTP API"

    def __init__(self, base_url: str, api_key: str, rig_lock_token: str | None = None):
        self._base_url = base_url
        self._api_key = api_key
        self._last_request_time: None | float = None
        self._session = requests.Session()
        self._rig_lock_token = rig_lock_token

    def clone_with_rig_lock_token(self, token: str) -> "RPCClient":
        "Create a new RPCClient that uses the given rig lock token"
        return RPCClient(
            base_url=self._base_url, api_key=self._api_key, rig_lock_token=token
        )

    def call(
        self,
        method: str,
        params: Any = None,
        files: None | list[tuple[str, MultiPartFile]] = None,
    ) -> Any:
        """Call an RPC method

        method: Name of the endpoint
        params: Parameters for the call.
                Can be a pydantic type, or just a dictionary.
        files: List of files to provide with the request.
        """
        kw: dict[str, Any] = {"files": [] if files is None else files}

        if hasattr(params, "dict"):
            params = params.dict()

        if params is not None:
            if files is not None:
                """Cannot send JSON request simultaneously with files,
                so send the parameters as form data instead."""
                kw["data"] = params
            else:
                kw["json"] = params

        kw["headers"] = {"rockface-api-token": self._api_key}

        if self._rig_lock_token is not None:
            kw["headers"]["rockface-rig-lock-token"] = self._rig_lock_token

        if (
            self._last_request_time is not None
            and self._last_request_time - time.monotonic() > 60
        ):
            """The server's keepalive timeout is set to 120s, and we have not talked
            to it in nearly that time.  Unfortunately requests has an issue if
            we an issue a request at roughly the same time as the connection timeout
            and restart the session if we have potentially timed-out.
            https://github.com/psf/requests/issues/4664"""
            self._session.close()
            self._session = requests.Session()

        r = self._session.post(f"{self._base_url}/{method}", **kw)
        self._last_request_time = time.monotonic()
        r.raise_for_status()
        return r.json()

    def rig_tools_list(self) -> list[api_rig.ToolIdentity]:
        "List the tools on the rig"
        resp = self.call("rig.tools.list")
        return parse_obj_as(list[api_rig.ToolIdentity], resp)

    def rig_tools_reset(self, tool_id: ToolIdentity) -> None:
        self.call("rig.tools.reset", tool_id)

    def rig_lock_acquire(self, owner: str) -> str:
        "Acquire the rig lock"
        resp = self.call("rig.lock.acquire", {"owner": owner})
        return api_rig_lock.RigLockToken.parse_obj(resp).token

    def rig_lock_release(self) -> None:
        "Release the rig lock"
        self.call("rig.lock.release")

    def rig_lock_force_release(self, holder_name: str | None = None) -> None:
        "Force the release of lock, even if we are not the current holder"
        params = {}
        if holder_name is not None:
            params["holder_name"] = holder_name

        self.call("rig.lock.force_release", params)

    def rig_lock_get_holder(self) -> api_rig_lock.RigLockHolder:
        "Get the current holder of the rig lock"
        resp = self.call("rig.lock.get_holder")
        return api_rig_lock.RigLockHolder.parse_obj(resp)

    def tools_gpio_identify(self) -> ToolIdentity:
        "Retrieve the identity of a GPIO tool"
        resp = self.call("tools.gpio.identify")
        return ToolIdentity.parse_obj(resp)

    def tools_gpio_get_signals(self, tool_id: ToolIdentity) -> list[str]:
        "Get the signals available on a GPIO tool"
        resp = self.call("tools.gpio.get_signals", tool_id)
        return api_gpio.SignalListModel.parse_obj(resp).__root__

    def tools_gpio_signal_configure(
        self, signal: str, config: api_gpio.SignalConfig, tool_id: ToolIdentity
    ) -> None:
        "Configure a signal on a GPIO tool"
        param = api_gpio.SignalConfigureParams(
            tool_id=tool_id.tool_id, signal=signal, config=config
        )
        self.call("tools.gpio.signal.configure", param)

    def tools_gpio_signal_get_configuration(
        self, signal: str, tool_id: ToolIdentity
    ) -> api_gpio.SignalConfig:
        "Get the configuration of a signal on a GPIO tool"
        param = api_gpio.SignalGetParams(tool_id=tool_id.tool_id, signal=signal)
        resp = self.call("tools.gpio.signal.get_configuration", param)
        return api_gpio.SignalConfig.parse_obj(resp)

    def tools_gpio_signal_set_state(
        self, signal: str, state: api_gpio.SignalState, tool_id: ToolIdentity
    ) -> None:
        "Set the state of a signal on a GPIO tool"
        param = api_gpio.SignalSetStateParams(
            tool_id=tool_id.tool_id, signal=signal, state=state
        )
        self.call("tools.gpio.signal.set_state", param)

    def tools_gpio_signal_get_state(
        self, signal: str, tool_id: ToolIdentity
    ) -> api_gpio.SignalState:
        "Get the state of a signal on a GPIO tool"
        param = api_gpio.SignalGetParams(tool_id=tool_id.tool_id, signal=signal)
        resp = self.call("tools.gpio.signal.get_state", param)
        return api_gpio.SignalStateModel.parse_obj(resp).__root__

    def tools_gpio_playlist_play(
        self, tool_id: ToolIdentity, playlist: list[api_gpio.PlaylistEntry]
    ) -> None:
        "Play a playlist on a GPIO tool"
        param = api_gpio.PlaylistPlayParams(tool_id=tool_id.tool_id, playlist=playlist)
        self.call("tools.gpio.playlist.play", param)

    def tools_gpio_playlist_get_state(
        self, tool_id: ToolIdentity
    ) -> api_gpio.PlaylistState:
        "Get the playlist playback state of a GPIO tool"
        resp = self.call("tools.gpio.playlist.get_state", tool_id)
        return api_gpio.PlaylistStateModel.parse_obj(resp).__root__

    def tools_gpio_playlist_stop(self, tool_id: ToolIdentity) -> None:
        "Make a GPIO tool stop playing its playlist"
        self.call("tools.gpio.playlist.stop", tool_id)

    def tools_programmer_reset_target(self, tool_id: ToolIdentity) -> None:
        "Reset the target connected to a programmer tool"
        self.call("tools.programmer.reset_target", tool_id)

    def tools_programmer_flash(
        self, tool_id: ToolIdentity, src: ReadableByteStream
    ) -> None:
        "Load the given hex file into the target connected to a programmer tool"
        self.call(
            "tools.programmer.flash",
            tool_id,
            files=[("file", ("src.hex", src, "application/octet-stream"))],
        )

    def tools_logic_analyser_get_signals(self, tool_id: ToolIdentity) -> list[str]:
        "Get the list of signals on a logic analyser tool"
        r = self.call("tools.logic_analyser.get_signals", tool_id)
        return api_la.SignalListModel.parse_obj(r).__root__

    def tools_logic_analyser_get_sample_rates(self, tool_id: ToolIdentity) -> list[int]:
        "Get the sample rates a logic analyser tool supports"
        r = self.call("tools.logic_analyser.get_sample_rates", tool_id)
        return api_la.SampleRatesModel.parse_obj(r).__root__

    def tools_logic_analyser_get_recording_state(
        self, tool_id: ToolIdentity
    ) -> api_la.RecordingState:
        "Get the recording state of a logic analyser"
        r = self.call("tools.logic_analyser.get_recording_state", tool_id)
        return api_la.RecordingStateModel.parse_obj(r).__root__

    def tools_logic_analyser_start_recording(
        self,
        tool_id: ToolIdentity,
        signals: list[str],
        sample_rate_hz: int,
        samples: int,
    ) -> None:
        "Make a logic analyser tool start recording"
        param = api_la.StartRecordingParams(
            tool_id=tool_id.tool_id,
            signals=signals,
            sample_rate_hz=sample_rate_hz,
            samples=samples,
        )
        self.call("tools.logic_analyser.start_recording", param)

    def tools_logic_analyser_get_data(self, tool_id: ToolIdentity) -> Any:
        "Retrieve the recorded data from a logic analyser tool"
        return self.call("tools.logic_analyser.get_data", tool_id)

    def tools_psu_enable(self, tool_id: ToolIdentity) -> None:
        "Enable the output of a power supply tool"
        self.call("tools.psu.enable", tool_id)

    def tools_psu_disable(self, tool_id: ToolIdentity) -> None:
        "Disable the output of a power supply tool"
        self.call("tools.psu.disable", tool_id)

    def tools_psu_get_state(self, tool_id: ToolIdentity) -> api_psu.PSUState:
        "Get the state of a power supply tool"
        r = self.call("tools.psu.get_state", tool_id)
        return api_psu.PSUState.parse_obj(r)

    def tools_psu_get_capabilities(self, tool_id: ToolIdentity) -> api_psu.PSUSpec:
        "Get the capabilities of a power supply tool"
        r = self.call("tools.psu.get_capabilities", tool_id)
        return api_psu.PSUSpec.parse_obj(r)

    def tools_psu_set_voltage_setpoint(
        self,
        tool_id: ToolIdentity,
        quantity: Quantity,
    ) -> None:
        "Set the voltage setpoint of a power supply tool"
        self.call(
            "tools.psu.set_voltage_setpoint",
            QuantityRequest(
                tool_id=tool_id.tool_id,
                magnitude=quantity.magnitude,
            ),
        )

    def tools_psu_get_voltage_setpoint(self, tool_id: ToolIdentity) -> Quantity:
        "Get the voltage setpoint of a power supply tool"
        return Quantity.parse_obj(self.call("tools.psu.get_voltage_setpoint", tool_id))

    def tools_psu_get_current_limit(self, tool_id: ToolIdentity) -> Quantity:
        "Get the current limit of a power supply tool"
        return Quantity.parse_obj(self.call("tools.psu.get_current_limit", tool_id))

    def tools_psu_set_current_limit(
        self, tool_id: ToolIdentity, quantity: Quantity
    ) -> None:
        "Set the current limit of a power supply tool"
        self.call(
            "tools.psu.set_current_limit",
            QuantityRequest(
                tool_id=tool_id.tool_id,
                magnitude=quantity.magnitude,
            ),
        )

    def tools_psu_clear_trip(self, tool_id: ToolIdentity) -> None:
        self.call("tools.psu.clear_trip", tool_id)

    def tools_psu_get_current_limit_mode(
        self, tool_id: ToolIdentity
    ) -> api_psu.CurrentLimitMode:
        return api_psu.CurrentLimitMode(
            self.call("tools.psu.get_current_limit_mode", tool_id)["current_limit_mode"]
        )

    def tools_psu_set_current_limit_mode(
        self, tool_id: ToolIdentity, current_limit_mode: api_psu.CurrentLimitMode
    ) -> None:
        self.call(
            "tools.psu.set_current_limit_mode",
            api_psu.CurrentLimitModeParams(
                tool_id=tool_id.tool_id, current_limit_mode=current_limit_mode
            ),
        )

    def tools_usb_serial_is_available(self, tool_id: ToolIdentity) -> bool:
        "Determine if the USB device associated with a USB serial tool is available"
        return bool(self.call("tools.usb_serial.is_available", tool_id))

    def tools_usb_serial_write(
        self, tool_id: ToolIdentity, data: bytes
    ) -> api_usb_serial.WriteResponse:
        "Write some data via a USB serial tool"
        ascii_encoded = base64.b64encode(data).decode("ascii")
        param = api_usb_serial.WriteParams(tool_id=tool_id.tool_id, data=ascii_encoded)
        r = self.call("tools.serial.write", param)
        return api_usb_serial.WriteResponse.parse_obj(r)

    def tools_usb_serial_read(self, tool_id: ToolIdentity, count: int) -> bytes:
        "Read some data from a USB serial tool"
        param = api_usb_serial.ReadParams(tool_id=tool_id.tool_id, count=count)
        return base64.b64decode(self.call("tools.serial.read", param))

    def tools_usb_serial_get_descriptors(self, tool_id: ToolIdentity) -> dict[str, str]:
        "Get the USB descriptors associated with a USB serial tool"
        return dict(self.call("tools.usb_serial.get_descriptors", tool_id))

    def tools_container_run(
        self,
        tool_id: ToolIdentity,
        container: str,
        command: list[str],
        username: str | None,
        password: str | None,
    ) -> None:
        self.call(
            "tools.container.run",
            api_container.RunRequest(
                tool_id=tool_id.tool_id,
                container=container,
                command=command,
                username=username,
                password=password,
            ),
        )

    def tools_container_signal(self, tool_id: ToolIdentity, signal: str) -> None:
        self.call(
            "tools.container.signal",
            api_container.SignalRequest(tool_id=tool_id.tool_id, signal=signal),
        )

    def tools_container_get_stdout(self, tool_id: ToolIdentity) -> bytes:
        response = api_container.GetStdoutResponse.parse_obj(
            self.call("tools.container.get_stdout", tool_id)
        )
        return base64.b64decode(response.stdout)

    def tools_container_get_stderr(self, tool_id: ToolIdentity) -> bytes:
        response = api_container.GetStderrResponse.parse_obj(
            self.call("tools.container.get_stderr", tool_id)
        )
        return base64.b64decode(response.stderr)

    def tools_container_get_state(
        self, tool_id: ToolIdentity
    ) -> api_container.GetStateResponse:
        return api_container.GetStateResponse.parse_obj(
            self.call("tools.container.get_state", tool_id)
        )

from rockface.api.quantity import Quantity
from rockface.api.tools.psu import CurrentLimitMode, PSUMode, PSUSpec, PSUState

from ..api.tool_identity import ToolIdentity
from ..rpc import RPCClient


class PSUConfig:
    "The configuration of a power supply tool"

    def __init__(self, psu: "PSUTool"):
        self._psu = psu

    @property
    def voltage(self) -> float:
        """The voltage setpoint

        This is the voltage that the power supply will attempt to
        drive its output to.  Set this property to modify the
        setpoint."""
        return self._psu._rpc.tools_psu_get_voltage_setpoint(
            self._psu._tool_id
        ).magnitude

    @voltage.setter
    def voltage(self, voltage: float) -> None:
        self._psu._rpc.tools_psu_set_voltage_setpoint(
            self._psu._tool_id, Quantity(magnitude=voltage)
        )

    @property
    def current_limit(self) -> float:
        """The current limit magnitude

        This is the maximum current that the power supply will
        deliver to the load.  Set this property to modify it."""
        return self._psu._rpc.tools_psu_get_current_limit(self._psu._tool_id).magnitude

    @current_limit.setter
    def current_limit(self, current_limit: float) -> None:
        self._psu._rpc.tools_psu_set_current_limit(
            self._psu._tool_id, Quantity(magnitude=current_limit)
        )

    @property
    def current_limit_mode(self) -> CurrentLimitMode:
        """The type of current limiting in use

        See the CurrentLimitMode type for a description of possible
        values.   Set this property to change mode.
        """
        return self._psu._rpc.tools_psu_get_current_limit_mode(self._psu._tool_id)

    @current_limit_mode.setter
    def current_limit_mode(self, current_limit_mode: CurrentLimitMode) -> None:
        self._psu._rpc.tools_psu_set_current_limit_mode(
            self._psu._tool_id, current_limit_mode
        )


class PSUTool:
    "A PSU tool"

    def __init__(self, rpc: RPCClient, tool_id: str):
        self._rpc = rpc
        self._tool_id = ToolIdentity(tool_id=tool_id)

    def reset(self) -> None:
        """Reset the tool

        The existing configuration will be lost and the output will be disabled
        """
        self._rpc.rig_tools_reset(self._tool_id)

    @property
    def _state(self) -> PSUState:
        return self._rpc.tools_psu_get_state(self._tool_id)

    @property
    def enabled(self) -> bool:
        """Whether or not the output is enabled"""
        return self._state.enabled

    @enabled.setter
    def enabled(self, enable: bool) -> None:
        if enable:
            self._rpc.tools_psu_enable(self._tool_id)
        else:
            self._rpc.tools_psu_disable(self._tool_id)

    @property
    def tripped(self) -> bool:
        """Whether the tool has disabled its output as a result of exceeding its current limit"""
        return self._state.tripped

    @tripped.setter
    def tripped(self, tripped: bool) -> None:
        if tripped:
            raise ValueError("tripped state can only be cleared")
        self._rpc.tools_psu_clear_trip(self._tool_id)

    @property
    def current(self) -> float:
        """The output current measured by the power supply, in amps

        For the configured current limit see PSUTool.config
        """
        return self._state.current

    @property
    def voltage(self) -> float:
        """The output voltage measured by the power supply, in volts

        For the configured voltage see PSUTool.config
        """
        return self._state.voltage

    @property
    def in_constant_current(self) -> bool:
        """Whether or not the device is in constant current mode"""
        return self._state.mode == PSUMode.CONSTANT_CURRENT

    @property
    def in_constant_voltage(self) -> bool:
        """Whether or not the device is in constant voltage mode"""
        return self._state.mode == PSUMode.CONSTANT_VOLTAGE

    @property
    def spec(self) -> PSUSpec:
        """The tool specification"""
        return self._rpc.tools_psu_get_capabilities(self._tool_id)

    @property
    def config(self) -> PSUConfig:
        """The configuration of the tool"""
        return PSUConfig(self)

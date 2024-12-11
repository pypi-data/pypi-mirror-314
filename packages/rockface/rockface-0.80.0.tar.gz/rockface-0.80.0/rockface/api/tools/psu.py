from enum import Enum
from math import isclose

from pydantic import BaseModel, confloat, root_validator

from ...api.tool_request import ToolRequest


class CurrentLimitMode(str, Enum):
    """The behaviour of a PSU tool when the current limit is reached

    LIMIT: The power supply will enter into "constant current" mode
           if the limit is reached -- i.e. it will reduce the voltage
           it is delivering to the load to keep the current below the
           limit.
    TRIP: If the current delivered to the load exceeds the limit, then
          the power supply will turn off."""

    LIMIT = "limit"
    TRIP = "trip"


class CurrentLimitModeParams(ToolRequest):
    "Parameters for the tools.psu.set_current_limit_mode endpoint"

    current_limit_mode: CurrentLimitMode


class PSUMode(str, Enum):
    """The operating mode of a PSU tool."""

    CONSTANT_CURRENT = "constant current"
    CONSTANT_VOLTAGE = "constant voltage"


class PSUState(BaseModel):
    """
    The state of a PSU tool

    Attributes:
        voltage (float): The output voltage in volts.
        current (float): The output current in amps.
        enabled (bool): True if the output of the PSU is enabled.
        tripped (bool): True if the PSU has tripped.
        mode (PSUMode): Operating mode of the tool.
    """

    voltage: float
    current: float
    enabled: bool
    tripped: bool
    mode: PSUMode


class Range(BaseModel):
    "An inclusive range."

    min: float
    max: float

    @root_validator
    def check_min_not_gt_max(cls, values: dict[str, float]) -> dict[str, float]:
        """Ensure that min <= max"""
        # pylint: disable=no-self-argument,no-self-use
        #   Disable pylint as it is unable to determine that root_validators are classmethods,
        #   see: https://github.com/samuelcolvin/pydantic/issues/568)
        _min, _max = values.get("min"), values.get("max")
        assert _min is not None and _max is not None

        assert not _min > _max
        return values

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Range):
            raise NotImplementedError()
        return isclose(self.min, other.min) and isclose(self.max, other.max)


class CurrentCapabilities(Range):
    "The current capabilities of a power supply, all fields reported in Amps"

    limit_resolution: float
    min: confloat(le=0)  # type: ignore # mypy considers these invalid type annotations
    max: confloat(ge=0)  # type: ignore # mypy considers these invalid type annotations


class VoltageCapabilities(Range):
    "The voltage capabilities of a power supply, all fields reported in Volts"

    setpoint_resolution: confloat(gt=0)  # type: ignore # mypy considers these invalid type annotations
    sense_resolution: confloat(gt=0)  # type: ignore # mypy considers these invalid type annotations

    @root_validator
    def check_min_not_gt_max(cls, values: dict[str, float]) -> dict[str, float]:
        """Ensure that min <= max"""
        # pylint: disable=no-self-argument,no-self-use
        #   Disable pylint as it is unable to determine that root_validators are classmethods,
        #   see: https://github.com/samuelcolvin/pydantic/issues/568)
        _min, _max = values.get("min"), values.get("max")
        assert _min is not None and _max is not None

        assert not _min > _max
        return values


class PSUSpec(BaseModel):
    "The specifications of a power supply"

    voltage: VoltageCapabilities
    current: CurrentCapabilities

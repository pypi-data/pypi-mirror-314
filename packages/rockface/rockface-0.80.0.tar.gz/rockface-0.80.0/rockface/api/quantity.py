from pydantic import BaseModel

from .tool_request import ToolRequest


class Quantity(BaseModel):
    """
    A physical quantity

    The magnitude is considered to be in SI units (e.g Amps, Volts, Watts) so 1mV
    will be represented with a magnitude of 0.001
    """

    magnitude: float


class QuantityRequest(Quantity, ToolRequest):
    """Model for sending a quantity request to the server"""

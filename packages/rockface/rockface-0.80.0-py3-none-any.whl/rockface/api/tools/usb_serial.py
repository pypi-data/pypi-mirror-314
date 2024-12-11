from pydantic import BaseModel, StrictStr


class WriteParams(BaseModel):
    "The parameters of a write request to a USB Serial tool"

    tool_id: StrictStr
    data: StrictStr


class ReadParams(BaseModel):
    "The parameters of a read request to a USB Serial tool"

    tool_id: StrictStr
    count: int


class WriteResponse(BaseModel):
    """The response to a write request to a USB Serial tool"""

    count: int | None = None

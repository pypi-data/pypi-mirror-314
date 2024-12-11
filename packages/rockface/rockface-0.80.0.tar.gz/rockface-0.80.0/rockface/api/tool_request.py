from pydantic import BaseModel, StrictStr


class ToolRequest(BaseModel):
    """Request to use or inherit from when making a tool-specific request"""

    tool_id: StrictStr

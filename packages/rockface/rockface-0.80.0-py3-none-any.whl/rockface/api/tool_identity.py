from pydantic import BaseModel, StrictStr


class ToolIdentity(BaseModel):
    "The unique identity of a tool"

    tool_id: StrictStr

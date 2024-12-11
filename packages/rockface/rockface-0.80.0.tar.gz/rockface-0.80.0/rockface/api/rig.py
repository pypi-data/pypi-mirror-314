from pydantic import BaseModel


class ToolIdentity(BaseModel):
    "Identity of a tool"

    kind: str
    id: str

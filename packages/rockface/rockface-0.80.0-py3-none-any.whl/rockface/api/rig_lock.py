from datetime import datetime

from pydantic import BaseModel


class RigLockToken(BaseModel):
    "A token representing holding the lock on a rig"

    token: str


class RigLockHolder(BaseModel):
    "Information about a rig lock holder"

    name: str
    time_of_acquisition: datetime

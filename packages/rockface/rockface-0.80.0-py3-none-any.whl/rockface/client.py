import os
from dataclasses import dataclass, field, replace
from typing import Any

import requests

from .rpc import RPCClient


class UnauthorizedError(Exception):
    "Invalid API key"


def api_key_from_env() -> str:
    "Load the API key from the environment"
    key = os.getenv("ROCKFACE_API_KEY")
    if key is None:
        raise RuntimeError(
            "Rockface API key not found.  Set the ROCKFACE_API_KEY environment variable."
        )
    return key


def base_url_from_env() -> str:
    "Load the API base URL from the environment"
    return os.getenv("ROCKFACE_API_BASE_URL", default="https://api.rockface.io")


@dataclass
class APIParams:
    "Location and authentication information for the Rockface API"

    api_key: str = field(repr=False, default_factory=api_key_from_env)
    api_base_url: str = field(default_factory=base_url_from_env)


@dataclass(frozen=True)
class RigInfo:
    """Information about a Rig

         id: The ID number of the rig
       name: The human-readable name of the rig
    address: The address of the rig's API
    """

    id: int
    name: str
    address: APIParams

    @classmethod
    def from_dict(cls, src: dict[str, Any], address: APIParams) -> "RigInfo":
        "Build the RigInfo from a JSON-derived dict"

        return cls(id=src["id"], name=src["name"], address=address)

    def build_rpc(self) -> RPCClient:
        "Build an RPCClient for interacting with this rig"
        return RPCClient(
            base_url=self.address.api_base_url, api_key=self.address.api_key
        )


@dataclass
class RockfaceClient:
    "A client for accessing the Rockface API"

    params: APIParams

    @property
    def rigs(self) -> list[RigInfo]:
        "List of the available rigs"

        resp = requests.get(
            f"{self.params.api_base_url}/rigs",
            headers={"rockface-api-token": self.params.api_key},
        )

        if resp.status_code == requests.codes.unauthorized:
            raise UnauthorizedError()

        resp.raise_for_status()

        result = []
        for rig in resp.json():
            address = replace(
                self.params, api_base_url=f"{self.params.api_base_url}/rigs/{rig['id']}"
            )

            result.append(RigInfo.from_dict(rig, address))

        return result

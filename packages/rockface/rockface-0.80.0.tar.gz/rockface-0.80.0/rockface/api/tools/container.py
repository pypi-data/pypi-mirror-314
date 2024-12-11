from pydantic import BaseModel, StrictBool, StrictInt, StrictStr, root_validator


class RunRequest(BaseModel):
    "The parameters of a 'run' request to a Container tool"

    tool_id: StrictStr
    container: StrictStr
    command: list[StrictStr]
    username: StrictStr | None
    password: StrictStr | None

    @root_validator
    def check_both_credentials_or_neither(
        cls, values: dict[str, float]
    ) -> dict[str, float]:
        """Ensure that either both username and password or set, or neither are set"""
        # pylint: disable=no-self-argument,no-self-use
        #   Disable pylint as it is unable to determine that root_validators are classmethods,
        #   see: https://github.com/samuelcolvin/pydantic/issues/568)
        username, password = values.get("username"), values.get("password")
        assert (username is None and password is None) or (
            username is not None and password is not None
        )
        return values


class SignalRequest(BaseModel):
    """The parameters of a 'signal' request to a Container tool"""

    tool_id: StrictStr
    signal: StrictStr


class GetStdoutResponse(BaseModel):
    """The response of a 'get_stdout' request to a Container tool"""

    stdout: StrictStr


class GetStateResponse(BaseModel):
    """The response of a 'get_state' request to a Container tool"""

    running: StrictBool
    return_code: StrictInt | None = None


class GetStderrResponse(BaseModel):
    """The response of a 'get_stderr request to a Container tool"""

    stderr: StrictStr

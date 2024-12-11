import os
from enum import Enum


class FeatureFlags(str, Enum):
    NEW_LOCK = "Sets whether the client library should use the new locking API"


def _set_in_env(flag: FeatureFlags) -> bool:
    var = os.getenv(f"ROCKFACE_FEATURE_{flag.name}")
    return var is not None and bool(int(var))


_enabled_flags = {flag for flag in FeatureFlags if _set_in_env(flag)}


def flag_enabled(flag: FeatureFlags) -> bool:
    """Whether the provided feature flag is enabled"""
    return flag in _enabled_flags

from enum import Enum


class LpnrDirectionEnum(str, Enum):
    IN = "in"
    OUT = "out"
    UNKNOWN = "unknown"

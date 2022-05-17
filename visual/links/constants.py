from enum import Enum, auto


class LinkType(Enum):
    UNITED = auto()
    SEPARATED = auto()


class WeightType(Enum):
    KERNEL = auto()
    BIAS = auto()

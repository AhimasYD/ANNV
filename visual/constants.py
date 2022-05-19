from enum import Enum, auto


class Display(Enum):
    COMPACT = auto()
    EXTENDED = auto()


class WeightColor(Enum):
    OFF = auto()
    ON = auto()


class WeightThick(Enum):
    OFF = auto()
    ON = auto()


class Names(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class Captions(Enum):
    OFF = auto()
    ON = auto()


class Bias(Enum):
    OFF = auto()
    ON = auto()


class Activation(Enum):
    OFF = auto()
    ON = auto()


SCENE_RECT_PADDING = 25

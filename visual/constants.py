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


class LinkType(Enum):
    UNITED = auto()
    SEPARATED = auto()


LAYER_MARGIN = 300


BLOCK_HEIGHT = 900
BLOCK_WIDTH = 300

NEURON_SIDE = 100
NEURON_MARGIN = 10

NEURON_REC_HEIGHT = 200
NEURON_REC_WIDTH = 100
NEURON_REC_MARGIN = 100

KERNEL_MARGIN = 80


PLACEHOLDER_SIDE = 50
PLACEHOLDER_MARGIN_IN = 30
PLACEHOLDER_MARGIN_OUT = 40
PLACEHOLDER_MAX_NEURONS = 3
PLACEHOLDER_MAX_KERNELS = 3


PIXMAP_SIDE = 50


CAPTION_MARGIN = 50

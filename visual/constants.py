from enum import Enum, auto


class Display(Enum):
    COMPACT = auto()
    EXTENDED = auto()


class Names(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


LAYER_MARGIN = 300

BLOCK_HEIGHT = 600
BLOCK_WIDTH = 200

NEURON_HEIGHT = 100
NEURON_WIDTH = NEURON_HEIGHT
NEURON_MARGIN = 10

PIXMAP_SIDE = 10

CELL_TABLE_SIZE = 50

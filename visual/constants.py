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

NEURON_SIDE = 100
NEURON_MARGIN = 10

NEURON_REC_HEIGHT = 200
NEURON_REC_WIDTH = 100
NEURON_REC_MARGIN = 100

KERNEL_MARGIN = 20

PIXMAP_SIDE = 10

CELL_TABLE_SIZE = 50

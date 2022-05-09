from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic.layers import *

from .constants import *
from .functions import *
from .layer import VLayer
from .pixmap import Pixmap


class VDense(VLayer):
    def __init__(self, logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias, widget):
        super().__init__(logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias, widget)

        if self.opt_display == Display.COMPACT:
            self.block = VDenseBlock(self.scene, self.pos_x, self.select)
        elif self.opt_display == Display.EXTENDED:
            self.neurons = []
            units = self.logic.units
            total_height = units * NEURON_HEIGHT + (units - 1) * NEURON_MARGIN
            y = -total_height/2 + NEURON_HEIGHT/2
            for i in range(units):
                unit = VDenseNeuron(self.scene, self.pos_x, y, self.select)
                self.neurons.append(unit)
                y += NEURON_HEIGHT + NEURON_MARGIN

    def select(self, event):
        layout = self.widget.layout()
        clear_layout(layout)

        layout.addWidget(QLabel('Type: ' + self.logic.type))
        layout.addWidget(QLabel('Activation: ' + self.logic.activation))

        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('Kernel:'))
        layout.addWidget(Pixmap(self.logic.kernel, CELL_TABLE_SIZE, hv=False, hh=False, sb=False))

        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('Bias:'))
        layout.addWidget(Pixmap(self.logic.bias, CELL_TABLE_SIZE, hv=False, hh=False, sb=False))

        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))


class VDenseBlock:
    def __init__(self, scene, x, callback):
        self.scene = scene

        self.rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.bound = self.rect.boundingRect()
        self.text = draw_text('Dense', self.bound)

        self.scene.addItem(self.rect)
        self.scene.addItem(self.text)

        self.rect.mousePressEvent = callback


class VDenseNeuron:
    def __init__(self, scene, x, y, callback):
        self.scene = scene

        self.ellipse = draw_ellipse(x, y, NEURON_HEIGHT, NEURON_WIDTH)
        self.scene.addItem(self.ellipse)

        self.ellipse.mousePressEvent = callback

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer


class VDense(VLayer):
    def __init__(self, logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions,
                 opt_bias, widget, flat, volume):
        super().__init__(logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions,
                         opt_bias, widget, flat, volume)

        if self.opt_display == Display.COMPACT:
            self.block = VDenseBlock(self.scene, self.pos_x, self.select, self.opt_names)
        elif self.opt_display == Display.EXTENDED:
            units = self.logic.units
            self.neurons = np.empty(units, dtype=VDenseNeuron)

            total_height = units * NEURON_SIDE + (units - 1) * NEURON_MARGIN
            y = -total_height/2 + NEURON_SIDE/2
            for i in range(units):
                self.neurons[i] = VDenseNeuron(self.scene, self.pos_x, y, self.select)
                y += NEURON_SIDE + NEURON_MARGIN

    def select(self, event):
        super().select(event)

        layout = self.widget.layout()
        clear_layout(layout)

        layout.addWidget(QLabel(f'Type: {self.logic.type}'))
        layout.addWidget(QLabel(f'Activation: {self.logic.activation}'))

        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('Kernel:'))
        layout.addWidget(Pixmap(self.logic.kernel, CELL_TABLE_SIZE, hv=True, hh=True, sb=True))

        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('Bias:'))
        layout.addWidget(Pixmap(self.logic.bias, CELL_TABLE_SIZE, hv=True, hh=True, sb=True))

        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))


class VDenseBlock:
    def __init__(self, scene, x, callback, opt_names):
        self.scene = scene

        self.rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.bound = self.rect.boundingRect()
        self.text = draw_text('Dense', self.bound, opt_names)

        self.scene.addItem(self.rect)
        self.scene.addItem(self.text)

        self.rect.mousePressEvent = callback


class VDenseNeuron:
    def __init__(self, scene, x, y, callback):
        self.scene = scene

        self.ellipse = draw_ellipse(x, y, NEURON_SIDE, NEURON_SIDE)
        self.scene.addItem(self.ellipse)

        self.ellipse.mousePressEvent = callback

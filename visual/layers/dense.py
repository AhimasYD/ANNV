from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer
from .placeholder import VPlaceholder


class VDense(VLayer):
    def __init__(self, logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions,
                 opt_bias, widget, flat, volume):
        super().__init__(logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions,
                         opt_bias, widget, flat, volume)

        # Display as block
        if self.opt_display == Display.COMPACT:
            self.block = VDenseBlock(self.scene, BLOCK_WIDTH, BLOCK_HEIGHT, self.pos_x, self.select, self.opt_names)
        # Display as neurons
        elif self.opt_display == Display.EXTENDED:
            units = self.logic.units
            self.neurons = np.empty(units, dtype=VDenseNeuron)

            # No placeholder needed
            if units <= PLACEHOLDER_MAX_NEURONS * 2:
                total_height = units * NEURON_SIDE + (units - 1) * NEURON_MARGIN
                y = -total_height/2 + NEURON_SIDE/2
                for i in range(units):
                    self.neurons[i] = VDenseNeuron(self.scene, NEURON_SIDE, self.pos_x, y, self.select)
                    y += NEURON_SIDE + NEURON_MARGIN
            # Placeholder needed
            else:
                placeholder = VPlaceholder(PLACEHOLDER_SIDE, PLACEHOLDER_MARGIN_IN, pos_x, 0)
                self.scene.addItem(placeholder)

                total_height = 2 * PLACEHOLDER_MAX_NEURONS * NEURON_SIDE + 2 * PLACEHOLDER_MAX_NEURONS * NEURON_MARGIN
                total_height += placeholder.boundingRect().height() + 2 * PLACEHOLDER_MARGIN_OUT

                y = -total_height / 2 + NEURON_SIDE / 2
                for i in range(units):
                    if i < PLACEHOLDER_MAX_NEURONS:
                        self.neurons[i] = VDenseNeuron(self.scene, NEURON_SIDE, self.pos_x, y, self.select)
                        y += NEURON_SIDE + NEURON_MARGIN
                    elif i == PLACEHOLDER_MAX_NEURONS:
                        y += placeholder.boundingRect().height()
                        y += 2 * PLACEHOLDER_MARGIN_OUT
                        y += NEURON_MARGIN
                    elif i >= units - PLACEHOLDER_MAX_NEURONS:
                        self.neurons[i] = VDenseNeuron(self.scene, NEURON_SIDE, self.pos_x, y, self.select)
                        y += NEURON_SIDE + NEURON_MARGIN

    def select(self, event):
        super().select(event)

        layout = self.widget.layout()
        clear_layout(layout)

        layout.addWidget(QLabel(f'Type: {self.logic.type}'))
        layout.addWidget(QLabel(f'Activation: {self.logic.activation}'))

        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('Kernel:'))
        layout.addWidget(Pixmap(self.logic.kernel, PIXMAP_SIDE, hv=True, hh=True, sb=True))

        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('Bias:'))
        layout.addWidget(Pixmap(self.logic.bias, PIXMAP_SIDE, hv=True, hh=True, sb=True))

        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))


class VDenseBlock:
    def __init__(self, scene, width, height, x, callback, opt_names):
        self.scene = scene

        self.rect = draw_rect(x, 0, width, height)
        self.bound = self.rect.boundingRect()
        self.text = draw_text('Dense', self.bound, opt_names)

        self.scene.addItem(self.rect)
        self.scene.addItem(self.text)

        self.rect.mousePressEvent = callback


class VDenseNeuron:
    def __init__(self, scene, side, x, y, callback):
        self.scene = scene

        self.ellipse = draw_ellipse(x, y, side, side)
        self.scene.addItem(self.ellipse)

        self.ellipse.mousePressEvent = callback

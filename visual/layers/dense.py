from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer
from .placeholder import VPlaceholder


class VDense(VLayer):
    def __init__(self, logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume)

        # Display as _block
        if self._o_display == Display.COMPACT:
            self._connection = LinkType.UNITED
            self._block = VDenseBlock(self._scene, self._x, self.select, self._o_names)

        # Display as neurons
        elif self._o_display == Display.EXTENDED:
            self._connection = LinkType.SEPARATED
            self._neuron_ctrl = VDenseNeuronController(self._scene, self._x, self._logic.units, self.select)

    def select(self, event):
        super().select(event)

        layout = self._w_info.layout()
        layout.addWidget(QLabel(f'Type: {self._logic.type}'))
        layout.addWidget(QLabel(f'Activation: {self._logic.activation}'))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('Kernel:'))
        layout.addWidget(Pixmap(self._logic.kernel, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('Bias:'))
        layout.addWidget(Pixmap(self._logic.bias, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def binds_in(self):
        if self._connection == LinkType.UNITED:
            return self._connection, self._block.bind_in()
        else:
            return self._connection, self._neuron_ctrl.binds_in()

    def binds_out(self):
        if self._connection == LinkType.UNITED:
            return self._connection, self._block.bind_out()
        else:
            return self._connection, self._neuron_ctrl.binds_out()


class VDenseBlock:
    def __init__(self, scene, x, callback, opt_names):
        self._scene = scene

        self._rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self._rect.mousePressEvent = callback
        self._text = draw_text('Dense', self._rect.boundingRect(), opt_names)
        self._scene.addItem(self._rect)
        self._scene.addItem(self._text)

        self._bind_in = QPointF(x - BLOCK_WIDTH / 2, 0)
        self._bind_out = QPointF(x + BLOCK_WIDTH / 2, 0)

    def bind_in(self):
        return self._bind_in

    def bind_out(self):
        return self._bind_out


class VDenseNeuronController:
    def __init__(self, scene, x, units, select):
        self._scene = scene
        self._x = x
        self._units = units

        self._neurons = None

        self._placeholder = None
        self._neurons_start = None
        self._neurons_end = None

        # No placeholder needed
        if units <= PLACEHOLDER_MAX_NEURONS * 2:
            self._neurons = np.empty(units, dtype=VDenseNeuron)

            total_height = units * NEURON_SIDE + (units - 1) * NEURON_MARGIN
            y = -total_height/2 + NEURON_SIDE/2
            for i in range(units):
                self._neurons[i] = VDenseNeuron(self._scene, NEURON_SIDE, self._x, y, select)
                y += NEURON_SIDE + NEURON_MARGIN

        # Placeholder needed
        else:
            self._placeholder = VPlaceholder(PLACEHOLDER_SIDE, PLACEHOLDER_MARGIN_IN, x, 0)
            self._placeholder.mousePressEvent = select
            self._scene.addItem(self._placeholder)

            self._neurons_start = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=VDenseNeuron)
            self._neurons_end = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=VDenseNeuron)

            total_height = 2 * PLACEHOLDER_MAX_NEURONS * NEURON_SIDE + 2 * PLACEHOLDER_MAX_NEURONS * NEURON_MARGIN
            total_height += self._placeholder.boundingRect().height() + 2 * PLACEHOLDER_MARGIN_OUT

            y = -total_height / 2 + NEURON_SIDE / 2
            for i in range(units):
                if i < PLACEHOLDER_MAX_NEURONS:
                    j = i
                    self._neurons_start[j] = VDenseNeuron(self._scene, NEURON_SIDE, self._x, y, select)
                    y += NEURON_SIDE + NEURON_MARGIN
                elif i >= units - PLACEHOLDER_MAX_NEURONS:
                    j = i - (units - PLACEHOLDER_MAX_NEURONS)
                    self._neurons_end[j] = VDenseNeuron(self._scene, NEURON_SIDE, self._x, y, select)
                    y += NEURON_SIDE + NEURON_MARGIN

                if i == PLACEHOLDER_MAX_NEURONS:
                    y += self._placeholder.boundingRect().height()
                    y += 2 * PLACEHOLDER_MARGIN_OUT
                    y += NEURON_MARGIN

    def binds_in(self):
        if self._placeholder is None:
            binds = np.empty(self._units, dtype=QPointF)
            for i in range(self._units):
                binds[i] = self._neurons[i].bind_in()

        else:
            placeholder = np.full(shape=(self._units - 2 * PLACEHOLDER_MAX_NEURONS), fill_value=None, dtype=QPointF)

            binds_start = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=QPointF)
            for i in range(PLACEHOLDER_MAX_NEURONS):
                binds_start[i] = self._neurons_start[i].bind_in()

            binds_end = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=QPointF)
            for i in range(PLACEHOLDER_MAX_NEURONS):
                binds_end[i] = self._neurons_end[i].bind_in()

            binds = np.concatenate((binds_start, placeholder, binds_end))

        return binds

    def binds_out(self):
        if self._placeholder is None:
            binds = np.empty(self._units, dtype=QPointF)
            for i in range(self._units):
                binds[i] = self._neurons[i].bind_out()

        else:
            placeholder = np.full(shape=(self._units - 2 * PLACEHOLDER_MAX_NEURONS), fill_value=None, dtype=QPointF)

            binds_start = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=QPointF)
            for i in range(PLACEHOLDER_MAX_NEURONS):
                binds_start[i] = self._neurons_start[i].bind_out()

            binds_end = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=QPointF)
            for i in range(PLACEHOLDER_MAX_NEURONS):
                binds_end[i] = self._neurons_end[i].bind_out()

            binds = np.concatenate((binds_start, placeholder, binds_end))

        return binds


class VDenseNeuron:
    def __init__(self, scene, side, x, y, select):
        self._scene = scene

        self._ellipse = draw_ellipse(x, y, side, side)
        self._ellipse.mousePressEvent = select
        self._scene.addItem(self._ellipse)

        self._bind_in = QPointF(x - side/2, y)
        self._bind_out = QPointF(x + side / 2, y)

    def bind_in(self):
        return self._bind_in

    def bind_out(self):
        return self._bind_out

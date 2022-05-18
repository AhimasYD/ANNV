from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from visual.constants import *
from visual.functions import draw_text, brush_by_factor
from visual.pixmap import Pixmap
from visual.hintskeeper import HintsKeeper

from visual.links import VLink, LinkType, WeightType

from visual.layers.layer import VLayer
from visual.layers.block import VBlock
from visual.layers.placeholder import VPlaceholder
from visual.layers.outputwindow import OutputWindow
from visual.layers.bias import VBiasNeuron

from visual.layers.item.neuron import VNeuron


class VLSTM(VLayer):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, w_info, w_flat, w_volume)

        if HintsKeeper().display == Display.COMPACT:
            self._connection = LinkType.UNITED
            self._block = VLSTMBlock(self._scene, self._x, self.select, self.show_output)

        elif HintsKeeper().display == Display.EXTENDED:
            self._connection = LinkType.SEPARATED
            self._neuron_ctrl = VLSTMNeuronController(self._scene, self._x, self._logic.units, self.select, self.show_output, logic)

        self._init_caption()

    def select(self, event):
        super().select(event)

        layout = self._w_info.layout()

        layout.addWidget(QLabel(f'Type: {self._logic.type}'))
        layout.addWidget(QLabel(f'Activation: {self._logic.activation}'))
        layout.addItem(QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('W_i:'))
        layout.addWidget(Pixmap(self._logic.W_i, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('W_f:'))
        layout.addWidget(Pixmap(self._logic.W_f, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('W_c:'))
        layout.addWidget(Pixmap(self._logic.W_c, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('W_o:'))
        layout.addWidget(Pixmap(self._logic.W_o, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('U_i:'))
        layout.addWidget(Pixmap(self._logic.U_i, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('U_f:'))
        layout.addWidget(Pixmap(self._logic.U_f, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('U_c:'))
        layout.addWidget(Pixmap(self._logic.U_c, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('U_o:'))
        layout.addWidget(Pixmap(self._logic.U_o, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('b_i:'))
        layout.addWidget(Pixmap(self._logic.b_i, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('b_f:'))
        layout.addWidget(Pixmap(self._logic.b_f, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('b_c:'))
        layout.addWidget(Pixmap(self._logic.b_c, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('b_o:'))
        layout.addWidget(Pixmap(self._logic.b_o, PIXMAP_SIDE, hv=True, hh=True, sb=True))

        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def binds_in(self):
        if HintsKeeper().display == Display.COMPACT:
            return self._connection, self._block.bind_in()
        else:
            return self._connection, self._neuron_ctrl.binds_in()

    def binds_out(self):
        if HintsKeeper().display == Display.COMPACT:
            return self._connection, self._block.bind_out()
        else:
            return self._connection, self._neuron_ctrl.binds_out()

    def set_links_in(self, links):
        if HintsKeeper().display == Display.COMPACT:
            self._block.set_links_in(links)
        else:
            self._neuron_ctrl.set_links_in(links)

    def set_links_out(self, links):
        if HintsKeeper().display == Display.COMPACT:
            self._block.set_links_out(links)
        else:
            self._neuron_ctrl.set_links_out(links)

    def show_output(self, event):
        if self._logic.output is None:
            return
        self._window = OutputWindow(self._logic.output)
        self._window.setModal(True)
        self._window.showMaximized()

    def bounding(self):
        if HintsKeeper().display == Display.COMPACT:
            return self._block.bounding()
        else:
            return self._neuron_ctrl.bounding()

    def set_bias(self, bounding):
        if HintsKeeper().display == Display.COMPACT:
            pass
        else:
            self._neuron_ctrl.set_bias(bounding, (self._logic.b_i, self._logic.b_f, self._logic.b_c, self._logic.b_o))


class VLSTMBlock(VBlock):
    def __init__(self, scene, x, select, show_output):
        super().__init__(scene, x, select, show_output, 'LSTM')


class VLSTMNeuronController:
    def __init__(self, scene, x, units, select, show_output, logic):
        self._scene = scene
        self._x = x
        self._units = units

        self._neurons = None

        self._placeholder = None
        self._neurons_start = None
        self._neurons_end = None

        # No placeholder needed
        if units <= PLACEHOLDER_MAX_NEURONS * 2:
            self._neurons = np.empty(units, dtype=VLSTMNeuron)

            total_height = units * NEURON_REC_HEIGHT + (units - 1) * NEURON_REC_MARGIN
            y = -total_height/2
            for i in range(units):
                self._neurons[i] = VLSTMNeuron(self._scene, self._x, y, select, show_output)
                y += NEURON_REC_HEIGHT + NEURON_REC_MARGIN

        # Placeholder needed
        else:
            self._placeholder = VPlaceholder(PLACEHOLDER_SIDE, PLACEHOLDER_MARGIN_IN, x, 0)
            self._placeholder.mousePressEvent = select
            self._scene.addItem(self._placeholder)

            self._neurons_start = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=VLSTMNeuron)
            self._neurons_end = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=VLSTMNeuron)

            total_height = 2 * PLACEHOLDER_MAX_NEURONS * NEURON_REC_HEIGHT + 2 * PLACEHOLDER_MAX_NEURONS * NEURON_REC_MARGIN
            total_height += self._placeholder.boundingRect().height() + 2 * PLACEHOLDER_MARGIN_OUT

            y = -total_height / 2
            for i in range(units):
                if i < PLACEHOLDER_MAX_NEURONS:
                    j = i
                    self._neurons_start[j] = VLSTMNeuron(self._scene, self._x, y, select, show_output)
                    y += NEURON_REC_HEIGHT + NEURON_REC_MARGIN
                elif i >= units - PLACEHOLDER_MAX_NEURONS:
                    j = i - (units - PLACEHOLDER_MAX_NEURONS)
                    self._neurons_end[j] = VLSTMNeuron(self._scene, self._x, y, select, show_output)
                    y += NEURON_REC_HEIGHT + NEURON_REC_MARGIN

                if i == PLACEHOLDER_MAX_NEURONS:
                    y += self._placeholder.boundingRect().height()
                    y += 2 * PLACEHOLDER_MARGIN_OUT
                    y += NEURON_REC_MARGIN

            self._placeholder.setPos(self._x + NEURON_REC_WIDTH / 2 - self._placeholder.boundingRect().width() / 2,
                                     0 - self._placeholder.boundingRect().height() / 2)

        logic.attach_output(self.update_output)

    def _get_neuron(self, i):
        if self._neurons is not None:
            return self._neurons[i]
        else:
            if i < PLACEHOLDER_MAX_NEURONS:
                return self._neurons_start[i]
            elif i >= self._units - PLACEHOLDER_MAX_NEURONS:
                return self._neurons_end[i - (self._units - PLACEHOLDER_MAX_NEURONS)]
            else:
                return None

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

    def set_links_in(self, links):
        for i in range(self._units):
            neuron = self._get_neuron(i)
            if neuron is not None:
                neuron.set_links_in(links[i])

    def set_links_out(self, links):
        for i in range(self._units):
            neuron = self._get_neuron(i)
            if neuron is not None:
                neuron.set_links_out(links[i])

    def update_output(self, output):
        maximum = max(output.min(), output.max(), key=abs)
        for i in range(self._units):
            neuron = self._get_neuron(i)
            if neuron is not None:
                if maximum is not None:
                    neuron.set_output(output[i], output[i] / maximum)
                else:
                    neuron.set_output(output[i], 0.0)

    def bounding(self):
        unit_0 = self._get_neuron(0)
        unit_1 = self._get_neuron(self._units - 1)
        return unit_0.bounding().united(unit_1.bounding())

    def set_bias(self, bounding, weights):
        b_i, b_f, b_c, b_o = weights

        bias = VBiasNeuron(self._scene, bounding)
        bind_out = bias.bind_out()
        binds_in = self.binds_in()

        links = np.full(len(binds_in), None, dtype=VLayer)
        for i in range(len(binds_in)):
            bind_in = binds_in[i]
            if bind_in is not None:
                tooltip = f'i:{b_i[i]}\nf:{b_f[i]}\nc:{b_c[i]}\no:{b_o[i]}'

                links[i] = VLink(bind_out, bind_in, WeightType.BIAS)
                links[i].set_tooltip(tooltip)
                self._get_neuron(i).set_link_bias(links[i])

                self._scene.addItem(links[i].get_item())
        bias.set_links_out(links)


class VLSTMNeuron(VNeuron):
    def __init__(self, scene, x, y, select, show_output):
        super().__init__(scene)

        width = NEURON_REC_WIDTH
        height = NEURON_REC_HEIGHT

        self._item = QGraphicsRectItem(x, y, width, height)
        self._item.setZValue(10)
        self._item.mousePressEvent = select
        self._item.mouseDoubleClickEvent = show_output
        self._text = draw_text('LSTM', self._item.boundingRect(), HintsKeeper().names)
        self._text.setZValue(11)
        self._scene.addItem(self._item)
        self._scene.addItem(self._text)

        self._bind_in = QPointF(x, y + height / 2)
        self._bind_out = QPointF(x + width, y + height / 2)

    def set_output(self, value, factor):
        super().set_output(value, factor)
        self._item.setToolTip(str(value))

    def set_links_in(self, links, weights=None):
        super().set_links_in(links)
        if type(self._links_in) is np.ndarray and weights is not None:
            array, maximum = weights
            for i in range(self._links_in.shape[0]):
                if self._links_in[i] is not None:
                    self._links_in[i].set_weight(array[i], maximum)
                    self._links_in[i].set_tooltip(str(array[i]))

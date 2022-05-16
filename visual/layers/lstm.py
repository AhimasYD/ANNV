from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer
from .placeholder import VPlaceholder
from visual.links import VLink
from visual.layers.block import VBlock

from visual.hintskeeper import HintsKeeper


class VLSTM(VLayer):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, w_info, w_flat, w_volume)

        if HintsKeeper().display == Display.COMPACT:
            self._connection = LinkType.UNITED
            self._block = VLSTMBlock(self._scene, self._x, self.select)

        elif HintsKeeper().display == Display.EXTENDED:
            self._connection = LinkType.SEPARATED
            self._neuron_ctrl = VLSTMNeuronController(self._scene, self._x, self._logic.units, self.select, Names.HORIZONTAL)

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


class VLSTMBlock(VBlock):
    def __init__(self, scene, x, select):
        super().__init__(scene, x, select, 'LSTM')


class VLSTMNeuronController:
    def __init__(self, scene, x, units, select, o_names):
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
                self._neurons[i] = VLSTMNeuron(self._scene, self._x, y, select, o_names)
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
                    self._neurons_start[j] = VLSTMNeuron(self._scene, self._x, y, select, o_names)
                    y += NEURON_REC_HEIGHT + NEURON_REC_MARGIN
                elif i >= units - PLACEHOLDER_MAX_NEURONS:
                    j = i - (units - PLACEHOLDER_MAX_NEURONS)
                    self._neurons_end[j] = VLSTMNeuron(self._scene, self._x, y, select, o_names)
                    y += NEURON_REC_HEIGHT + NEURON_REC_MARGIN

                if i == PLACEHOLDER_MAX_NEURONS:
                    y += self._placeholder.boundingRect().height()
                    y += 2 * PLACEHOLDER_MARGIN_OUT
                    y += NEURON_REC_MARGIN

            self._placeholder.setPos(self._x + NEURON_REC_WIDTH / 2 - self._placeholder.boundingRect().width() / 2,
                                     0 - self._placeholder.boundingRect().height() / 2)

        self._init_rec_weights()

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

    def _init_rec_weights(self):
        if self._neurons is not None:
            for i in range(self._neurons.shape[0] - 1):
                neuron_0 = self._neurons[i]
                neuron_1 = self._neurons[i + 1]

                bind_out = neuron_0.bind_rec_out()
                bind_in = neuron_1.bind_rec_in()

                link = VLink(bind_out, bind_in)
                self._scene.addItem(link.get_item())

                neuron_0.set_rec_links_out(link)
                neuron_1.set_rec_links_in(link)

        else:
            for i in range(self._neurons_start.shape[0] - 1):
                neuron_0 = self._neurons_start[i]
                neuron_1 = self._neurons_start[i + 1]

                bind_out = neuron_0.bind_rec_out()
                bind_in = neuron_1.bind_rec_in()

                link = VLink(bind_out, bind_in)
                self._scene.addItem(link.get_item())

                neuron_0.set_rec_links_out(link)
                neuron_1.set_rec_links_in(link)

            for i in range(self._neurons_end.shape[0] - 1):
                neuron_0 = self._neurons_end[i]
                neuron_1 = self._neurons_end[i + 1]

                bind_out = neuron_0.bind_rec_out()
                bind_in = neuron_1.bind_rec_in()

                link = VLink(bind_out, bind_in)
                self._scene.addItem(link.get_item())

                neuron_0.set_rec_links_out(link)
                neuron_1.set_rec_links_in(link)

            neuron = self._neurons_start[self._neurons_start.shape[0] - 1]
            bind_out = neuron.bind_rec_out()
            bind_in = QPointF(bind_out.x(), bind_out.y() + NEURON_REC_MARGIN)
            link = VLink(bind_out, bind_in)
            self._scene.addItem(link.get_item())
            neuron.set_rec_links_out(link)

            neuron = self._neurons_end[0]
            bind_in = neuron.bind_rec_in()
            bind_out = QPointF(bind_in.x(), bind_in.y() - NEURON_REC_MARGIN)
            link = VLink(bind_out, bind_in)
            self._scene.addItem(link.get_item())
            neuron.set_rec_links_in(link)

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


class VLSTMNeuron:
    def __init__(self, scene, x, y, select, o_names):
        self._scene = scene

        width = NEURON_REC_WIDTH
        height = NEURON_REC_HEIGHT

        self._rect = QGraphicsRectItem(x, y, width, height)
        self._rect.setZValue(10)
        self._rect.mousePressEvent = select
        self._text = draw_text('LSTM', self._rect.boundingRect(), o_names)
        self._text.setZValue(11)
        self._scene.addItem(self._rect)
        self._scene.addItem(self._text)

        self._bind_in = QPointF(x, y + height / 2)
        self._bind_out = QPointF(x + width, y + height / 2)

        self._links_in = None
        self._links_out = None

        self._bind_rec_in = QPointF(x + width / 2, y)
        self._bind_rec_out = QPointF(x + width / 2, y + height)

        self._link_rec_in = None
        self._link_rec_out = None

    def bind_in(self):
        return self._bind_in

    def bind_out(self):
        return self._bind_out

    def bind_rec_in(self):
        return self._bind_rec_in

    def bind_rec_out(self):
        return self._bind_rec_out

    def set_links_in(self, links, weights=None):
        self._links_in = links

    def set_links_out(self, links):
        self._links_out = links

    def set_rec_links_in(self, link):
        self._link_rec_in = link

    def set_rec_links_out(self, link):
        self._link_rec_out = link

from PyQt5.QtWidgets import QLabel, QSpacerItem, QSizePolicy, QGraphicsRectItem
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QBrush

import numpy as np

from weak import WeakMethod
from visual.constants import Display
from visual.trivia import Pixmap, HintsKeeper, PIXMAP_SIDE
from visual.links import VLink, LinkType, WeightType
from visual.layers.constants import NEURON_REC_HEIGHT, NEURON_REC_WIDTH, NEURON_REC_MARGIN
from visual.layers.functions import draw_text
from visual.layers.layer import VLayer
from visual.layers.trivia import VBlock, VBiasNeuron
from visual.layers.item.itemlayer import VItem
from visual.layers.item.neuroncontroller import VNeuronController
from visual.layers.item.neuron import VNeuron


class VGRU(VItem):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, w_info, w_flat, w_volume)

        self._select_callback = WeakMethod(self, VGRU.select)
        self._output_callback = WeakMethod(self, VGRU.show_output)
        if HintsKeeper().display == Display.COMPACT:
            self._connection = LinkType.UNITED
            self._block = VGRUBlock(self._scene, self._x, self._select_callback, self._output_callback)

        elif HintsKeeper().display == Display.EXTENDED:
            self._connection = LinkType.SEPARATED
            self._neuron_ctrl = VGRUNeuronController(self._scene, self._x, self._logic.units, self._select_callback, self._output_callback, logic)

        self._init_caption()

    def __del__(self):
        super().__del__()

    def select(self, event):
        super().select(event)

        layout = self._w_info.layout()

        layout.addWidget(QLabel(f'Type: {self._logic.type}'))
        layout.addWidget(QLabel(f'Activation: {self._logic.activation}'))
        layout.addWidget(QLabel(f'Recurrent activation: {self._logic.rec_activation}'))
        layout.addItem(QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('W_z:'))
        layout.addWidget(Pixmap(self._logic.W_z, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('W_r:'))
        layout.addWidget(Pixmap(self._logic.W_r, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('W_h:'))
        layout.addWidget(Pixmap(self._logic.W_h, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('U_z:'))
        layout.addWidget(Pixmap(self._logic.U_z, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('U_r:'))
        layout.addWidget(Pixmap(self._logic.U_r, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('U_h:'))
        layout.addWidget(Pixmap(self._logic.U_h, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('b_iz:'))
        layout.addWidget(Pixmap(self._logic.b_iz, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('b_ir:'))
        layout.addWidget(Pixmap(self._logic.b_ir, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('b_ih:'))
        layout.addWidget(Pixmap(self._logic.b_ih, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('b_rz:'))
        layout.addWidget(Pixmap(self._logic.b_rz, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('b_rr:'))
        layout.addWidget(Pixmap(self._logic.b_rr, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('b_rh:'))
        layout.addWidget(Pixmap(self._logic.b_rh, PIXMAP_SIDE, hv=True, hh=True, sb=True))

        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def set_links_in(self, links):
        if HintsKeeper().display == Display.COMPACT:
            self._block.set_links_in(links)
        else:
            self._neuron_ctrl.set_links_in(links, (np.transpose(self._logic.W_z), np.transpose(self._logic.W_r),
                                                   np.transpose(self._logic.W_h)))

    def set_bias(self, bounding):
        if HintsKeeper().display == Display.COMPACT:
            pass
        else:
            self._neuron_ctrl.set_bias(bounding, (self._logic.b_iz, self._logic.b_ir, self._logic.b_ih))


class VGRUBlock(VBlock):
    def __init__(self, scene, x, select, show_output):
        super().__init__(scene, x, select, show_output, 'GRU')


class VGRUNeuronController(VNeuronController):
    def __init__(self, scene, x, units, select, show_output, logic):
        super().__init__(scene, x, units, select, show_output, logic, VGRUNeuron, NEURON_REC_HEIGHT, NEURON_REC_WIDTH, NEURON_REC_MARGIN)

    def set_links_in(self, links, weights):
        W_z, W_r, W_h = weights

        for i in range(self._units):
            neuron = self._get_neuron(i)
            if neuron is not None:
                neuron.set_links_in(links[i], (W_z[i], W_r[i], W_h[i]))

    def set_bias(self, bounding, weights):
        b_z, b_r, b_h = weights

        bias = VBiasNeuron(self._scene, bounding)
        bind_out = bias.bind_out()
        binds_in = self.binds_in()

        links = np.full(len(binds_in), None, dtype=VLayer)
        for i in range(len(binds_in)):
            bind_in = binds_in[i]
            if bind_in is not None:
                tooltip = f'z: {"{:.4f}".format(b_z[i])}\nr: {"{:.4f}".format(b_r[i])}\n' \
                          f'h: {"{:.4f}".format(b_h[i])}'

                links[i] = VLink(bind_out, bind_in, WeightType.BIAS)
                links[i].set_tooltip(tooltip)
                self._get_neuron(i).set_link_bias(links[i])

                self._scene.addItem(links[i].get_item())
        bias.set_links_out(links)


class VGRUNeuron(VNeuron):
    def __init__(self, scene, x, y, select, show_output):
        super().__init__(scene)

        width = NEURON_REC_WIDTH
        height = NEURON_REC_HEIGHT

        self._item = QGraphicsRectItem(x, y, width, height)
        self._item.setZValue(10)
        self._item.setBrush(QBrush(QColor(255, 255, 255)))
        self._item.mousePressEvent = select
        self._item.mouseDoubleClickEvent = show_output
        self._text = draw_text('GRU', self._item.boundingRect(), HintsKeeper().names)
        self._text.setZValue(11)
        self._scene.addItem(self._item)
        self._scene.addItem(self._text)

        self._bind_in = QPointF(x, y + height / 2)
        self._bind_out = QPointF(x + width, y + height / 2)

        self._name_callback = WeakMethod(self, VGRUNeuron.update_name)
        HintsKeeper().attach_names(self._name_callback)

    def __del__(self):
        HintsKeeper().detach_names(self._name_callback)
        super().__del__()

    def update_name(self, value):
        self._scene.removeItem(self._text)

        self._text = draw_text('GRU', self._item.boundingRect(), value)
        self._text.setZValue(11)
        self._scene.addItem(self._text)

    def set_output(self, value, factor):
        super().set_output(value, factor)
        self._item.setToolTip(str(value))

    def set_links_in(self, links, weights):
        super().set_links_in(links, weights)

        if type(links) is not np.ndarray:
            return

        W_z, W_r, W_h = weights
        for i in range(self._links_in.shape[0]):
            if self._links_in[i] is not None:
                tooltip = f'z: {"{:.4f}".format(W_z[i])}\nr: {"{:.4f}".format(W_r[i])}\n' \
                          f'h: {"{:.4f}".format(W_h[i])}'
                self._links_in[i].set_tooltip(tooltip)

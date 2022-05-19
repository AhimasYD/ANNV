from PyQt5.QtWidgets import QLabel, QSpacerItem, QSizePolicy, QGraphicsRectItem
from PyQt5.QtCore import QPointF

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


class VSimpleRNN(VItem):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, w_info, w_flat, w_volume)

        self._select_callback = WeakMethod(self, VSimpleRNN.select)
        self._output_callback = WeakMethod(self, VSimpleRNN.show_output)
        if HintsKeeper().display == Display.COMPACT:
            self._connection = LinkType.UNITED
            self._block = VSimpleRNNBlock(self._scene, self._x, self._select_callback, self._output_callback)

        elif HintsKeeper().display == Display.EXTENDED:
            self._connection = LinkType.SEPARATED
            self._neuron_ctrl = VSimpleRNNNeuronController(self._scene, self._x, self._logic.units, self._select_callback, self._output_callback, logic)

        self._init_caption()

    def __del__(self):
        super().__del__()

    def select(self, event):
        super().select(event)

        layout = self._w_info.layout()

        layout.addWidget(QLabel(f'Type: {self._logic.type}'))
        layout.addWidget(QLabel(f'Activation: {self._logic.activation}'))
        layout.addItem(QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addWidget(QLabel('Kernel:'))
        layout.addWidget(Pixmap(self._logic.W, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('Recurrent kernel:'))
        layout.addWidget(Pixmap(self._logic.U, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('Bias:'))
        layout.addWidget(Pixmap(self._logic.b, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def set_links_in(self, links):
        if HintsKeeper().display == Display.COMPACT:
            self._block.set_links_in(links)
        else:
            self._neuron_ctrl.set_links_in(links, np.transpose(self._logic.W))

    def set_bias(self, bounding):
        if HintsKeeper().display == Display.COMPACT:
            pass
        else:
            self._neuron_ctrl.set_bias(bounding, self._logic.b)


class VSimpleRNNBlock(VBlock):
    def __init__(self, scene, x, select, show_output):
        super().__init__(scene, x, select, show_output, 'SimpleRNN')


class VSimpleRNNNeuronController(VNeuronController):
    def __init__(self, scene, x, units, select, show_output, logic):
        super().__init__(scene, x, units, select, show_output, logic, VSimpleRNNNeuron, NEURON_REC_HEIGHT, NEURON_REC_MARGIN)

    def set_links_in(self, links, weights):
        for i in range(self._units):
            neuron = self._get_neuron(i)
            if neuron is not None:
                neuron.set_links_in(links[i], weights[i])

    def set_bias(self, bounding, weights):
        bias = VBiasNeuron(self._scene, bounding)
        bind_out = bias.bind_out()
        binds_in = self.binds_in()

        links = np.full(len(binds_in), None, dtype=VLayer)
        for i in range(len(binds_in)):
            bind_in = binds_in[i]
            if bind_in is not None:
                links[i] = VLink(bind_out, bind_in, WeightType.BIAS)
                links[i].set_tooltip(str(weights[i]))
                self._get_neuron(i).set_link_bias(links[i])

                self._scene.addItem(links[i].get_item())
        bias.set_links_out(links)


class VSimpleRNNNeuron(VNeuron):
    def __init__(self, scene, x, y, select, show_output):
        super().__init__(scene)

        width = NEURON_REC_WIDTH
        height = NEURON_REC_HEIGHT

        self._item = QGraphicsRectItem(x, y, width, height)
        self._item.setZValue(10)
        self._item.mousePressEvent = select
        self._item.mouseDoubleClickEvent = show_output
        self._text = draw_text('SRNN', self._item.boundingRect(), HintsKeeper().names)
        self._text.setZValue(11)
        self._scene.addItem(self._item)
        self._scene.addItem(self._text)

        self._bind_in = QPointF(x, y + height / 2)
        self._bind_out = QPointF(x + width, y + height / 2)

        self._name_callback = WeakMethod(self, VSimpleRNNNeuron.update_name)
        HintsKeeper().attach_names(self._name_callback)

    def __del__(self):
        HintsKeeper().detach_names(self._name_callback)

    def update_name(self, value):
        self._scene.removeItem(self._text)

        self._text = draw_text('SRNN', self._item.boundingRect(), value)
        self._text.setZValue(11)
        self._scene.addItem(self._text)

    def set_output(self, value, factor):
        super().set_output(value, factor)
        self._item.setToolTip(str(value))

    def set_links_in(self, links, weights):
        super().set_links_in(links, weights)

        if type(links) is not np.ndarray:
            return

        for i in range(self._links_in.shape[0]):
            if self._links_in[i] is not None:
                self._links_in[i].set_tooltip(str(weights[i]))

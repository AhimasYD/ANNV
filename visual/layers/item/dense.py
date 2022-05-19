from PyQt5.QtWidgets import QLabel, QSpacerItem, QSizePolicy, QGraphicsEllipseItem
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QBrush

import numpy as np

from weak import WeakMethod
from visual.constants import Display
from visual.trivia import Pixmap, HintsKeeper, PIXMAP_SIDE
from visual.links import VLink, LinkType, WeightType
from visual.layers.constants import NEURON_SIDE, NEURON_MARGIN
from visual.layers.layer import VLayer
from visual.layers.trivia import VBlock, VBiasNeuron
from visual.layers.item.itemlayer import VItem
from visual.layers.item.neuroncontroller import VNeuronController
from visual.layers.item.neuron import VNeuron


class VDense(VItem):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, w_info, w_flat, w_volume)

        self._select_callback = WeakMethod(self, VDense.select)
        self._output_callback = WeakMethod(self, VDense.show_output)
        # Display as block
        if HintsKeeper().display == Display.COMPACT:
            self._connection = LinkType.UNITED
            self._block = VDenseBlock(self._scene, self._x, self._select_callback, self._output_callback)

        # Display as neurons
        elif HintsKeeper().display == Display.EXTENDED:
            self._connection = LinkType.SEPARATED
            self._neuron_ctrl = VDenseNeuronController(self._scene, self._x, self._logic.units, self._select_callback, self._output_callback, logic)

        self._init_caption()

    def __del__(self):
        super().__del__()

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

    def set_links_in(self, links):
        if HintsKeeper().display == Display.COMPACT:
            self._block.set_links_in(links)
        else:
            self._neuron_ctrl.set_links_in(links, np.transpose(self._logic.kernel))

    def set_bias(self, bounding):
        if HintsKeeper().display == Display.COMPACT:
            pass
        else:
            self._neuron_ctrl.set_bias(bounding, self._logic.bias)


class VDenseBlock(VBlock):
    def __init__(self, scene, x, select, show_output):
        super().__init__(scene, x, select, show_output, 'Dense')


class VDenseNeuronController(VNeuronController):
    def __init__(self, scene, x, units, select, show_output, logic):
        super().__init__(scene, x, units, select, show_output, logic, VDenseNeuron, NEURON_SIDE, NEURON_SIDE, NEURON_MARGIN)

    def set_links_in(self, links, weights):
        maximum = max(weights.min(), weights.max(), key=abs)
        for i in range(self._units):
            neuron = self._get_neuron(i)
            if neuron is not None:
                neuron.set_links_in(links[i], weights=(weights[i], maximum))

    def set_bias(self, bounding, weights):
        self._bias = VBiasNeuron(self._scene, bounding)
        bind_out = self._bias.bind_out()
        binds_in = self.binds_in()

        maximum = max(weights.min(), weights.max(), key=abs)

        links = np.full(len(binds_in), None, dtype=VLayer)
        for i in range(len(binds_in)):
            bind_in = binds_in[i]
            if bind_in is not None:
                links[i] = VLink(bind_out, bind_in, WeightType.BIAS)
                links[i].set_weight(weights[i], maximum)
                links[i].set_tooltip(str(weights[i]))
                self._get_neuron(i).set_link_bias(links[i])

                self._scene.addItem(links[i].get_item())
        self._bias.set_links_out(links)


class VDenseNeuron(VNeuron):
    def __init__(self, scene, x, y, select, show_output):
        super().__init__(scene)

        side = NEURON_SIDE

        self._item = QGraphicsEllipseItem(x, y, side, side)
        self._item.setZValue(10)
        self._item.setBrush(QBrush(QColor(255, 255, 255)))
        self._item.mousePressEvent = select
        self._item.mouseDoubleClickEvent = show_output
        self._scene.addItem(self._item)

        self._bind_in = QPointF(x, y + side / 2)
        self._bind_out = QPointF(x + side, y + side / 2)

        self.update_activation(HintsKeeper().activation)

    def __del__(self):
        super().__del__()

    def set_output(self, value, factor):
        super().set_output(value, factor)
        self._item.setToolTip(str(value))

    def set_links_in(self, links, weights):
        super().set_links_in(links, weights)

        if type(links) is not np.ndarray:
            return

        array, maximum = weights
        for i in range(self._links_in.shape[0]):
            if self._links_in[i] is not None:
                self._links_in[i].set_weight(array[i], maximum)
                self._links_in[i].set_tooltip(str(array[i]))

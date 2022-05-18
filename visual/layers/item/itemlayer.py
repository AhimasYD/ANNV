from PyQt5.QtWidgets import *

from visual.constants import *
from visual.trivia.pixmap import Pixmap
from visual.trivia.hintskeeper import HintsKeeper

from visual.layers.layer import VLayer
from widgets.outputwindow import OutputWindow


class VItem(VLayer):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, w_info, w_flat, w_volume)
        self._block = None
        self._neuron_ctrl = None

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
        if HintsKeeper().display == Display.COMPACT:
            return self._connection, self._block.bind_in()
        else:
            return self._connection, self._neuron_ctrl.binds_in()

    def binds_out(self):
        if HintsKeeper().display == Display.COMPACT:
            return self._connection, self._block.bind_out()
        else:
            return self._connection, self._neuron_ctrl.binds_out()

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
            self._neuron_ctrl.set_bias(bounding, self._logic.bias)

from PyQt5.QtWidgets import QLabel, QSpacerItem, QSizePolicy

import numpy as np

from visual.constants import *
from visual.pixmap import Pixmap
from visual.layers.conv.kernelwrapper import KernelWrapperFlat

from visual.layers.conv.conv import VConv
from visual.layers.block import VBlock
from visual.layers.conv.convkernelcontroller import VConvKernelController
from visual.layers.conv.convkernel import VConvKernel


class VConv2D(VConv):
    def __init__(self, logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume)

        self._connection = LinkType.UNITED
        if self._o_display == Display.COMPACT:
            self._block = VConv2DBlock(self._scene, self._x, self.select, self._o_names)
        elif self._o_display == Display.EXTENDED:
            self._kernel_ctrl = VConv2DKernelController(self._scene, self._x, self._logic.channel_num, self._logic.filter_num,
                                                        self._logic.filters[self._filter], self.select)

    def select(self, event):
        super().select(event)

        layout = self._w_info.layout()

        layout.addWidget(QLabel(f'Type: {self._logic.type}'))
        layout.addWidget(QLabel(f'Filters: {self._logic.filter_num}'))
        layout.addWidget(QLabel(f'Channels: {self._logic.channel_num}'))
        layout.addWidget(QLabel(f'Kernel shape: {self._logic.kernel_shape}'))
        layout.addWidget(QLabel(f'Padding: {self._logic.padding}'))
        layout.addWidget(QLabel(f'Strides: {self._logic.strides}'))
        layout.addWidget(QLabel(f'Dilation rate: {self._logic.dilation_rate}'))
        layout.addWidget(QLabel(f'Groups: {self._logic.groups}'))
        layout.addWidget(QLabel(f'Activation: {self._logic.activation}'))

        self._kernels = np.empty(self._logic.channel_num, dtype=Pixmap)
        for i in range(self._logic.channel_num):
            self._kernels[i] = Pixmap(self._logic.filters[self._filter, i], PIXMAP_SIDE, hv=True, hh=True, sb=True, mr=None)
            layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
            layout.addWidget(QLabel(f'Filter_{self._filter} / Kernel_{i}:'))
            layout.addWidget(self._kernels[i])

        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('Bias:'))
        layout.addWidget(Pixmap(self._logic.bias, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self._w_flat.show()
        self._w_flat.filter_num.setText(f'{self._filter}')
        self._w_flat.filter_prev.mousePressEvent = self.filter_prev
        self._w_flat.filter_next.mousePressEvent = self.filter_next

    def update(self):
        self._w_flat.filter_num.setText(f'{self._filter}')
        for i in range(self._logic.channel_num):
            self._kernels[i].update(self._logic.filters[self._filter, i])
        if self._kernel_ctrl is not None:
            self._kernel_ctrl.update(self._logic.filters[self._filter], self._filter)


class VConv2DBlock(VBlock):
    def __init__(self, scene, x, select, opt_names):
        super().__init__(scene, x, select, opt_names, 'Conv2D')


class VConv2DKernelController(VConvKernelController):
    def __init__(self, scene, x, units, filters, arrays, select):
        super().__init__(scene, x, units, filters, arrays, select, VConv2DKernel)


class VConv2DKernel(VConvKernel):
    def __init__(self, scene, array, x, y, filters, select):
        super().__init__(scene, array, x, y, filters, select, KernelWrapperFlat)


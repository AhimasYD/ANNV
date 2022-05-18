from PyQt5.QtWidgets import QLabel, QSpacerItem, QSizePolicy

import numpy as np

from visual.constants import Display
from visual.trivia import Pixmap, PIXMAP_SIDE, HintsKeeper
from visual.links import LinkType
from visual.layers.trivia import VBlock
from visual.layers.conv.convlayer import VConv
from visual.layers.conv.convkernelcontroller import VConvKernelController
from visual.layers.conv.convkernel import VConvKernel
from visual.layers.conv.kernelwrapper import KernelWrapperVolume


class VConv3D(VConv):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, w_info, w_flat, w_volume)
        self._depth = 0

        self._connection = LinkType.UNITED
        if HintsKeeper().display == Display.COMPACT:
            self._block = VConv3DBlock(self._scene, self._x, self.select, self.show_output)
        elif HintsKeeper().display == Display.EXTENDED:
            self._kernel_ctrl = VConv3DKernelController(self._scene, self._x, self._logic.channel_num, self._logic.filter_num,
                                                        self._logic.filters[self._filter, self._depth], self.select, self.show_output)

        self._init_caption()

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
            self._kernels[i] = Pixmap(self._logic.filters[self._filter, self._depth, i], PIXMAP_SIDE, hv=True, hh=True, sb=True, mr=None)
            layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
            layout.addWidget(QLabel(f'Channel_{i}:'))
            layout.addWidget(self._kernels[i])

        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('Bias:'))
        layout.addWidget(Pixmap(self._logic.bias, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self._w_volume.show()
        self._w_volume.num_0.setText(f'{self._filter}')
        self._w_volume.button_0_prev.mousePressEvent = self.filter_prev
        self._w_volume.button_0_next.mousePressEvent = self.filter_next
        self._w_volume.num_1.setText(f'{self._depth}')
        self._w_volume.button_1_prev.mousePressEvent = self.depth_prev
        self._w_volume.button_1_next.mousePressEvent = self.depth_next

    def update(self):
        self._w_flat.num.setText(f'{self._filter}')
        for i in range(self._logic.channel_num):
            self._w_volume.num_0.setText(f'{self._filter}')
            self._w_volume.num_1.setText(f'{self._depth}')
            self._kernels[i].update_map(self._logic.filters[self._filter, self._depth, i])
        if self._kernel_ctrl is not None:
            self._kernel_ctrl.update(self._logic.filters[self._filter, self._depth], self._filter)

    def depth_prev(self, event):
        if self._depth - 1 >= 0:
            self._depth -= 1
            self.update()

    def depth_next(self, event):
        if self._depth + 1 < self._logic.depth:
            self._depth += 1
            self.update()


class VConv3DBlock(VBlock):
    def __init__(self, scene, x, select, show_output):
        super().__init__(scene, x, select, show_output, 'Conv3D')


class VConv3DKernelController(VConvKernelController):
    def __init__(self, scene, x, units, filters, arrays, select, show_output):
        super().__init__(scene, x, units, filters, arrays, select, show_output, VConv3DKernel)


class VConv3DKernel(VConvKernel):
    def __init__(self, scene, array, x, y, filters, select, show_output):
        super().__init__(scene, array, x, y, filters, select, show_output, KernelWrapperVolume)



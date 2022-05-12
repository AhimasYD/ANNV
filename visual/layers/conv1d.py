import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer


class VConv1D(VLayer):
    def __init__(self, logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume)

        self.filter = 0
        self.block = None
        self.kernels = None
        self.widget_kernels = None

        if self._o_display == Display.COMPACT:
            self.block = VConv1DBlock(self._scene, self._x, self.select, self._o_names)
        elif self._o_display == Display.EXTENDED:
            channels = self._logic.channel_num
            self.kernels = np.empty(channels, dtype=VConv1DKernel)
            for i in range(channels):
                self.kernels[i] = VConv1DKernel(self._scene, self._logic.filters[self.filter, i], self._x, 0, self.select)

            height = self.kernels[0].height()
            total_height = channels * height + (channels - 1) * KERNEL_MARGIN
            y = -total_height / 2 + height / 2
            for i in range(channels):
                kernel = self.kernels[i]
                kernel.move_to(self._x, y)
                y += height + KERNEL_MARGIN

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

        self.widget_kernels = np.empty(self._logic.channel_num, dtype=Pixmap)
        for i in range(self._logic.channel_num):
            self.widget_kernels[i] = Pixmap(self._logic.filters[self.filter, i], PIXMAP_SIDE, hv=True, hh=True, sb=True, mr=None)
            layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
            layout.addWidget(QLabel(f'Filter_{self.filter} / Kernel_{i}:'))
            layout.addWidget(self.widget_kernels[i])

        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('Bias:'))
        layout.addWidget(Pixmap(self._logic.bias, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self._w_flat.show()
        self._w_flat.filter_num.setText(f'{self.filter}')
        self._w_flat.filter_prev.mousePressEvent = self.filter_prev
        self._w_flat.filter_next.mousePressEvent = self.filter_next

    def update(self):
        self._w_flat.filter_num.setText(f'{self.filter}')
        if self.kernels is not None:
            for i in range(self._logic.channel_num):
                self.kernels[i].update(self._logic.filters[self.filter, i])
        for i in range(self._logic.channel_num):
            self.widget_kernels[i].update(self._logic.filters[self.filter, i])

    def filter_prev(self, event):
        if self.filter - 1 >= 0:
            self.filter -= 1
            self.update()

    def filter_next(self, event):
        if self.filter + 1 < self._logic.filter_num:
            self.filter += 1
            self.update()


class VConv1DBlock:
    def __init__(self, scene, x, select, opt_names):
        self._scene = scene

        self._rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self._rect.mousePressEvent = select
        self._text = draw_text('Conv1D', self._rect.boundingRect(), opt_names)

        self._scene.addItem(self._rect)
        self._scene.addItem(self._text)


class VConv1DKernel:
    def __init__(self, scene, array, x, y, select):
        self._scene = scene

        self._pixmap = Pixmap(array, PIXMAP_SIDE, hv=False, hh=False, sb=False)
        self._pixmap.mousePressEvent = select
        self._proxy = self._scene.addWidget(self._pixmap)

        self.move_to(x, y)

    def height(self):
        return self._pixmap.height()

    def width(self):
        return self._pixmap.width()

    def move_to(self, x_left, y):
        y = y - self._pixmap.height() / 2
        self._proxy.setX(x_left)
        self._proxy.setY(y)

    def update(self, array):
        self._pixmap.update(array)

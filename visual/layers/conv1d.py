import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer
from .placeholder import VPlaceholder


class VConv1D(VLayer):
    def __init__(self, logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume)

        self._filter = 0
        self._block = None
        self._kernel_ctrl = None
        self._kernels = None

        self._connection = LinkType.UNITED
        if self._o_display == Display.COMPACT:
            self._block = VConv1DBlock(self._scene, self._x, self.select, self._o_names)
        elif self._o_display == Display.EXTENDED:
            self._kernel_ctrl = VConv1DKernelController(self._scene, self._x, self._logic.channel_num,
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
            self._kernel_ctrl.update(self._logic.filters[self._filter])

    def filter_prev(self, event):
        if self._filter - 1 >= 0:
            self._filter -= 1
            self.update()

    def filter_next(self, event):
        if self._filter + 1 < self._logic.filter_num:
            self._filter += 1
            self.update()

    def binds_in(self):
        if self._o_display == Display.COMPACT:
            return self._connection, self._block.bind_in()
        else:
            return self._connection, self._kernel_ctrl.bind_in()

    def binds_out(self):
        if self._o_display == Display.COMPACT:
            return self._connection, self._block.bind_out()
        else:
            return self._connection, self._kernel_ctrl.bind_out()


class VConv1DBlock:
    def __init__(self, scene, x, select, opt_names):
        self._scene = scene

        self._rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self._rect.mousePressEvent = select
        self._text = draw_text('Conv1D', self._rect.boundingRect(), opt_names)
        self._scene.addItem(self._rect)
        self._scene.addItem(self._text)

        self._bind_in = QPointF(x - BLOCK_WIDTH / 2, 0)
        self._bind_out = QPointF(x + BLOCK_WIDTH / 2, 0)

    def bind_in(self):
        return self._bind_in

    def bind_out(self):
        return self._bind_out


class VConv1DKernelController:
    def __init__(self, scene, x, units, arrays, select):
        self._scene = scene
        self._x = x
        self._units = units

        self._kernels = None

        self._placeholder = None
        self._kernels_start = None
        self._kernels_end = None

        # No placeholder needed
        if units <= PLACEHOLDER_MAX_NEURONS * 2:
            self._kernels = np.empty(units, dtype=VConv1DKernel)

            for i in range(self._units):
                self._kernels[i] = VConv1DKernel(self._scene, arrays[i], self._x, 0, select)

            height = self._kernels[0].height()
            width = self._kernels[0].width()
            total_height = self._units * height + (self._units - 1) * KERNEL_MARGIN
            y = -total_height / 2 + height / 2
            for i in range(self._units):
                kernel = self._kernels[i]
                kernel.move_to(self._x, y)
                y += height + KERNEL_MARGIN

        # Placeholder needed
        else:
            self._placeholder = VPlaceholder(PLACEHOLDER_SIDE, PLACEHOLDER_MARGIN_IN, x, 0)
            self._placeholder.mousePressEvent = select
            self._scene.addItem(self._placeholder)

            self._kernels_start = np.empty(PLACEHOLDER_MAX_KERNELS, dtype=VConv1DKernel)
            self._kernels_end = np.empty(PLACEHOLDER_MAX_KERNELS, dtype=VConv1DKernel)

            for i in range(PLACEHOLDER_MAX_KERNELS):
                j = self._units - PLACEHOLDER_MAX_KERNELS + i
                self._kernels_start[i] = VConv1DKernel(self._scene, arrays[i], self._x, 0, select)
                self._kernels_end[i] = VConv1DKernel(self._scene, arrays[j], self._x, 0, select)

            height = self._kernels_start[0].height()
            width = self._kernels_start[0].width()
            total_height = 2 * PLACEHOLDER_MAX_KERNELS * height + 2 * PLACEHOLDER_MAX_KERNELS * KERNEL_MARGIN
            total_height += self._placeholder.boundingRect().height() + 2 * PLACEHOLDER_MARGIN_OUT

            y = -total_height / 2 + height / 2
            for i in range(PLACEHOLDER_MAX_KERNELS):
                kernel = self._kernels_start[i]
                kernel.move_to(self._x, y)
                y += height + KERNEL_MARGIN
            y += self._placeholder.boundingRect().height()
            y += 2 * PLACEHOLDER_MARGIN_OUT
            y += KERNEL_MARGIN
            for i in range(PLACEHOLDER_MAX_KERNELS):
                kernel = self._kernels_end[i]
                kernel.move_to(self._x, y)
                y += height + KERNEL_MARGIN

            self._placeholder.moveBy(self._kernels_start[0].width() / 2, 0)

        self._bind_in = QPointF(x, 0)
        self._bind_out = QPointF(x + width, 0)

    def update(self, arrays):
        if self._kernels is not None:
            for i in range(self._units):
                self._kernels[i].update(arrays[i])
        else:
            for i in range(PLACEHOLDER_MAX_KERNELS):
                j = self._units - PLACEHOLDER_MAX_KERNELS + i
                self._kernels_start[i].update(arrays[i])
                self._kernels_end[i].update(arrays[j])

    def bind_in(self):
        return self._bind_in

    def bind_out(self):
        return self._bind_out


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

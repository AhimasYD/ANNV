import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer


class VConv2D(VLayer):
    def __init__(self, logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions,
                 opt_bias, widget, flat, volume):
        super().__init__(logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias,
                         widget, flat, volume)

        self.filter = 0
        self.block = None
        self.kernels = None
        self.widget_kernels = None

        if self.opt_display == Display.COMPACT:
            self.block = VConv2DBlock(self.scene, self.pos_x, self.select, self.opt_names)
        elif self.opt_display == Display.EXTENDED:
            channels = self.logic.channel_num
            self.kernels = np.empty(channels, dtype=VConv2DKernel)
            for i in range(channels):
                self.kernels[i] = VConv2DKernel(self.scene, self.logic.filters[self.filter, i], self.pos_x, 0, self.select)

            height = self.kernels[0].height()
            total_height = channels * height + (channels - 1) * KERNEL_MARGIN
            y = -total_height / 2 + height / 2
            for i in range(channels):
                kernel = self.kernels[i]
                kernel.move_to(self.pos_x, y)
                y += height + KERNEL_MARGIN

    def select(self, event):
        super().select(event)

        layout = self.widget.layout()
        clear_layout(layout)

        layout.addWidget(QLabel(f'Type: {self.logic.type}'))
        layout.addWidget(QLabel(f'Filters: {self.logic.filter_num}'))
        layout.addWidget(QLabel(f'Channels: {self.logic.channel_num}'))
        layout.addWidget(QLabel(f'Kernel shape: {self.logic.kernel_shape}'))
        layout.addWidget(QLabel(f'Padding: {self.logic.padding}'))
        layout.addWidget(QLabel(f'Strides: {self.logic.strides}'))
        layout.addWidget(QLabel(f'Dilation rate: {self.logic.dilation_rate}'))
        layout.addWidget(QLabel(f'Groups: {self.logic.groups}'))
        layout.addWidget(QLabel(f'Activation: {self.logic.activation}'))

        self.widget_kernels = np.empty(self.logic.channel_num, dtype=Pixmap)
        for i in range(self.kernels.size):
            self.widget_kernels[i] = Pixmap(self.logic.filters[self.filter, i], CELL_TABLE_SIZE, hv=True, hh=True, sb=True, mr=None)
            layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
            layout.addWidget(QLabel(f'Filter_{self.filter} / Kernel_{i}:'))
            layout.addWidget(self.widget_kernels[i])

        layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(QLabel('Bias:'))
        layout.addWidget(Pixmap(self.logic.bias, CELL_TABLE_SIZE, hv=True, hh=True, sb=True))
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.flat.show()
        self.flat.filter_num.setText(f'{self.filter}')
        self.flat.filter_prev.mousePressEvent = self.filter_prev
        self.flat.filter_next.mousePressEvent = self.filter_next

    def update(self):
        self.flat.filter_num.setText(f'{self.filter}')
        if self.kernels is not None:
            for i in range(self.logic.channel_num):
                self.kernels[i].update(self.logic.filters[self.filter, i])
        for i in range(self.logic.channel_num):
            self.widget_kernels[i].update(self.logic.filters[self.filter, i])

    def filter_prev(self, event):
        if self.filter - 1 >= 0:
            self.filter -= 1
            self.update()

    def filter_next(self, event):
        if self.filter + 1 < self.logic.filter_num:
            self.filter += 1
            self.update()


class VConv2DBlock:
    def __init__(self, scene, x, callback, opt_names):
        self.scene = scene

        self.rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.bound = self.rect.boundingRect()
        self.text = draw_text('Conv2D', self.bound, opt_names)

        self.scene.addItem(self.rect)
        self.scene.addItem(self.text)

        self.rect.mousePressEvent = callback


class VConv2DKernel:
    def __init__(self, scene, array, x, y, callback):
        self.scene = scene
        self.pixmap = Pixmap(array, CELL_TABLE_SIZE, hv=False, hh=False, sb=False)
        self.proxy = self.scene.addWidget(self.pixmap)
        self.pixmap.mousePressEvent = callback
        self.move_to(x, y)

    def height(self):
        return self.pixmap.height()

    def width(self):
        return self.pixmap.width()

    def move_to(self, x_left, y):
        y = y - self.pixmap.height() / 2
        self.proxy.setX(x_left)
        self.proxy.setY(y)

    def update(self, array):
        self.pixmap.update(array)

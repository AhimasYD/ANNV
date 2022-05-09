from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic.layers import *

from .constants import *
from .functions import *
from .layer import VLayer
from .pixmap import Pixmap


class VConv2D(VLayer):
    def __init__(self, logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias, widget):
        super().__init__(logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias, widget)

        if self.opt_display == Display.COMPACT:
            self.block = VConv2DBlock(self.scene, self.pos_x, self.select)
        elif self.opt_display == Display.EXTENDED:
            self.kernels = []
            channels = self.logic.channel_num
            for i in range(channels):
                kernel = VConv2DKernel(self.scene, logic.filters[0, i], self.pos_x, 0, self.select)
                self.kernels.append(kernel)

    def select(self, event):
        layout = self.widget.layout()
        clear_layout(layout)


class VConv2DBlock:
    def __init__(self, scene, x, callback):
        self.scene = scene

        self.rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.bound = self.rect.boundingRect()
        self.text = draw_text('Conv2D', self.bound)

        self.scene.addItem(self.rect)
        self.scene.addItem(self.text)

        self.rect.mousePressEvent = callback


class VConv2DKernel:
    def __init__(self, scene, array, x, y, callback):
        self.scene = scene

        self.pixmap = Pixmap(array, CELL_TABLE_SIZE, hv=False, hh=False, sb=False)
        self.proxy = self.scene.addWidget(self.pixmap)

        print('PIXMAP', self.pixmap.width())
        print('PROXY', self.proxy.width())
        print('')

        self.proxy.mousePressEvent = callback

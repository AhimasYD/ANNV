import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from visual.layers.layer import VLayer
from visual.links import VLink
from visual.layers.kernelwrapper import KernelWrapperFlat

from .convkernelcontroller import VConvKernelController
from .convkernel import VConvKernel


class VConv2D(VLayer):
    def __init__(self, logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume)

        self._filter = 0
        self._block = None
        self._kernel_ctrl = None
        self._kernels = None

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

    def set_links_in(self, links):
        if self._o_display == Display.COMPACT:
            self._block.set_links_in(links)
        else:
            self._kernel_ctrl.set_links_in(links)

    def set_links_out(self, links):
        if self._o_display == Display.COMPACT:
            self._block.set_links_out(links)
        else:
            self._kernel_ctrl.set_links_out(links)

    def set_weight_color_hint(self, hint: WeightColor, forward: bool = False):
        if self._o_display == Display.COMPACT:
            self._block.set_weight_color_hint(hint, forward)
        else:
            self._kernel_ctrl.set_weight_color_hint(hint, forward)

    def set_weight_thick_hint(self, hint: WeightThick, forward: bool = False):
        if self._o_display == Display.COMPACT:
            self._block.set_weight_thick_hint(hint, forward)
        else:
            self._kernel_ctrl.set_weight_thick_hint(hint, forward)


class VConv2DBlock:
    def __init__(self, scene, x, select, opt_names):
        self._scene = scene

        self._rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self._rect.mousePressEvent = select
        self._text = draw_text('Conv2D', self._rect.boundingRect(), opt_names)
        self._scene.addItem(self._rect)
        self._scene.addItem(self._text)

        self._bind_in = QPointF(x - BLOCK_WIDTH / 2, 0)
        self._bind_out = QPointF(x + BLOCK_WIDTH / 2, 0)

        self._links_in = None
        self._links_out = None

    def bind_in(self):
        return self._bind_in

    def bind_out(self):
        return self._bind_out

    def set_links_in(self, links):
        self._links_in = links

    def set_links_out(self, links):
        self._links_out = links

    def set_weight_color_hint(self, hint: WeightColor, forward: bool = False):
        if self._links_in is None:
            return

        if type(self._links_in) is VLink:
            self._links_in.set_color_hint(hint)
        elif type(self._links_in) is np.ndarray:
            for i in range(self._links_in.shape[0]):
                link = self._links_in[i]
                if link is None:
                    continue
                link.set_color_hint(hint)

        if not forward or self._links_out is None:
            return

        if type(self._links_out) is VLink:
            self._links_out.set_color_hint(hint)
        elif type(self._links_out) is np.ndarray:
            for i in range(self._links_out.shape[0]):
                link = self._links_out[i]
                if link is None:
                    continue
                link.set_color_hint(hint)

    def set_weight_thick_hint(self, hint: WeightThick, forward: bool = False):
        if self._links_in is None:
            return

        if type(self._links_in) is VLink:
            self._links_in.set_thick_hint(hint)
        elif type(self._links_in) is np.ndarray:
            for i in range(self._links_in.shape[0]):
                link = self._links_in[i]
                if link is None:
                    continue
                link.set_thick_hint(hint)

        if not forward or self._links_out is None:
            return

        if type(self._links_out) is VLink:
            self._links_out.set_thick_hint(hint)
        elif type(self._links_out) is np.ndarray:
            for i in range(self._links_out.shape[0]):
                link = self._links_out[i]
                if link is None:
                    continue
                link.set_thick_hint(hint)


class VConv2DKernelController(VConvKernelController):
    def __init__(self, scene, x, units, filters, arrays, select):
        super().__init__(scene, x, units, filters, arrays, select, VConv2DKernel)


class VConv2DKernel(VConvKernel):
    def __init__(self, scene, array, x, y, filters, select):
        super().__init__(scene, array, x, y, filters, select, KernelWrapperFlat)



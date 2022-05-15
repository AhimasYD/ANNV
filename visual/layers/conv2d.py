import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer
from .placeholder import VPlaceholder
from visual.links import VLink
from .kernelwrapper import KernelWrapperFlat


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


class VConv2DKernelController:
    def __init__(self, scene, x, units, filters, arrays, select):
        self._scene = scene
        self._x = x
        self._units = units

        self._kernels = None

        self._placeholder = None
        self._kernels_start = None
        self._kernels_end = None

        # No placeholder needed
        if units <= PLACEHOLDER_MAX_NEURONS * 2:
            self._kernels = np.empty(units, dtype=VConv2DKernel)

            for i in range(self._units):
                self._kernels[i] = VConv2DKernel(self._scene, arrays[i], self._x, 0, filters, select)

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

            self._kernels_start = np.empty(PLACEHOLDER_MAX_KERNELS, dtype=VConv2DKernel)
            self._kernels_end = np.empty(PLACEHOLDER_MAX_KERNELS, dtype=VConv2DKernel)

            for i in range(PLACEHOLDER_MAX_KERNELS):
                j = self._units - PLACEHOLDER_MAX_KERNELS + i
                self._kernels_start[i] = VConv2DKernel(self._scene, arrays[i], self._x, 0, filters, select)
                self._kernels_end[i] = VConv2DKernel(self._scene, arrays[j], self._x, 0, filters, select)

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

        self._links_in = None
        self._links_out = None

    def update(self, arrays, filter_num):
        if self._kernels is not None:
            for i in range(self._units):
                self._kernels[i].update(arrays[i], filter_num)
        else:
            for i in range(PLACEHOLDER_MAX_KERNELS):
                j = self._units - PLACEHOLDER_MAX_KERNELS + i
                self._kernels_start[i].update(arrays[i], filter_num)
                self._kernels_end[i].update(arrays[j], filter_num)

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
                if self._links_in[i] is not None:
                    self._links_in[i].set_color_hint(hint)
        else:
            raise TypeError

        if not forward:
            return
        if type(self._links_out) is VLink:
            self._links_out.set_color_hint(hint)
        elif type(self._links_out) is np.ndarray:
            for i in range(self._links_out.shape[0]):
                if self._links_out[i] is not None:
                    self._links_out[i].set_color_hint(hint)
        else:
            raise TypeError

    def set_weight_thick_hint(self, hint: WeightThick, forward: bool = False):
        if self._links_in is None:
            return

        if type(self._links_in) is VLink:
            self._links_in.set_thick_hint(hint)
        elif type(self._links_in) is np.ndarray:
            for i in range(self._links_in.shape[0]):
                if self._links_in[i] is not None:
                    self._links_in[i].set_thick_hint(hint)
        else:
            raise TypeError

        if not forward or self._links_out is None:
            return
        if type(self._links_out) is VLink:
            self._links_out.set_thick_hint(hint)
        elif type(self._links_out) is np.ndarray:
            for i in range(self._links_out.shape[0]):
                if self._links_out[i] is not None:
                    self._links_out[i].set_thick_hint(hint)
        else:
            raise TypeError


class VConv2DKernel:
    def __init__(self, scene, array, x, y, filters, select):
        self._scene = scene

        self._pixmap = Pixmap(array, PIXMAP_SIDE, hv=False, hh=False, sb=False)
        self._pixmap.mousePressEvent = select
        self._proxy = self._scene.addWidget(self._pixmap)

        self._wrapper = KernelWrapperFlat(self._proxy.pos(), filters, self._proxy, select=select)
        self._scene.addItem(self._wrapper)

        self.move_to(x, y)

    def height(self):
        return self._pixmap.height()

    def width(self):
        return self._pixmap.width()

    def move_to(self, x_left, y):
        pos = QPointF(x_left, y - self._pixmap.height() / 2)
        self._wrapper.move_to(pos)

    def update(self, array, filter_num):
        self._pixmap.update(array)
        self._wrapper.set_active(filter_num)


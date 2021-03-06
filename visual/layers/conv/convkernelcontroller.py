from PyQt5.QtCore import QPointF

import numpy as np

from visual.constants import WeightColor, WeightThick
from visual.links import VLink
from visual.layers.constants import PLACEHOLDER_SIDE, PLACEHOLDER_MAX_KERNELS, PLACEHOLDER_MARGIN_IN, PLACEHOLDER_MARGIN_OUT
from visual.layers.constants import KERNEL_MARGIN
from visual.layers.trivia import VPlaceholder


class VConvKernelController:
    def __init__(self, scene, x, units, filters, arrays, select, show_output, dtype):
        self._scene = scene
        self._x = x
        self._units = units

        self._kernels = None

        self._placeholder = None
        self._kernels_start = None
        self._kernels_end = None

        # No placeholder needed
        if units <= PLACEHOLDER_MAX_KERNELS * 2:
            self._kernels = np.empty(units, dtype=dtype)

            for i in range(self._units):
                self._kernels[i] = dtype(self._scene, arrays[i], self._x, 0, filters, select, show_output)

            width = self._kernels[0].bounding().width()
            height = self._kernels[0].bounding().height()
            total_height = self._units * height + (self._units - 1) * KERNEL_MARGIN
            y = -total_height / 2
            for i in range(self._units):
                kernel = self._kernels[i]
                kernel.move_to(self._x, y)
                y += height + KERNEL_MARGIN

            self._kernels[0].bounding()


        # Placeholder needed
        else:
            self._placeholder = VPlaceholder(PLACEHOLDER_SIDE, PLACEHOLDER_MARGIN_IN, x, 0)
            self._placeholder.mousePressEvent = select
            self._scene.addItem(self._placeholder)

            self._kernels_start = np.empty(PLACEHOLDER_MAX_KERNELS, dtype=dtype)
            self._kernels_end = np.empty(PLACEHOLDER_MAX_KERNELS, dtype=dtype)

            for i in range(PLACEHOLDER_MAX_KERNELS):
                j = self._units - PLACEHOLDER_MAX_KERNELS + i
                self._kernels_start[i] = dtype(self._scene, arrays[i], self._x, 0, filters, select, show_output)
                self._kernels_end[i] = dtype(self._scene, arrays[j], self._x, 0, filters, select, show_output)

            width = self._kernels_start[0].bounding().width()
            height = self._kernels_start[0].bounding().height()
            total_height = 2 * PLACEHOLDER_MAX_KERNELS * height + 2 * PLACEHOLDER_MAX_KERNELS * KERNEL_MARGIN
            total_height += self._placeholder.boundingRect().height() + 2 * PLACEHOLDER_MARGIN_OUT

            y = -total_height / 2
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

            self._placeholder.setPos(self._x + width / 2 - self._placeholder.boundingRect().width() / 2,
                                     0 - self._placeholder.boundingRect().height() / 2)

        self._bind_in = QPointF(self._x, 0)
        self._bind_out = QPointF(self._x + width, 0)

        self._links_in = None
        self._links_out = None

    def _get_kernel(self, i):
        if self._kernels is not None:
            return self._kernels[i]
        else:
            if i < PLACEHOLDER_MAX_KERNELS:
                return self._kernels_start[i]
            elif i >= self._units - PLACEHOLDER_MAX_KERNELS:
                return self._kernels_end[i - (self._units - PLACEHOLDER_MAX_KERNELS)]
            else:
                return None

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

    def bounding(self):
        unit_0 = self._get_kernel(0)
        unit_1 = self._get_kernel(self._units - 1)
        return unit_0.bounding().united(unit_1.bounding())

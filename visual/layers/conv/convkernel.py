from PyQt5.QtCore import QPointF

from visual.constants import *
from visual.pixmap import Pixmap


class VConvKernel:
    def __init__(self, scene, array, x, y, filters, select, wrapper_type):
        self._scene = scene

        self._pixmap = Pixmap(array, PIXMAP_SIDE, hv=False, hh=False, sb=False)
        self._pixmap.mousePressEvent = select
        self._proxy = self._scene.addWidget(self._pixmap)

        self._wrapper = wrapper_type(self._proxy.pos(), filters, self._proxy, select=select)
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

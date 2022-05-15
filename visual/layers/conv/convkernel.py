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

    def bounding(self):
        bound = self._wrapper.childrenBoundingRect()
        bound.moveTo(self._wrapper.pos())
        return bound

    def move_to(self, x, y):
        self._wrapper.setPos(x, y)

    def update(self, array, filter_num):
        self._pixmap.update(array)
        self._wrapper.set_active(filter_num)
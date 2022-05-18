from visual.constants import *
from visual.trivia.pixmap import Pixmap


class VConvKernel:
    def __init__(self, scene, array, x, y, filters, select, show_output, wrapper_type):
        self._scene = scene

        self._pixmap = Pixmap(array, PIXMAP_SIDE, hv=False, hh=False, sb=False)
        self._proxy = self._scene.addWidget(self._pixmap)

        self._wrapper = wrapper_type(self._proxy.pos(), filters, self._proxy, select=select)
        self._wrapper.mousePressEvent = select
        self._wrapper.mouseDoubleClickEvent = show_output
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

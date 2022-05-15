from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np


MAX_WRAPPERS = 5
INIT_Z = 10


class KernelWrapperFlat(QGraphicsItemGroup):
    def __init__(self, pos: QPointF, kernels: int, kernel: QGraphicsItem, active: int = 0, select=None):
        super().__init__()

        self._kernel_max = kernels
        self._kernel_num = min(kernels, MAX_WRAPPERS)
        self._kernel = kernel
        self.addToGroup(self._kernel)

        self._wrappers = np.empty(MAX_WRAPPERS, dtype=QGraphicsRectItem)
        for i in range(self._kernel_num):
            item = QGraphicsRectItem(self._kernel.boundingRect())
            item.setBrush(QBrush(QColor(255, 255, 255)))
            item.setPen(QPen(QBrush(QColor(0, 0, 0)), 2))
            item.setZValue(INIT_Z + i)
            item.setPos(pos + QPointF(10, 10) * float(i))

            self._wrappers[i] = item
            self.addToGroup(item)

        self._max_z = INIT_Z + self._kernel_num
        self._kernel.setZValue(self._max_z)
        self.set_active(active)

        self.mousePressEvent = select

    def set_active(self, number):
        for i in range(self._kernel_num):
            item = self._wrappers[i]
            item.setZValue(i)

        if self._kernel_num == self._kernel_max:
            pass
        else:
            side_size = np.floor(self._kernel_num / 2)

            if number < side_size:
                pass
            elif number >= self._kernel_max - side_size:
                number -= self._kernel_max - self._kernel_num
            else:
                number = np.floor(self._kernel_num / 2)
        number = int(number)

        self._wrappers[number].setZValue(self._max_z)
        self._kernel.setParentItem(self._wrappers[number])
        self._kernel.setPos(QPointF(0.0, 0.0))

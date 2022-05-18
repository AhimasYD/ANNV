from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np


MAX_WRAPPERS = 5
INIT_Z = 10

WRAPPER_3D_INDENT = 10


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


class KernelWrapperVolume(QGraphicsItemGroup):
    def __init__(self, pos: QPointF, kernels: int, kernel: QGraphicsItem, active: int = 0, select=None):
        super().__init__()

        self._kernel_max = kernels
        self._kernel_num = min(kernels, MAX_WRAPPERS)
        self._kernel = kernel
        self.addToGroup(self._kernel)

        self._wrappers = np.empty(self._kernel_num, dtype=QGraphicsRectItem)
        self._tops = np.empty(self._kernel_num, dtype=QGraphicsPolygonItem)
        self._lefts = np.empty(self._kernel_num, dtype=QGraphicsPolygonItem)

        for i in range(self._kernel_num):
            width = self._kernel.boundingRect().width()
            height = self._kernel.boundingRect().height()

            top_polygon = QPolygonF()
            top_polygon << pos + QPointF(10, 10) * float(i)
            top_polygon << pos + QPointF(width, 0) + QPointF(10, 10) * float(i)
            top_polygon << pos + QPointF(width, 0) + QPointF(WRAPPER_3D_INDENT, WRAPPER_3D_INDENT) + QPointF(10, 10) * float(i)
            top_polygon << pos + QPointF(WRAPPER_3D_INDENT, WRAPPER_3D_INDENT) + QPointF(10, 10) * float(i)
            top = QGraphicsPolygonItem(top_polygon)
            top.setBrush(QBrush(QColor(255, 255, 255)))
            top.setPen(QPen(QBrush(QColor(0, 0, 0)), 2))
            top.setZValue(INIT_Z + i)

            left_polygon = QPolygonF()
            left_polygon << pos + QPointF(10, 10) * float(i)
            left_polygon << pos + QPointF(WRAPPER_3D_INDENT, WRAPPER_3D_INDENT) + QPointF(10, 10) * float(i)
            left_polygon << pos + QPointF(0, height) + QPointF(WRAPPER_3D_INDENT, WRAPPER_3D_INDENT) + QPointF(10, 10) * float(i)
            left_polygon << pos + QPointF(0, height) + QPointF(10, 10) * float(i)
            left = QGraphicsPolygonItem(left_polygon)
            left.setBrush(QBrush(QColor(255, 255, 255)))
            left.setPen(QPen(QBrush(QColor(0, 0, 0)), 2))
            left.setZValue(INIT_Z + i)

            item = QGraphicsRectItem(self._kernel.boundingRect())
            item.setBrush(QBrush(QColor(255, 255, 255)))
            item.setPen(QPen(QBrush(QColor(0, 0, 0)), 2))
            item.setZValue(INIT_Z + i)
            item.setPos(QPointF(WRAPPER_3D_INDENT, WRAPPER_3D_INDENT) + pos + QPointF(10, 10) * float(i))

            self._wrappers[i] = item
            self._tops[i] = top
            self._lefts[i] = left
            self.addToGroup(item)
            self.addToGroup(top)
            self.addToGroup(left)

        self._max_z = INIT_Z + self._kernel_num
        self._kernel.setZValue(self._max_z)
        self.set_active(active)

        self.mousePressEvent = select

    def set_active(self, number):
        for i in range(self._kernel_num):
            self._wrappers[i].setZValue(i)
            self._tops[i].setZValue(i)
            self._lefts[i].setZValue(i)

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
        self._tops[number].setZValue(self._max_z)
        self._lefts[number].setZValue(self._max_z)

        self._kernel.setParentItem(self._wrappers[number])
        self._kernel.setPos(QPointF(0.0, 0.0))

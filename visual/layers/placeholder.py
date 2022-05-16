from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItemGroup
from PyQt5.QtGui import QBrush, QColor


class VPlaceholder(QGraphicsItemGroup):
    def __init__(self, side, margin, x, y):
        super().__init__()

        self._circle1 = QGraphicsEllipseItem(0, 0, side, side)
        self._circle2 = QGraphicsEllipseItem(0, 0 + margin + side, side, side)
        self._circle3 = QGraphicsEllipseItem(0, 0 + 2 * margin + 2 * side, side, side)

        self._circle1.setBrush(QBrush(QColor(0, 0, 0)))
        self._circle2.setBrush(QBrush(QColor(0, 0, 0)))
        self._circle3.setBrush(QBrush(QColor(0, 0, 0)))

        self._circle1.setZValue(10)
        self._circle2.setZValue(10)
        self._circle3.setZValue(10)

        self.addToGroup(self._circle1)
        self.addToGroup(self._circle2)
        self.addToGroup(self._circle3)

        self.setPos(x, y)

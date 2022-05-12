from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import math


class Arrow(QGraphicsItemGroup):
    def __init__(self, source: QPointF, destination: QPointF, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._sourcePoint = source
        self._destinationPoint = destination

        self._arrow_height = 20
        self._arrow_width = 12

        self._line = QGraphicsLineItem(QLineF(source, destination))
        self._cap = QGraphicsPolygonItem(self.cap_сalc(self._sourcePoint, self._destinationPoint))
        self._cap.setBrush(QBrush(QColor(255, 255, 255)))

        self.addToGroup(self._line)
        self.addToGroup(self._cap)

    # calculates the point where the arrow should be drawn
    def cap_сalc(self, start_point=None, end_point=None):
        try:
            startPoint, endPoint = start_point, end_point

            if start_point is None:
                startPoint = self._sourcePoint

            if endPoint is None:
                endPoint = self._destinationPoint

            dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()

            leng = math.sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / leng, dy / leng  # normalize

            # perpendicular vector
            perpX = -normY
            perpY = normX

            leftX = endPoint.x() + self._arrow_height * normX + self._arrow_width * perpX
            leftY = endPoint.y() + self._arrow_height * normY + self._arrow_width * perpY

            rightX = endPoint.x() + self._arrow_height * normX - self._arrow_width * perpX
            rightY = endPoint.y() + self._arrow_height * normY - self._arrow_width * perpY

            point2 = QPointF(leftX, leftY)
            point3 = QPointF(rightX, rightY)

            return QPolygonF([point2, endPoint, point3])

        except (ZeroDivisionError, Exception):
            return None

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import math


class Arrow(QGraphicsItemGroup):
    def __init__(self, source: QPointF, destination: QPointF):
        super().__init__()

        self._sourcePoint = source
        self._destinationPoint = destination

        self._arrow_height = 20
        self._arrow_width = 12

        self._line = QGraphicsLineItem(QLineF(source, destination))
        self._cap = QGraphicsPolygonItem(self.cap_calculation(self._sourcePoint, self._destinationPoint))
        self._cap.setBrush(QBrush(QColor(255, 255, 255)))

        self.addToGroup(self._line)
        self.addToGroup(self._cap)

    # calculates the point where the arrow should be drawn
    def cap_calculation(self, start_point, end_point):
        try:
            dx, dy = start_point.x() - end_point.x(), start_point.y() - end_point.y()

            length = math.sqrt(dx ** 2 + dy ** 2)
            norm_x, norm_y = dx / length, dy / length  # normalize

            # perpendicular vector
            perp_x = -norm_y
            perp_y = norm_x

            left_x = end_point.x() + self._arrow_height * norm_x + self._arrow_width * perp_x
            left_y = end_point.y() + self._arrow_height * norm_y + self._arrow_width * perp_y

            right_x = end_point.x() + self._arrow_height * norm_x - self._arrow_width * perp_x
            right_y = end_point.y() + self._arrow_height * norm_y - self._arrow_width * perp_y

            point2 = QPointF(left_x, left_y)
            point3 = QPointF(right_x, right_y)

            return QPolygonF([point2, end_point, point3])

        except (ZeroDivisionError, Exception):
            return None

from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsItemGroup
from PyQt5.QtGui import QColor, QBrush, QPolygonF, QPen
from PyQt5.QtCore import QPointF, QLineF, Qt

from math import sqrt


LINE_WIDTH = 2.0
LINE_WIDTH_MIN = 1.0
LINE_WIDTH_MAX = 3.0

ARROW_HEIGHT = 24
ARROW_WIDTH = 12


class Arrow(QGraphicsItemGroup):
    def __init__(self, source: QPointF, destination: QPointF):
        super().__init__()

        self._sourcePoint = source
        self._destinationPoint = destination

        self._line = QGraphicsLineItem(QLineF(source, destination))
        self._line.setZValue(0)

        self._cap = QGraphicsPolygonItem(self._cap_calculation(self._sourcePoint, self._destinationPoint))
        self._cap.setBrush(QBrush(QColor(255, 255, 255)))
        self._cap.setZValue(0)

        self.reset_width()
        self.reset_color()

        self.addToGroup(self._line)
        self.addToGroup(self._cap)

    # calculates the point where the arrow should be drawn
    @staticmethod
    def _cap_calculation(start_point: QPointF, end_point: QPointF):
        try:
            dx, dy = start_point.x() - end_point.x(), start_point.y() - end_point.y()

            length = sqrt(dx ** 2 + dy ** 2)
            norm_x, norm_y = dx / length, dy / length  # normalize

            # perpendicular vector
            perp_x = -norm_y
            perp_y = norm_x

            left_x = end_point.x() + ARROW_HEIGHT * norm_x + ARROW_WIDTH * perp_x
            left_y = end_point.y() + ARROW_HEIGHT * norm_y + ARROW_WIDTH * perp_y

            right_x = end_point.x() + ARROW_HEIGHT * norm_x - ARROW_WIDTH * perp_x
            right_y = end_point.y() + ARROW_HEIGHT * norm_y - ARROW_WIDTH * perp_y

            point2 = QPointF(left_x, left_y)
            point3 = QPointF(right_x, right_y)

            return QPolygonF([point2, end_point, point3])

        except (ZeroDivisionError, Exception):
            return None

    def reset_width(self):
        brush = self._line.pen().brush()
        self._line.setPen(QPen(brush, LINE_WIDTH_MIN))
        self._line.setPen(QPen(brush, LINE_WIDTH_MIN))

    def set_width(self, factor: float):
        if factor < 0 or factor > 1:
            raise ValueError

        width = LINE_WIDTH_MAX * factor
        width = max(LINE_WIDTH_MIN, width)

        brush = self._line.pen().brush()
        self._line.setPen(QPen(brush, width))
        self._line.setPen(QPen(brush, width))

    def reset_color(self):
        width = self._line.pen().width()
        self._line.setPen(QPen(QBrush(QColor(0, 0, 0)), width))
        self._line.setPen(QPen(QBrush(QColor(0, 0, 0)), width))

    def set_color(self, factor: float):
        if abs(factor) > 1:
            raise ValueError

        alpha = abs(int(255 * factor))
        if factor >= 0:
            brush = QBrush(QColor(255, 0, 0, alpha))
        else:
            brush = QBrush(QColor(0, 0, 255, alpha))

        width = self._line.pen().width()
        self._line.setPen(QPen(brush, width))
        self._cap.setBrush(brush)
        self._cap.setPen(QPen(brush, width))

    def set_dashed(self):
        pen = self._line.pen()
        pen.setStyle(Qt.PenStyle.DashLine)
        self._line.setPen(pen)

        pen = self._cap.pen()
        pen.setStyle(Qt.PenStyle.DashLine)
        self._cap.setPen(pen)

    def set_tooltip(self, tooltip):
        self._line.setToolTip(tooltip)
        self._cap.setToolTip(tooltip)

    def hide(self):
        self._line.hide()
        self._cap.hide()

    def show(self):
        self._line.show()
        self._cap.show()

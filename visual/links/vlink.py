from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .arrow import Arrow
from visual.constants import WeightColor, WeightThick


class VLink(QGraphicsLineItem):
    def __init__(self, start, end, color=WeightColor.OFF, thick=WeightThick.OFF):
        super().__init__()
        self._arrow = Arrow(start, end)

        self._weight = None
        self._maximum = None

        self._color = color
        self._thick = thick

    def get_item(self):
        return self._arrow

    def set_weight(self, weight, maximum):
        self._weight = weight
        self._maximum = maximum

        self.update_arrow()

    def update_arrow(self):
        if self._weight is None or self._maximum is None:
            return

        factor = self._weight / self._maximum
        if self._color == WeightColor.ON:
            self._arrow.set_color(factor)
        if self._thick == WeightThick.ON:
            self._arrow.set_width(abs(factor))

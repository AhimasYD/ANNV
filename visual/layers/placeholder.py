from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from visual.functions import *


class VPlaceholder(QGraphicsItemGroup):
    def __init__(self, side, margin, x, y):
        super().__init__()

        _circle1 = draw_ellipse(x, y - margin - side, side, side)
        _circle2 = draw_ellipse(x, y, side, side)
        _circle3 = draw_ellipse(x, y + margin + side, side, side)

        self.addToGroup(_circle1)
        self.addToGroup(_circle2)
        self.addToGroup(_circle3)

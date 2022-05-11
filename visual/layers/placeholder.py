from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from visual.functions import *


class VPlaceholder(QGraphicsItemGroup):
    def __init__(self, side, margin, x, y):
        super().__init__()

        circle1 = draw_ellipse(x, y - margin - side, side, side)
        circle2 = draw_ellipse(x, y, side, side)
        circle3 = draw_ellipse(x, y + margin + side, side, side)

        self.addToGroup(circle1)
        self.addToGroup(circle2)
        self.addToGroup(circle3)

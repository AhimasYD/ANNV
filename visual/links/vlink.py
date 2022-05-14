from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .arrow import Arrow


class VLink(QGraphicsLineItem):
    def __init__(self, start, end, type):
        super().__init__()
        self._item = Arrow(start, end)

    def get_item(self):
        return self._item

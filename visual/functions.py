from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .constants import *


def draw_rect(x, y, width, height):
    item = QGraphicsRectItem(x - width/2, y - height/2, width, height)
    item.setZValue(50)
    return item


def draw_text(text, rect, names):
    item = QGraphicsTextItem()
    item.setFont(QFont('OldEnglish', 30, QFont.Bold))

    if names == Names.HORIZONTAL:
        item.setPlainText(text)
        bound = item.boundingRect()
        item.setRotation(-90)
        item.setPos(
            - bound.x() + rect.x() + rect.width()/2 - bound.height()/2,
            - bound.y() + rect.y() + bound.width() + rect.height()/2 - bound.width()/2
        )
    elif names == Names.VERTICAL:
        text = '\n'.join(list(text))
        item.setPlainText(text)
        bound = item.boundingRect()
        item.setPos(
            - bound.x() + rect.x() + rect.width() / 2 - bound.width() / 2,
            - bound.y() + rect.y() + rect.height() / 2 - bound.height() / 2
        )

    return item


def clear_layout(layout):
    while layout and layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

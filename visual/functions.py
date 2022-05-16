from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .constants import *


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


def brush_by_factor(factor):
    alpha = abs(int(255 * factor))
    if factor >= 0:
        brush = QBrush(QColor(255, 0, 0, alpha))
    else:
        brush = QBrush(QColor(0, 0, 255, alpha))
    return brush


def clear_layout(layout):
    while layout and layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

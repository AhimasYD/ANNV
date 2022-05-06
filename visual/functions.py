from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from enum import Enum, auto
from .constants import *


def draw_rect(x, y, width, height):
    return QGraphicsRectItem(x - width/2, y - height/2, width, height)


def draw_ellipse(x, y, width, height):
    return QGraphicsEllipseItem(x - width/2, y - height/2, width, height)


def draw_text(text, rect, names=None):
    item = QGraphicsTextItem(text)
    item.setFont(QFont('OldEnglish', 30, QFont.Light))

    bound = item.boundingRect()
    item.setRotation(-90)
    item.setPos(
        - bound.x() + rect.x() + rect.width()/2 - bound.height()/2,
        - bound.y() + rect.y() + bound.width() + rect.height()/2 - bound.width()/2
    )

    return item


def clear_layout(layout):
    while layout and layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

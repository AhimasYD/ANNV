from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from visual.constants import Names
from visual.trivia.hintskeeper import HintsKeeper


def draw_text(text, rect, names):
    if HintsKeeper().names == Names.HORIZONTAL:
        font_size = 30
    else:
        font_size = 20

    item = QGraphicsTextItem()
    item.setFont(QFont('OldEnglish', font_size, QFont.Bold))

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
    try:
        alpha = abs(int(255 * factor))
    except ValueError:
        alpha = 0
    if factor >= 0:
        brush = QBrush(QColor(255, 0, 0, alpha))
    else:
        brush = QBrush(QColor(0, 0, 255, alpha))
    return brush

from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QFont
from visual.constants import Names


def draw_text(text, rect, names):
    if names == Names.HORIZONTAL:
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

from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import QPointF

import numpy as np

from visual.constants import *
from visual.functions import draw_text

from visual.links import VLink

from visual.hintskeeper import HintsKeeper


class VBlock:
    def __init__(self, scene, x, select, show_output, name):
        self._scene = scene

        self._rect = QGraphicsRectItem(x, 0 - BLOCK_HEIGHT / 2, BLOCK_WIDTH, BLOCK_HEIGHT)
        self._rect.mousePressEvent = select
        self._rect.mouseDoubleClickEvent = show_output
        self._text = draw_text(name, self._rect.boundingRect(), HintsKeeper().names)
        self._scene.addItem(self._rect)
        self._scene.addItem(self._text)

        self._bind_in = QPointF(x, 0)
        self._bind_out = QPointF(x + BLOCK_WIDTH, 0)

        self._links_in = None
        self._links_out = None

    def bind_in(self):
        return self._bind_in

    def bind_out(self):
        return self._bind_out

    def set_links_in(self, links):
        self._links_in = links

    def set_links_out(self, links):
        self._links_out = links

    def bounding(self):
        return self._rect.boundingRect()

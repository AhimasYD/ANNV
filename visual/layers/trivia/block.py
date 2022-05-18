from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import QPointF

from visual.trivia import HintsKeeper
from visual.layers.constants import BLOCK_HEIGHT, BLOCK_WIDTH
from visual.layers.functions import draw_text


class VBlock:
    def __init__(self, scene, x, select, show_output, name):
        self._scene = scene
        self._name = name

        self._rect = QGraphicsRectItem(x, 0 - BLOCK_HEIGHT / 2, BLOCK_WIDTH, BLOCK_HEIGHT)
        self._rect.mousePressEvent = select
        self._rect.mouseDoubleClickEvent = show_output
        self._scene.addItem(self._rect)

        self._text = None
        self.update_name(HintsKeeper().names)
        HintsKeeper().attach_names(self.update_name)

        self._bind_in = QPointF(x, 0)
        self._bind_out = QPointF(x + BLOCK_WIDTH, 0)

        self._links_in = None
        self._links_out = None

    def __del__(self):
        HintsKeeper().detach_names(self.update_name)

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

    def update_name(self, value):
        if self._text is not None:
            self._scene.removeItem(self._text)
            self._text = None
        self._text = draw_text(self._name, self._rect.boundingRect(), value)
        self._scene.addItem(self._text)

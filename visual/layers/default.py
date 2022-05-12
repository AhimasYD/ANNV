from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer


class VDefault(VLayer):
    def __init__(self, logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume)
        self._block = VDefaultBlock(self._scene, self._x, self._logic.name, self.select, self._o_names)

    def select(self, event):
        super().select(event)


class VDefaultBlock:
    def __init__(self, scene, x, name, callback, opt_names):
        self._scene = scene

        self._rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self._rect.mousePressEvent = callback
        self._text = draw_text(name + ' (D)', self._rect.boundingRect(), opt_names)
        self._scene.addItem(self._rect)
        self._scene.addItem(self._text)

        self._bind_in = QPointF(x - BLOCK_WIDTH / 2, 0)
        self._bind_out = QPointF(x + BLOCK_WIDTH / 2, 0)

    def bind_in(self):
        return self._bind_in

    def bind_out(self):
        return self._bind_out

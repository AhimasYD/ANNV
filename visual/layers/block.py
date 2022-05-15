from PyQt5.QtCore import QPointF

import numpy as np

from visual.constants import *
from visual.functions import draw_rect, draw_text
from visual.links import VLink


class VBlock:
    def __init__(self, scene, x, select, opt_names, name):
        self._scene = scene

        self._rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self._rect.mousePressEvent = select
        self._text = draw_text(name, self._rect.boundingRect(), opt_names)
        self._scene.addItem(self._rect)
        self._scene.addItem(self._text)

        self._bind_in = QPointF(x - BLOCK_WIDTH / 2, 0)
        self._bind_out = QPointF(x + BLOCK_WIDTH / 2, 0)

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

    def set_weight_color_hint(self, hint: WeightColor, forward: bool = False):
        if self._links_in is None:
            return

        if type(self._links_in) is VLink:
            self._links_in.set_color_hint(hint)
        elif type(self._links_in) is np.ndarray:
            for i in range(self._links_in.shape[0]):
                link = self._links_in[i]
                if link is None:
                    continue
                link.set_color_hint(hint)

        if not forward or self._links_out is None:
            return

        if type(self._links_out) is VLink:
            self._links_out.set_color_hint(hint)
        elif type(self._links_out) is np.ndarray:
            for i in range(self._links_out.shape[0]):
                link = self._links_out[i]
                if link is None:
                    continue
                link.set_color_hint(hint)

    def set_weight_thick_hint(self, hint: WeightThick, forward: bool = False):
        if self._links_in is None:
            return

        if type(self._links_in) is VLink:
            self._links_in.set_thick_hint(hint)
        elif type(self._links_in) is np.ndarray:
            for i in range(self._links_in.shape[0]):
                link = self._links_in[i]
                if link is None:
                    continue
                link.set_thick_hint(hint)

        if not forward or self._links_out is None:
            return

        if type(self._links_out) is VLink:
            self._links_out.set_thick_hint(hint)
        elif type(self._links_out) is np.ndarray:
            for i in range(self._links_out.shape[0]):
                link = self._links_out[i]
                if link is None:
                    continue
                link.set_thick_hint(hint)
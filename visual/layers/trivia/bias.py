from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtCore import QPointF

from visual.constants import Bias, BIAS_BRUSH, BIAS_SIDE, BIAS_MARGIN
from visual.trivia.hintskeeper import HintsKeeper


class VBiasNeuron:
    def __init__(self, scene, l_bound):
        self._scene = scene

        side = BIAS_SIDE
        x = l_bound.x() + l_bound.width() / 2 - side / 2
        y = l_bound.y() - BIAS_MARGIN - BIAS_SIDE

        self._item = QGraphicsEllipseItem(x, y, side, side)
        self._item.setBrush(BIAS_BRUSH)
        self._item.setZValue(10)
        self._scene.addItem(self._item)

        self._bind_out = QPointF(x + side, y + side / 2)
        self._links_out = None

        HintsKeeper().attach_bias(self.set_bias_hint)
        self.set_bias_hint(HintsKeeper().bias)

    def bind_out(self):
        return self._bind_out

    def set_links_out(self, links):
        self._links_out = links

    def set_bias_hint(self, hint):
        if hint == Bias.ON:
            self._item.show()
        else:
            self._item.hide()

    def bounding(self):
        return self._item.boundingRect()

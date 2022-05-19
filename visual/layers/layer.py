from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QFont

from abc import ABCMeta, abstractmethod

from weak import WeakMethod
from visual.widgets.functions import clear_layout
from visual.constants import Captions
from visual.layers.constants import CAPTION_MARGIN
from visual.trivia import HintsKeeper


class VLayer(metaclass=ABCMeta):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        self._logic = logic
        self._scene = scene
        self._x = x
        self._w_info = w_info
        self._w_flat = w_flat
        self._w_volume = w_volume

        self._connection = None

    def __del__(self):
        HintsKeeper().detach_captions(self._captions_callback)

    def select(self, event):
        clear_layout(self._w_info.layout())

        self._w_flat.hide()
        self._w_volume.hide()

        self._w_flat.button_prev.mousePressEvent = None
        self._w_flat.button_next.mousePressEvent = None

        self._w_volume.button_0_prev.mousePressEvent = None
        self._w_volume.button_0_next.mousePressEvent = None
        self._w_volume.button_1_prev.mousePressEvent = None
        self._w_volume.button_1_next.mousePressEvent = None

    def _init_caption(self):
        self._caption = QGraphicsTextItem(str(self._logic.output_shape))
        self._caption.setFont(QFont('OldEnglish', 14, QFont.Medium))
        l_bound = self.bounding()
        x = l_bound.x() + l_bound.width() / 2 - self._caption.boundingRect().width() / 2
        y = l_bound.y() + l_bound.height() + CAPTION_MARGIN
        self._caption.setPos(x, y)
        self._scene.addItem(self._caption)

        self._captions_callback = WeakMethod(self, VLayer.update_caption)
        HintsKeeper().attach_captions(self._captions_callback)
        self.update_caption(HintsKeeper().captions)

    def update_caption(self, value):
        if value == Captions.ON:
            self._caption.show()
        else:
            self._caption.hide()

    def set_bias(self, bounding):
        pass

    @abstractmethod
    def binds_in(self):
        """"""

    @abstractmethod
    def binds_out(self):
        """"""

    @abstractmethod
    def set_links_in(self, links):
        """"""

    @abstractmethod
    def set_links_out(self, links):
        """"""

    @abstractmethod
    def bounding(self):
        """"""

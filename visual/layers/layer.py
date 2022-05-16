from abc import ABCMeta, abstractmethod

from visual.functions import clear_layout


class VLayer(metaclass=ABCMeta):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        self._logic = logic
        self._scene = scene
        self._x = x
        self._w_info = w_info
        self._w_flat = w_flat
        self._w_volume = w_volume

        self._connection = None

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
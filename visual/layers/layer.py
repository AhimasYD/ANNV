from abc import ABCMeta, abstractmethod, abstractproperty

from visual.functions import clear_layout


class VLayer:
    def __init__(self, logic, scene, x, o_display, o_color, o_thick, o_names, o_captions, o_bias, w_info, w_flat, w_volume):
        self._logic = logic
        self._scene = scene
        self._x = x
        self._o_display = o_display
        self._o_color = o_color
        self._o_thick = o_thick
        self._o_names = o_names
        self._o_captions = o_captions
        self._o_bias = o_bias
        self._w_info = w_info
        self._w_flat = w_flat
        self._w_volume = w_volume

    def select(self, event):
        clear_layout(self._w_info.layout())

        self._w_flat.hide()
        self._w_volume.hide()

        self._w_flat.filter_prev.mousePressEvent = None
        self._w_flat.filter_next.mousePressEvent = None

        self._w_volume.filter_prev.mousePressEvent = None
        self._w_volume.filter_next.mousePressEvent = None
        self._w_volume.depth_prev.mousePressEvent = None
        self._w_volume.depth_next.mousePressEvent = None

    @abstractmethod
    def set_links_in(self, links):
        """"""

    @abstractmethod
    def set_links_out(self, links):
        """"""

from weak import WeakMethod
from visual.functions import brush_by_factor
from visual.trivia import HintsKeeper
from visual.constants import Activation


class VNeuron:
    def __init__(self, scene):
        self._scene = scene

        self._item = None

        self._bind_in = None
        self._bind_out = None

        self._links_in = None
        self._links_out = None
        self._links_bias = None

        self._brush = brush_by_factor(0.0, 1.0)

        self._activation_callback = WeakMethod(self, VNeuron.update_activation)
        HintsKeeper().attach_activation(self._activation_callback)

    def __del__(self):
        HintsKeeper().detach_activation(self._activation_callback)

    def set_output(self, value, maximum):
        self._brush = brush_by_factor(value, maximum)
        if HintsKeeper().activation:
            self._item.setBrush(self._brush)

    def update_activation(self, value):
        if value == Activation.ON:
            self._item.setBrush(self._brush)
        else:
            self._item.setBrush(brush_by_factor(0.0, 1.0))

    def bind_in(self):
        return self._bind_in

    def bind_out(self):
        return self._bind_out

    def set_links_in(self, links, weights):
        self._links_in = links

    def set_links_out(self, links):
        self._links_out = links

    def set_link_bias(self, link):
        self._links_bias = link

    def bounding(self):
        return self._item.boundingRect()

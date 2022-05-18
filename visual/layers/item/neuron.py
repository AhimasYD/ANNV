from visual.functions import brush_by_factor


class VNeuron:
    def __init__(self, scene):
        self._scene = scene

        self._item = None

        self._bind_in = None
        self._bind_out = None

        self._links_in = None
        self._links_out = None
        self._links_bias = None

    def set_output(self, value, factor):
        self._item.setBrush(brush_by_factor(factor))

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

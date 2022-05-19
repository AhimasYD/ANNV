from visual.links import LinkType

from weak import WeakMethod
from visual.layers.layer import VLayer
from visual.layers.trivia import VBlock


class VEmbedding(VLayer):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, w_info, w_flat, w_volume)
        self._select_callback = WeakMethod(self, VEmbedding.select)
        self._block = VEmbeddingBlock(self._scene, self._x, self._select_callback)
        self._init_caption()

    def __del__(self):
        super().__del__()

    def select(self, event):
        super().select(event)

    def binds_in(self):
        return LinkType.UNITED, self._block.bind_in()

    def binds_out(self):
        return LinkType.UNITED, self._block.bind_out()

    def set_links_in(self, links):
        self._block.set_links_in(links)

    def set_links_out(self, links):
        self._block.set_links_out(links)

    def bounding(self):
        return self._block.bounding()


class VEmbeddingBlock(VBlock):
    def __init__(self, scene, x, select):
        super().__init__(scene, x, select, None, 'Embedding')

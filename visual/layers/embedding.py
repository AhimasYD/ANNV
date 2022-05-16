from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer
from visual.links import VLink
from visual.layers.block import VBlock

from visual.hintskeeper import HintsKeeper


class VEmbedding(VLayer):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, w_info, w_flat, w_volume)
        self._block = VEmbeddingBlock(self._scene, self._x, self.select)

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

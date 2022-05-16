from abc import abstractmethod

from visual.constants import *
from visual.layers.layer import VLayer

from visual.hintskeeper import HintsKeeper


class VConv(VLayer):
    def __init__(self, logic, scene, x, w_info, w_flat, w_volume):
        super().__init__(logic, scene, x, w_info, w_flat, w_volume)

        self._filter = 0
        self._block = None
        self._kernel_ctrl = None
        self._kernels = None

    @abstractmethod
    def update(self):
        """"""

    def filter_prev(self, event):
        if self._filter - 1 >= 0:
            self._filter -= 1
            self.update()

    def filter_next(self, event):
        if self._filter + 1 < self._logic.filter_num:
            self._filter += 1
            self.update()

    def binds_in(self):
        if HintsKeeper().display == Display.COMPACT:
            return self._connection, self._block.bind_in()
        else:
            return self._connection, self._kernel_ctrl.bind_in()

    def binds_out(self):
        if HintsKeeper().display == Display.COMPACT:
            return self._connection, self._block.bind_out()
        else:
            return self._connection, self._kernel_ctrl.bind_out()

    def set_links_in(self, links):
        if HintsKeeper().display == Display.COMPACT:
            self._block.set_links_in(links)
        else:
            self._kernel_ctrl.set_links_in(links)

    def set_links_out(self, links):
        if HintsKeeper().display == Display.COMPACT:
            self._block.set_links_out(links)
        else:
            self._kernel_ctrl.set_links_out(links)

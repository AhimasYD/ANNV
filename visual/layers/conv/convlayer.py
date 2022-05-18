from abc import abstractmethod

from widgets.outputwindow import OutputWindow
from visual.constants import Display
from visual.trivia.hintskeeper import HintsKeeper
from visual.layers.layer import VLayer


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

    def show_output(self, event):
        if self._logic.output is None:
            return
        self._window = OutputWindow(self._logic.output)
        self._window.setModal(True)
        self._window.showMaximized()

    def bounding(self):
        if HintsKeeper().display == Display.COMPACT:
            return self._block.bounding()
        else:
            return self._kernel_ctrl.bounding()

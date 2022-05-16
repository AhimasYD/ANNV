from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from flatblock import FlatBlock
from volumeblock import VolumeBlock
from visual.pixmap import Pixmap
from visual.constants import PIXMAP_SIDE


class OutputWindow(QDialog):
    def __init__(self, array):
        super().__init__()
        self._init_ui()

        self._array = array
        self._channel = 0
        self._depth = 0

        self._pixmap = None

        if len(self._array.shape) <= 2:
            self._layout_inner.addWidget(QLabel('Output:'))
            self._pixmap = Pixmap(array, PIXMAP_SIDE, hv=True, hh=True, sb=True)
            self._layout_inner.addWidget(self._pixmap)
            self._layout_inner.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        elif len(self._array.shape) == 3:
            self._layout_inner.addWidget(QLabel('Output:'))
            self._pixmap = Pixmap(array[self._channel], PIXMAP_SIDE, hv=True, hh=True, sb=True)
            self._layout_inner.addWidget(self._pixmap)
            self._layout_inner.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            self._flat.num.setText(f'{self._channel}')
            self._flat.show()
        elif len(self._array.shape) == 4:
            self._layout_inner.addWidget(QLabel('Output:'))
            self._pixmap = Pixmap(array[self._channel][self._depth], PIXMAP_SIDE, hv=True, hh=True, sb=True)
            self._layout_inner.addWidget(self._pixmap)
            self._layout_inner.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            self._volume.num_0.setText(f'{self._channel}')
            self._volume.num_1.setText(f'{self._depth}')
            self._volume.show()

    def _init_ui(self):
        self._layout_inner = QVBoxLayout()

        inner = QWidget()
        inner.setLayout(self._layout_inner)

        scroll = QScrollArea()
        scroll.setWidget(inner)
        scroll.setWidgetResizable(True)

        layout_pixmap = QVBoxLayout()
        layout_pixmap.addWidget(scroll)

        widget_pixmap = QWidget()
        widget_pixmap.setLayout(layout_pixmap)

        self._flat = FlatBlock('Channel')
        self._volume = VolumeBlock('Channel', 'Depth')

        layout = QVBoxLayout()
        layout.addWidget(widget_pixmap)
        layout.addWidget(self._flat)
        layout.addWidget(self._volume)
        self.setLayout(layout)

        self._flat.button_prev.mousePressEvent = self.channel_prev
        self._flat.button_next.mousePressEvent = self.channel_next

        self._flat.hide()
        self._volume.hide()

    def _init_pixmap_ui(self):
        inner_layout = QVBoxLayout()

        inner = QWidget()
        inner.setLayout(inner_layout)

        scroll = QScrollArea()
        scroll.setWidget(inner)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

    def channel_prev(self, event):
        if self._channel - 1 >= 0:
            self._channel -= 1
            self.update_pixmap()

    def channel_next(self, event):
        print('HERE')
        if self._channel + 1 < self._array.shape[0]:
            self._channel += 1
            self.update_pixmap()

    def depth_prev(self, event):
        if self._depth - 1 >= 0:
            self._depth -= 1
            self.update_pixmap()

    def depth_next(self, event):
        if self._depth + 1 < self._array.shape[0]:
            self._depth += 1
            self.update_pixmap()

    def update_pixmap(self):
        array = self._array
        if len(self._array.shape) <= 2:
            self._pixmap.update(array)
        elif len(self._array.shape) == 3:
            self._pixmap.update(array[self._channel])
            self._flat.num.setText(f'{self._channel}')
        elif len(self._array.shape) == 4:
            self._pixmap.update(array[self._channel][self._depth])
            self._volume.num_0.setText(f'{self._channel}')
            self._volume.num_1.setText(f'{self._depth}')

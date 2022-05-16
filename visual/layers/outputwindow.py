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

        self._layout_inner.addWidget(QLabel('Output:'))
        self._layout_inner.addWidget(Pixmap(array, PIXMAP_SIDE, hv=True, hh=True, sb=True))
        self._layout_inner.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

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

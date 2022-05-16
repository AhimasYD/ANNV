from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class OutputWindow(QDialog):
    def __init__(self, array):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self._init_buttons_ui()

        layout = QVBoxLayout()
        layout.addWidget(self._button_widget)
        self.setLayout(layout)

    def _init_pixmap_ui(self):
        inner_layout = QVBoxLayout()

        inner = QWidget()
        inner.setLayout(inner_layout)

        scroll = QScrollArea()
        scroll.setWidget(inner)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

    def _init_buttons_ui(self):
        button_prev = QPushButton('Prev')
        button_next = QPushButton('Next')

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(button_prev)
        layout_buttons.addWidget(button_next)

        label = QLabel('Depth:')
        num = QLabel('#')

        layout_text = QHBoxLayout()
        layout_text.addWidget(label)
        layout_text.addWidget(num)
        layout_text.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        layout = QVBoxLayout()
        layout.addLayout(layout_text)
        layout.addLayout(layout_buttons)

        self._button_widget = QWidget()
        self._button_widget.setLayout(layout)

        self._depth_prev = button_prev
        self._depth_next = button_next
        self._depth_num = num

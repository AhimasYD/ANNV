from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class VolumeBlock(QWidget):
    def __init__(self, name_0, name_1):
        super().__init__()

        button_0_prev = QPushButton('Prev')
        button_0_next = QPushButton('Next')

        layout_buttons_0 = QHBoxLayout()
        layout_buttons_0.addWidget(button_0_prev)
        layout_buttons_0.addWidget(button_0_next)

        label_0 = QLabel(f'{name_0}:')
        num_0 = QLabel('#')

        layout_0_text = QHBoxLayout()
        layout_0_text.addWidget(label_0)
        layout_0_text.addWidget(num_0)
        layout_0_text.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        layout_0 = QVBoxLayout()
        layout_0.addLayout(layout_0_text)
        layout_0.addLayout(layout_buttons_0)

        button_1_prev = QPushButton('Prev')
        button_1_next = QPushButton('Next')

        layout_buttons_1 = QHBoxLayout()
        layout_buttons_1.addWidget(button_1_prev)
        layout_buttons_1.addWidget(button_1_next)

        label_1 = QLabel(f'{name_1}:')
        num_1 = QLabel('#')

        layout_1_text = QHBoxLayout()
        layout_1_text.addWidget(label_1)
        layout_1_text.addWidget(num_1)
        layout_1_text.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        layout_1 = QVBoxLayout()
        layout_1.addLayout(layout_1_text)
        layout_1.addLayout(layout_buttons_1)

        layout = QHBoxLayout()
        layout.addLayout(layout_0)
        layout.addLayout(layout_1)

        self.setLayout(layout)

        self.button_0_prev = button_0_prev
        self.button_0_next = button_0_next
        self.button_1_prev = button_1_prev
        self.button_1_next = button_1_next

        self.num_0 = num_0
        self.num_1 = num_1

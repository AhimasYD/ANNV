from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class FlatBlock(QWidget):
    def __init__(self):
        super().__init__()

        button_prev = QPushButton('Prev')
        button_next = QPushButton('Next')

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(button_prev)
        layout_buttons.addWidget(button_next)

        label = QLabel('Filter:')
        num = QLabel('#')

        layout_text = QHBoxLayout()
        layout_text.addWidget(label)
        layout_text.addWidget(num)
        layout_text.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        layout = QVBoxLayout()
        layout.addLayout(layout_text)
        layout.addLayout(layout_buttons)

        self.setLayout(layout)

        self.filter_prev = button_prev
        self.filter_next = button_next
        self.filter_num = num

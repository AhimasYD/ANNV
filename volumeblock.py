from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class VolumeBlock(QWidget):
    def __init__(self):
        super().__init__()

        filter_button_prev = QPushButton('Prev')
        filter_button_next = QPushButton('Next')

        layout_filter_buttons = QHBoxLayout()
        layout_filter_buttons.addWidget(filter_button_prev)
        layout_filter_buttons.addWidget(filter_button_next)

        filter_label = QLabel('Filter:')
        filter_num = QLabel('#')

        layout_filter_text = QHBoxLayout()
        layout_filter_text.addWidget(filter_label)
        layout_filter_text.addWidget(filter_num)
        layout_filter_text.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        layout_filter = QVBoxLayout()
        layout_filter.addLayout(layout_filter_text)
        layout_filter.addLayout(layout_filter_buttons)

        depth_button_prev = QPushButton('Prev')
        depth_button_next = QPushButton('Next')

        layout_depth_buttons = QHBoxLayout()
        layout_depth_buttons.addWidget(depth_button_prev)
        layout_depth_buttons.addWidget(depth_button_next)

        depth_label = QLabel('Depth:')
        depth_num = QLabel('#')

        layout_depth_text = QHBoxLayout()
        layout_depth_text.addWidget(depth_label)
        layout_depth_text.addWidget(depth_num)
        layout_depth_text.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored))

        layout_depth = QVBoxLayout()
        layout_depth.addLayout(layout_depth_text)
        layout_depth.addLayout(layout_depth_buttons)

        layout = QHBoxLayout()
        layout.addLayout(layout_filter)
        layout.addLayout(layout_depth)

        self.setLayout(layout)

        self.filter_prev = filter_button_prev
        self.filter_next = filter_button_next
        self.depth_prev = depth_button_prev
        self.depth_next = depth_button_next

        self.filter_num = filter_num
        self.depth_num = depth_num

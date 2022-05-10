from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *

from visual.functions import *
from visual.pixmap import Pixmap
from .layer import VLayer


class VEmbedding(VLayer):
    def __init__(self, logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions,
                 opt_bias, widget, flat, volume):
        super().__init__(logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias,
                         widget, flat, volume)

        self.block = VEmbeddingBlock(self.scene, self.pos_x, self.select)

    def select(self, event):
        super().select(event)

        layout = self.widget.layout()
        clear_layout(layout)


class VEmbeddingBlock:
    def __init__(self, scene, x, callback):
        self.scene = scene

        self.rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.bound = self.rect.boundingRect()
        self.text = draw_text('Embedding', self.bound)

        self.scene.addItem(self.rect)
        self.scene.addItem(self.text)

        self.rect.mousePressEvent = callback

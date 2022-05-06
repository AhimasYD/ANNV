from logic.layers import *
from .layer import VLayer
from .constants import *
from .functions import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class VEmbedding(VLayer):
    def __init__(self, logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias, widget):
        super().__init__(logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias, widget)

        self.block = VEmbeddingBlock(self.scene, self.pos_x)


class VEmbeddingBlock:
    def __init__(self, scene, x):
        self.scene = scene

        self.rect = draw_rect(x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.bound = self.rect.boundingRect()
        self.text = draw_text('Embedding', self.bound)

        self.scene.addItem(self.rect)
        self.scene.addItem(self.text)

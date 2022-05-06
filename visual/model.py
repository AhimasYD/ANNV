from .constants import *
from .layers import *


class VModel:
    def __init__(self, logic, scene, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias, widget):
        self.logic = logic
        self.scene = scene

        self.opt_display = opt_display
        self.opt_weight_color = opt_weight_color
        self.opt_weight_thick = opt_weight_thick
        self.opt_names = opt_names
        self.opt_captions = opt_captions
        self.opt_bias = opt_bias

        self.widget = widget

        self.x = 0

        self.layers = []
        for l_layer in logic.layers:
            if type(l_layer).__name__ == 'LDense':
                layer = VDense(l_layer, self.scene, self.x,
                               self.opt_display, self.opt_weight_color, self.opt_weight_thick,
                               self.opt_names, self.opt_captions, self.opt_bias, self.widget)

            elif type(l_layer).__name__ == 'LEmbedding':
                layer = VEmbedding(l_layer, self.scene, self.x,
                                   self.opt_display, self.opt_weight_color, self.opt_weight_thick,
                                   self.opt_names, self.opt_captions, self.opt_bias, self.widget)
            else:
                layer = VDefault(l_layer, self.scene, self.x,
                                 self.opt_display, self.opt_weight_color, self.opt_weight_thick,
                                 self.opt_names, self.opt_captions, self.opt_bias, self.widget)

            self.layers.append(layer)
            self.x = self.scene.width() + LAYER_MARGIN

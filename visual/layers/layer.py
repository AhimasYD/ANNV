class VLayer:
    def __init__(self, logic, scene, pos_x, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias,
                 widget, flat, volume):
        self.logic = logic
        self.scene = scene
        self.pos_x = pos_x
        self.opt_display = opt_display
        self.opt_weight_color = opt_weight_color
        self.opt_weight_thick = opt_weight_thick
        self.opt_names = opt_names
        self.opt_captions = opt_captions
        self.opt_bias = opt_bias
        self.widget = widget
        self.flat = flat
        self.volume = volume

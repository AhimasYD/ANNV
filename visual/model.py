from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .constants import *
from visual.layers.layers import *


class VModel:
    def __init__(self, logic, scene, opt_display, opt_weight_color, opt_weight_thick, opt_names, opt_captions, opt_bias,
                 wl, wm, wf, wv):
        self.logic = logic
        self.scene = scene

        self.opt_display = opt_display
        self.opt_weight_color = opt_weight_color
        self.opt_weight_thick = opt_weight_thick
        self.opt_names = opt_names
        self.opt_captions = opt_captions
        self.opt_bias = opt_bias

        self.wl = wl
        self.wm = wm
        self.wf = wf
        self.wv = wv

        self.summary()

        self.x = 0

        self.layers = []
        for l_layer in logic.layers:
            if type(l_layer).__name__ == 'LDense':
                layer = VDense(l_layer, self.scene, self.x,
                               self.opt_display, self.opt_weight_color, self.opt_weight_thick,
                               self.opt_names, self.opt_captions, self.opt_bias, self.wl, self.wf, self.wv)

            elif type(l_layer).__name__ == 'LEmbedding':
                layer = VEmbedding(l_layer, self.scene, self.x,
                                   self.opt_display, self.opt_weight_color, self.opt_weight_thick,
                                   self.opt_names, self.opt_captions, self.opt_bias, self.wl, self.wf, self.wv)
            elif type(l_layer).__name__ == 'LConv2D':
                layer = VConv2D(l_layer, self.scene, self.x,
                                   self.opt_display, self.opt_weight_color, self.opt_weight_thick,
                                   self.opt_names, self.opt_captions, self.opt_bias, self.wl, self.wf, self.wv)
            else:
                layer = VDefault(l_layer, self.scene, self.x,
                                 self.opt_display, self.opt_weight_color, self.opt_weight_thick,
                                 self.opt_names, self.opt_captions, self.opt_bias, self.wl, self.wf, self.wv)

            self.layers.append(layer)
            self.x = self.scene.width() + LAYER_MARGIN

    def summary(self):
        summary = self.logic.summary

        table = QTableWidget(summary.shape[0], summary.shape[1], self.wm)

        vh_name = QTableWidgetItem('Name')
        vh_type = QTableWidgetItem('Type')
        vh_shape = QTableWidgetItem('Shape')
        table.setHorizontalHeaderItem(0, vh_name)
        table.setHorizontalHeaderItem(1, vh_type)
        table.setHorizontalHeaderItem(2, vh_shape)
        table.verticalHeader().hide()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setFocusPolicy(Qt.NoFocus)
        # table.setSelectionModel(QAbstractItemView.NoSelection)

        for i in range(summary.shape[0]):
            c_name = QTableWidgetItem(str(summary.at[i, 'Name']))
            c_type = QTableWidgetItem(str(summary.at[i, 'Type']))
            c_shape = QTableWidgetItem(str(summary.at[i, 'Shape']))

            c_name.setTextAlignment(Qt.AlignCenter)
            c_type.setTextAlignment(Qt.AlignCenter)
            c_shape.setTextAlignment(Qt.AlignCenter)

            table.setItem(i, 0, c_name)
            table.setItem(i, 1, c_type)
            table.setItem(i, 2, c_shape)

        self.wm.layout().addWidget(table)

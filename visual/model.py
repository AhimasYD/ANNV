from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np

from .constants import *
from .layers import *
from .links import *


class VModel:
    def __init__(self, logic, scene, _o_display, o_color, o_thick, o_names, o_captions, o_bias, wm, wl, wf, wv):
        self.logic = logic
        self.scene = scene

        self._o_display = _o_display
        self.o_color = o_color
        self.o_thick = o_thick
        self.o_names = o_names
        self.o_captions = o_captions
        self.o_bias = o_bias

        self.wl = wl
        self.wm = wm
        self.wf = wf
        self.wv = wv

        self.summary()

        self.x = 0
        self.layers = []
        for l_layer in logic.layers:
            layer = self.create_layer(l_layer)
            self.layers.append(layer)
            self.x = self.scene.width() + LAYER_MARGIN
        self.init_weights()

    def create_layer(self, logic):
        if type(logic).__name__ == 'LDense':
            layer = VDense(logic, self.scene, self.x,
                           self._o_display, self.o_color, self.o_thick,
                           self.o_names, self.o_captions, self.o_bias, self.wl, self.wf, self.wv)
        elif type(logic).__name__ == 'LLSTM':
            layer = VLSTM(logic, self.scene, self.x,
                          self._o_display, self.o_color, self.o_thick,
                          self.o_names, self.o_captions, self.o_bias, self.wl, self.wf, self.wv)
        elif type(logic).__name__ == 'LEmbedding':
            layer = VEmbedding(logic, self.scene, self.x,
                               self._o_display, self.o_color, self.o_thick,
                               self.o_names, self.o_captions, self.o_bias, self.wl, self.wf, self.wv)
        elif type(logic).__name__ == 'LConv1D':
            layer = VConv1D(logic, self.scene, self.x,
                            self._o_display, self.o_color, self.o_thick,
                            self.o_names, self.o_captions, self.o_bias, self.wl, self.wf, self.wv)
        elif type(logic).__name__ == 'LConv2D':
            layer = VConv2D(logic, self.scene, self.x,
                            self._o_display, self.o_color, self.o_thick,
                            self.o_names, self.o_captions, self.o_bias, self.wl, self.wf, self.wv)
        else:
            layer = VDefault(logic, self.scene, self.x,
                             self._o_display, self.o_color, self.o_thick,
                             self.o_names, self.o_captions, self.o_bias, self.wl, self.wf, self.wv)
        return layer

    def init_weights(self):
        for k in range(len(self.layers) - 1):
            layer_0 = self.layers[k]
            layer_1 = self.layers[k + 1]

            type_out, binds_out = layer_0.binds_out()
            type_in, binds_in = layer_1.binds_in()

            if type_out == LinkType.UNITED and type_in == LinkType.UNITED:
                link = VLink(binds_out, binds_in, LinkType.UNITED)
                self.scene.addItem(link.get_item())

                layer_0.set_links_out(link)
                layer_1.set_links_in(link)

            elif type_out == LinkType.UNITED and type_in == LinkType.SEPARATED:
                links = np.full(len(binds_in), None, dtype=VLayer)
                for i in range(len(binds_in)):
                    if binds_in[i] is not None:
                        link = VLink(binds_out, binds_in[i], LinkType.UNITED)
                        self.scene.addItem(link.get_item())

                        links[i] = link

                layer_0.set_links_out(links)
                layer_1.set_links_in(links)

            elif type_out == LinkType.SEPARATED and type_in == LinkType.UNITED:
                links = np.full(len(binds_out), None, dtype=VLayer)
                for i in range(len(binds_out)):
                    if binds_out[i] is not None:
                        link = VLink(binds_out[i], binds_in, LinkType.UNITED)
                        self.scene.addItem(link.get_item())

                        links[i] = link

                layer_0.set_links_out(links)
                layer_1.set_links_in(links)

            elif type_out == LinkType.SEPARATED and type_in == LinkType.SEPARATED:
                links_in = np.full((len(binds_in), len(binds_out)), None, dtype=VLayer)
                links_out = np.full((len(binds_out), len(binds_in)), None, dtype=VLayer)
                for i in range(len(binds_in)):
                    for j in range(len(binds_out)):
                        if binds_out[j] is None or binds_in[i] is None:
                            continue
                        link = VLink(binds_out[j], binds_in[i], LinkType.SEPARATED)
                        self.scene.addItem(link.get_item())

                        links_in[i][j] = link
                        links_out[j][i] = link

                layer_0.set_links_out(links_out)
                layer_1.set_links_in(links_in)

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

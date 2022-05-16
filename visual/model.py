from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np

from .constants import *
from .layers import *
from .links import *


class VModel:
    def __init__(self, logic, scene, _o_display, o_color, o_thick, o_names, o_captions, o_bias, wm, wl, wf, wv):
        self._logic = logic
        self._scene = scene

        self._o_display = _o_display
        self._o_color = o_color
        self._o_thick = o_thick
        self._o_names = o_names
        self._o_captions = o_captions
        self._o_bias = o_bias

        self._wl = wl
        self._wm = wm
        self._wf = wf
        self._wv = wv

        self._summary()

        self._x = 0
        self._layers = []
        for l_layer in logic.layers:
            layer = self._create_layer(l_layer)
            self._layers.append(layer)
            self._x = self._scene.itemsBoundingRect().width() + LAYER_MARGIN
        self._init_weights()

    @property
    def logic(self):
        return self._logic

    def _create_layer(self, logic):
        if type(logic).__name__ == 'LDense':
            layer = VDense(logic, self._scene, self._x,
                           self._o_display, self._o_color, self._o_thick,
                           self._o_names, self._o_captions, self._o_bias, self._wl, self._wf, self._wv)
        elif type(logic).__name__ == 'LLSTM':
            layer = VLSTM(logic, self._scene, self._x,
                          self._o_display, self._o_color, self._o_thick,
                          self._o_names, self._o_captions, self._o_bias, self._wl, self._wf, self._wv)
        elif type(logic).__name__ == 'LEmbedding':
            layer = VEmbedding(logic, self._scene, self._x,
                               self._o_display, self._o_color, self._o_thick,
                               self._o_names, self._o_captions, self._o_bias, self._wl, self._wf, self._wv)
        elif type(logic).__name__ == 'LConv1D':
            layer = VConv1D(logic, self._scene, self._x,
                            self._o_display, self._o_color, self._o_thick,
                            self._o_names, self._o_captions, self._o_bias, self._wl, self._wf, self._wv)
        elif type(logic).__name__ == 'LConv2D':
            layer = VConv2D(logic, self._scene, self._x,
                            self._o_display, self._o_color, self._o_thick,
                            self._o_names, self._o_captions, self._o_bias, self._wl, self._wf, self._wv)
        else:
            layer = VDefault(logic, self._scene, self._x,
                             self._o_display, self._o_color, self._o_thick,
                             self._o_names, self._o_captions, self._o_bias, self._wl, self._wf, self._wv)
        return layer

    def _init_weights(self):
        for k in range(len(self._layers) - 1):
            layer_0 = self._layers[k]
            layer_1 = self._layers[k + 1]

            type_out, binds_out = layer_0.binds_out()
            type_in, binds_in = layer_1.binds_in()

            if type_out == LinkType.UNITED and type_in == LinkType.UNITED:
                link = VLink(binds_out, binds_in, LinkType.UNITED)
                self._scene.addItem(link.get_item())

                layer_0.set_links_out(link)
                layer_1.set_links_in(link)

            elif type_out == LinkType.UNITED and type_in == LinkType.SEPARATED:
                links = np.full(len(binds_in), None, dtype=VLayer)
                for i in range(len(binds_in)):
                    if binds_in[i] is not None:
                        link = VLink(binds_out, binds_in[i], LinkType.UNITED)
                        self._scene.addItem(link.get_item())

                        links[i] = link

                layer_0.set_links_out(links)
                layer_1.set_links_in(links)

            elif type_out == LinkType.SEPARATED and type_in == LinkType.UNITED:
                links = np.full(len(binds_out), None, dtype=VLayer)
                for i in range(len(binds_out)):
                    if binds_out[i] is not None:
                        link = VLink(binds_out[i], binds_in, LinkType.UNITED)
                        self._scene.addItem(link.get_item())

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
                        self._scene.addItem(link.get_item())

                        links_in[i][j] = link
                        links_out[j][i] = link

                layer_0.set_links_out(links_out)
                layer_1.set_links_in(links_in)

    def _summary(self):
        summary = self._logic.summary

        table = QTableWidget(summary.shape[0], summary.shape[1], self._wm)

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

        self._wm.layout().addWidget(table)

    def set_weight_color_hint(self, hint: WeightColor):
        for layer in self._layers:
            layer.set_weight_color_hint(hint)

    def set_weight_thick_hint(self, hint: WeightThick):
        for layer in self._layers:
            layer.set_weight_thick_hint(hint)

    def load_input(self, filename):
        self._logic.load_input(filename)

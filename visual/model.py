from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox
from PyQt5.QtCore import Qt

import numpy as np

from visual.widgets import clear_layout
from visual.layers import *
from visual.links import *


class VModel:
    def __init__(self, logic, scene, wm, wl, wf, wv):
        self._logic = logic
        self._scene = scene

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
        self._init_biases()

    @property
    def logic(self):
        return self._logic

    def _create_layer(self, logic):
        if logic.type == 'Dense':
            v_layer = VDense(logic, self._scene, self._x, self._wl, self._wf, self._wv)
        elif logic.type == 'SimpleRNN':
            v_layer = VSimpleRNN(logic, self._scene, self._x, self._wl, self._wf, self._wv)
        elif logic.type == 'LSTM':
            v_layer = VLSTM(logic, self._scene, self._x, self._wl, self._wf, self._wv)
        elif logic.type == 'GRU':
            v_layer = VGRU(logic, self._scene, self._x, self._wl, self._wf, self._wv)
        elif logic.type == 'Embedding':
            v_layer = VEmbedding(logic, self._scene, self._x, self._wl, self._wf, self._wv)
        elif logic.type == 'Conv1D':
            v_layer = VConv1D(logic, self._scene, self._x, self._wl, self._wf, self._wv)
        elif logic.type == 'Conv2D':
            v_layer = VConv2D(logic, self._scene, self._x, self._wl, self._wf, self._wv)
        elif logic.type == 'Conv3D':
            v_layer = VConv3D(logic, self._scene, self._x, self._wl, self._wf, self._wv)
        else:
            v_layer = VDefault(logic, self._scene, self._x, self._wl, self._wf, self._wv)
        return v_layer

    def _init_weights(self):
        for k in range(len(self._layers) - 1):
            layer_0 = self._layers[k]
            layer_1 = self._layers[k + 1]

            type_out, binds_out = layer_0.binds_out()
            type_in, binds_in = layer_1.binds_in()

            if type_out == LinkType.UNITED and type_in == LinkType.UNITED:
                link = VLink(binds_out, binds_in)
                self._scene.addItem(link.get_item())

                layer_0.set_links_out(link)
                layer_1.set_links_in(link)

            elif type_out == LinkType.UNITED and type_in == LinkType.SEPARATED:
                links = np.full(len(binds_in), None, dtype=VLayer)
                for i in range(len(binds_in)):
                    if binds_in[i] is not None:
                        link = VLink(binds_out, binds_in[i])
                        self._scene.addItem(link.get_item())

                        links[i] = link

                layer_0.set_links_out(links)
                layer_1.set_links_in(links)

            elif type_out == LinkType.SEPARATED and type_in == LinkType.UNITED:
                links = np.full(len(binds_out), None, dtype=VLayer)
                for i in range(len(binds_out)):
                    if binds_out[i] is not None:
                        link = VLink(binds_out[i], binds_in)
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
                        link = VLink(binds_out[j], binds_in[i])
                        self._scene.addItem(link.get_item())

                        links_in[i][j] = link
                        links_out[j][i] = link

                layer_0.set_links_out(links_out)
                layer_1.set_links_in(links_in)

    def _init_biases(self):
        bounding = self._layers[0].bounding()
        bounding.translate(-LAYER_MARGIN, 0)
        self._layers[0].set_bias(bounding)

        for k in range(len(self._layers) - 1):
            layer_0 = self._layers[k]
            layer_1 = self._layers[k + 1]

            bounding = layer_0.bounding()
            layer_1.set_bias(bounding)

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

        clear_layout(self._wm.layout())
        self._wm.layout().addWidget(table)

    def load_input(self, filename):
        res = self._logic.load_input(filename)
        if res:
            message = QMessageBox(QMessageBox.Warning, 'Error', res)
            message.exec()

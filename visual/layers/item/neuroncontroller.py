from PyQt5.QtCore import QPointF

from abc import ABCMeta, abstractmethod
import numpy as np

from weak import WeakMethod
from visual.layers.trivia import VPlaceholder
from visual.layers.constants import PLACEHOLDER_SIDE, PLACEHOLDER_MAX_NEURONS, PLACEHOLDER_MARGIN_IN, PLACEHOLDER_MARGIN_OUT


class VNeuronController(metaclass=ABCMeta):
    def __init__(self, scene, x, units, select, show_output, logic, ntype, nheight, nmargin):
        self._scene = scene
        self._x = x
        self._units = units

        self._neurons = None

        self._placeholder = None
        self._neurons_start = None
        self._neurons_end = None

        # No placeholder needed
        if units <= PLACEHOLDER_MAX_NEURONS * 2:
            self._neurons = np.empty(units, dtype=ntype)

            total_height = units * nheight + (units - 1) * nmargin
            y = -total_height/2
            for i in range(units):
                self._neurons[i] = ntype(self._scene, self._x, y, select, show_output)
                y += nheight + nmargin

        # Placeholder needed
        else:
            self._placeholder = VPlaceholder(PLACEHOLDER_SIDE, PLACEHOLDER_MARGIN_IN, 0, 0)
            self._placeholder.mousePressEvent = select
            self._scene.addItem(self._placeholder)

            self._neurons_start = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=ntype)
            self._neurons_end = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=ntype)

            total_height = 2 * PLACEHOLDER_MAX_NEURONS * nheight + 2 * PLACEHOLDER_MAX_NEURONS * nmargin
            total_height += self._placeholder.boundingRect().height() + 2 * PLACEHOLDER_MARGIN_OUT

            y = -total_height / 2
            for i in range(units):
                if i < PLACEHOLDER_MAX_NEURONS:
                    j = i
                    self._neurons_start[j] = ntype(self._scene, self._x, y, select, show_output)
                    y += nheight + nmargin
                elif i >= units - PLACEHOLDER_MAX_NEURONS:
                    j = i - (units - PLACEHOLDER_MAX_NEURONS)
                    self._neurons_end[j] = ntype(self._scene, self._x, y, select, show_output)
                    y += nheight + nmargin

                if i == PLACEHOLDER_MAX_NEURONS:
                    y += self._placeholder.boundingRect().height()
                    y += 2 * PLACEHOLDER_MARGIN_OUT
                    y += nmargin

            self._placeholder.setPos(self._x + nheight / 2 - self._placeholder.boundingRect().width() / 2,
                                     0 - self._placeholder.boundingRect().height() / 2)

        self._output_callback = WeakMethod(self, VNeuronController.update_output)
        logic.attach_output(self._output_callback)
        self._output_detach = logic.detach_output

    def __del__(self):
        self._output_detach(self._output_callback)
        print('DELETE VNeuronController')

    def _get_neuron(self, i):
        if self._neurons is not None:
            return self._neurons[i]
        else:
            if i < PLACEHOLDER_MAX_NEURONS:
                return self._neurons_start[i]
            elif i >= self._units - PLACEHOLDER_MAX_NEURONS:
                return self._neurons_end[i - (self._units - PLACEHOLDER_MAX_NEURONS)]
            else:
                return None

    def binds_in(self):
        if self._placeholder is None:
            binds = np.empty(self._units, dtype=QPointF)
            for i in range(self._units):
                binds[i] = self._neurons[i].bind_in()

        else:
            placeholder = np.full(shape=(self._units - 2 * PLACEHOLDER_MAX_NEURONS), fill_value=None, dtype=QPointF)

            binds_start = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=QPointF)
            for i in range(PLACEHOLDER_MAX_NEURONS):
                binds_start[i] = self._neurons_start[i].bind_in()

            binds_end = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=QPointF)
            for i in range(PLACEHOLDER_MAX_NEURONS):
                binds_end[i] = self._neurons_end[i].bind_in()

            binds = np.concatenate((binds_start, placeholder, binds_end))

        return binds

    def binds_out(self):
        if self._placeholder is None:
            binds = np.empty(self._units, dtype=QPointF)
            for i in range(self._units):
                binds[i] = self._neurons[i].bind_out()

        else:
            placeholder = np.full(shape=(self._units - 2 * PLACEHOLDER_MAX_NEURONS), fill_value=None, dtype=QPointF)

            binds_start = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=QPointF)
            for i in range(PLACEHOLDER_MAX_NEURONS):
                binds_start[i] = self._neurons_start[i].bind_out()

            binds_end = np.empty(PLACEHOLDER_MAX_NEURONS, dtype=QPointF)
            for i in range(PLACEHOLDER_MAX_NEURONS):
                binds_end[i] = self._neurons_end[i].bind_out()

            binds = np.concatenate((binds_start, placeholder, binds_end))

        return binds

    @abstractmethod
    def set_links_in(self, links, weights):
        """"""

    def set_links_out(self, links):
        for i in range(self._units):
            neuron = self._get_neuron(i)
            if neuron is not None:
                neuron.set_links_out(links[i])

    def update_output(self, output):
        maximum = max(output.min(), output.max(), key=abs)
        for i in range(self._units):
            neuron = self._get_neuron(i)
            if neuron is not None:
                if maximum is not None:
                    neuron.set_output(output[i], maximum)
                else:
                    neuron.set_output(output[i], 0.0)

    def bounding(self):
        unit_0 = self._get_neuron(0)
        unit_1 = self._get_neuron(self._units - 1)
        return unit_0.bounding().united(unit_1.bounding())

    @abstractmethod
    def set_bias(self, bounding, weights):
        """"""

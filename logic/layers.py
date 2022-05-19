import numpy as np


class LLayer:
    def __init__(self, logic):
        self._type = None
        self._output_shape = logic.output_shape
        self._output = None
        self._output_subs = []

    @property
    def type(self):
        return self._type

    @property
    def output_shape(self):
        return self._output_shape

    @property
    def output(self):
        return self._output

    def set_output(self, new_output):
        self._output = new_output
        for callback in self._output_subs:
            callback(self._output)

    def attach_output(self, callback):
        self._output_subs.append(callback)

    def detach_output(self, callback):
        self._output_subs.remove(callback)


class LDense(LLayer):
    def __init__(self, layer):
        super().__init__(layer)

        self._type = 'Dense'

        self._activation = str(layer.activation.__name__)
        self._units = layer.units
        self._kernel = layer.get_weights()[0]
        self._bias = layer.get_weights()[1]

    def set_output(self, new_output):
        new_output = new_output[0]
        super().set_output(new_output)

    @property
    def activation(self):
        return self._activation

    @property
    def units(self):
        return self._units

    @property
    def kernel(self):
        return self._kernel

    @property
    def bias(self):
        return self._bias


class LSimpleRNN(LLayer):
    def __init__(self, layer):
        super().__init__(layer)

        self._type = 'SimpleRNN'
        self._activation = str(layer.activation.__name__)
        self._units = layer.units

        self._W = layer.get_weights()[0]
        self._U = layer.get_weights()[1]
        self._b = layer.get_weights()[2]

    def set_output(self, new_output):
        new_output = new_output[0]
        while len(new_output.shape) > 1 and new_output.shape[0] == 1:
            new_output = new_output[0]
        super().set_output(new_output)

    @property
    def activation(self):
        return self._activation

    @property
    def units(self):
        return self._units

    @property
    def W(self):
        return self._W

    @property
    def U(self):
        return self._U

    @property
    def b(self):
        return self._b


class LLSTM(LLayer):
    def __init__(self, layer):
        super().__init__(layer)

        self._type = 'LSTM'
        self._activation = str(layer.activation.__name__)
        self._rec_activation = str(layer.recurrent_activation.__name__)
        self._units = layer.units

        self._W = layer.get_weights()[0]
        self._U = layer.get_weights()[1]
        self._b = layer.get_weights()[2]

    def set_output(self, new_output):
        new_output = new_output[0]
        while len(new_output.shape) > 1 and new_output.shape[0] == 1:
            new_output = new_output[0]
        super().set_output(new_output)

    @property
    def activation(self):
        return self._activation

    @property
    def rec_activation(self):
        return self._rec_activation

    @property
    def units(self):
        return self._units

    @property
    def W_i(self):
        return self._W[:, :self.units]

    @property
    def W_f(self):
        return self._W[:, self.units:self.units*2]

    @property
    def W_c(self):
        return self._W[:, self.units*2:self.units*3]

    @property
    def W_o(self):
        return self._W[:, self.units*3:]

    @property
    def U_i(self):
        return self._U[:, :self.units]

    @property
    def U_f(self):
        return self._U[:, self.units:self.units * 2]

    @property
    def U_c(self):
        return self._U[:, self.units * 2:self.units * 3]

    @property
    def U_o(self):
        return self._U[:, self.units * 3:]

    @property
    def b_i(self):
        return self._b[:self.units]

    @property
    def b_f(self):
        return self._b[self.units:self.units * 2]

    @property
    def b_c(self):
        return self._b[self.units * 2:self.units * 3]

    @property
    def b_o(self):
        return self._b[self.units * 3:]


class LGRU(LLayer):
    def __init__(self, layer):
        super().__init__(layer)

        self._type = 'GRU'
        self._activation = str(layer.activation.__name__)
        self._rec_activation = str(layer.recurrent_activation.__name__)
        self._units = layer.units

        self._W = layer.get_weights()[0]
        self._U = layer.get_weights()[1]
        self._b = layer.get_weights()[2]

    def set_output(self, new_output):
        new_output = new_output[0]
        while len(new_output.shape) > 1 and new_output.shape[0] == 1:
            new_output = new_output[0]
        super().set_output(new_output)

    @property
    def activation(self):
        return self._activation

    @property
    def rec_activation(self):
        return self._rec_activation

    @property
    def units(self):
        return self._units

    @property
    def W_z(self):
        return self._W[:, :self.units]

    @property
    def W_r(self):
        return self._W[:, self.units:self.units*2]

    @property
    def W_h(self):
        return self._W[:, self.units*2:]

    @property
    def U_z(self):
        return self._U[:, :self.units]

    @property
    def U_r(self):
        return self._U[:, self.units:self.units * 2]

    @property
    def U_h(self):
        return self._U[:, self.units * 2:]

    @property
    def b_iz(self):
        return self._b[0, :self.units]

    @property
    def b_ir(self):
        return self._b[0, self.units:self.units * 2]

    @property
    def b_ih(self):
        return self._b[0, self.units * 2:self.units * 3]

    @property
    def b_rz(self):
        return self._b[1, :self.units]

    @property
    def b_rr(self):
        return self._b[1, self.units:self.units * 2]

    @property
    def b_rh(self):
        return self._b[1, self.units * 2:self.units * 3]


class LConv1D(LLayer):
    def __init__(self, layer):
        super().__init__(layer)

        self._type = 'Conv1D'
        # Filter, Channel, Width
        self._filters = np.transpose(layer.get_weights()[0], (2, 1, 0))
        self._bias = layer.get_weights()[1]

        self._padding = layer.padding
        self._strides = layer.strides
        self._dilation_rate = layer.dilation_rate
        self._groups = layer.groups
        self._activation = str(layer.activation.__name__)

    def set_output(self, new_output):
        new_output = new_output[0]
        new_output = np.transpose(new_output, (1, 0))
        super().set_output(new_output)

    @property
    def filters(self):
        return self._filters

    @property
    def bias(self):
        return self._bias

    @property
    def filter_num(self):
        return self.filters.shape[0]

    @property
    def channel_num(self):
        return self.filters.shape[1]

    @property
    def kernel_shape(self):
        return self.filters.shape[2:]

    @property
    def padding(self):
        return self._padding

    @property
    def strides(self):
        return self._strides

    @property
    def dilation_rate(self):
        return self._dilation_rate

    @property
    def groups(self):
        return self._groups

    @property
    def activation(self):
        return self._activation


class LConv2D(LLayer):
    def __init__(self, layer):
        super().__init__(layer)

        self._type = 'Conv2D'
        # Filter, Channel, Height, Width
        self._filters = np.transpose(layer.get_weights()[0], (3, 2, 0, 1))
        self._bias = layer.get_weights()[1]

        self._padding = layer.padding
        self._strides = layer.strides
        self._dilation_rate = layer.dilation_rate
        self._groups = layer.groups
        self._activation = str(layer.activation.__name__)

    def set_output(self, new_output):
        new_output = new_output[0]
        new_output = np.transpose(new_output, (2, 0, 1))
        super().set_output(new_output)

    @property
    def filters(self):
        return self._filters

    @property
    def bias(self):
        return self._bias

    @property
    def filter_num(self):
        return self.filters.shape[0]

    @property
    def channel_num(self):
        return self.filters.shape[1]

    @property
    def kernel_shape(self):
        return self.filters.shape[2:]

    @property
    def padding(self):
        return self._padding

    @property
    def strides(self):
        return self._strides

    @property
    def dilation_rate(self):
        return self._dilation_rate

    @property
    def groups(self):
        return self._groups

    @property
    def activation(self):
        return self._activation


class LConv3D(LLayer):
    def __init__(self, layer):
        super().__init__(layer)

        self._type = 'Conv3D'
        # Filter, Depth, Channel, Height, Width
        self._filters = np.transpose(layer.get_weights()[0], (4, 0, 3, 1, 2))
        self._bias = layer.get_weights()[1]

        self._padding = layer.padding
        self._strides = layer.strides
        self._dilation_rate = layer.dilation_rate
        self._groups = layer.groups
        self._activation = str(layer.activation.__name__)

    def set_output(self, new_output):
        new_output = new_output[0]
        new_output = np.transpose(new_output, (3, 0, 1, 2))
        super().set_output(new_output)

    @property
    def filters(self):
        return self._filters

    @property
    def bias(self):
        return self._bias

    @property
    def filter_num(self):
        return self.filters.shape[0]

    @property
    def channel_num(self):
        return self.filters.shape[2]

    @property
    def depth(self):
        return self.filters.shape[1]

    @property
    def kernel_shape(self):
        return self.depth, *self.filters.shape[3:]

    @property
    def padding(self):
        return self._padding

    @property
    def strides(self):
        return self._strides

    @property
    def dilation_rate(self):
        return self._dilation_rate

    @property
    def groups(self):
        return self._groups

    @property
    def activation(self):
        return self._activation


class LEmbedding(LLayer):
    def __init__(self, layer):
        super().__init__(layer)

        self._type = 'Embedding'
        self._weights = layer.get_weights()[0]

    def set_output(self, new_output):
        new_output = new_output[0]
        length = len(new_output.shape)
        new_output = np.transpose(new_output, (length - 1, *range(length - 1)))
        super().set_output(new_output)

    @property
    def weights(self):
        return self._weights


class LDefault(LLayer):
    def __init__(self, layer):
        super().__init__(layer)
        self._type = type(layer).__name__

    def set_output(self, new_output):
        pass

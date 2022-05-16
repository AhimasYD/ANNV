import numpy


class LLayer:
    def __init__(self):
        self._ltype = None
        self._output = None

        self._output_subs = []

    @property
    def ltype(self):
        return self._ltype

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
        super().__init__()

        self.type = 'Dense'
        self.activation = str(layer.activation.__name__)
        self.units = layer.units
        self.kernel = layer.get_weights()[0]
        self.bias = layer.get_weights()[1]

    def set_output(self, new_output):
        new_output = new_output[0]
        super().set_output(new_output)


class LLSTM(LLayer):
    def __init__(self, layer):
        super().__init__()

        self.type = 'LSTM'
        self.activation = str(layer.activation.__name__)
        units = layer.units
        self.units = layer.units

        W = layer.get_weights()[0]
        U = layer.get_weights()[1]
        b = layer.get_weights()[2]

        self.W_i = W[:, :units]
        self.W_f = W[:, units:units*2]
        self.W_c = W[:, units*2:units*3]
        self.W_o = W[:, units*3:]

        self.U_i = U[:, :units]
        self.U_f = U[:, units:units*2]
        self.U_c = U[:, units*2:units*3]
        self.U_o = U[:, units*3:]

        self.b_i = b[:units]
        self.b_f = b[units:units*2]
        self.b_c = b[units*2:units*3]
        self.b_o = b[units*3:]

    def set_output(self, new_output):
        new_output = new_output[0]
        super().set_output(new_output)


class LConv1D(LLayer):
    def __init__(self, layer):
        super().__init__()

        self.type = 'Conv1D'
        self.filters = numpy.transpose(layer.get_weights()[0], (2, 1, 0))
        self.bias = layer.get_weights()[1]

        self.filter_num = self.filters.shape[0]
        self.channel_num = self.filters.shape[1]
        self.kernel_shape = self.filters.shape[2:]

        self.padding = layer.padding
        self.strides = layer.strides
        self.dilation_rate = layer.dilation_rate
        self.groups = layer.groups
        self.activation = str(layer.activation.__name__)

    def set_output(self, new_output):
        new_output = new_output[0]
        new_output = numpy.transpose(new_output, (1, 0))
        super().set_output(new_output)


class LConv2D(LLayer):
    def __init__(self, layer):
        super().__init__()

        self.type = 'Conv2D'
        self.filters = numpy.transpose(layer.get_weights()[0], (3, 2, 0, 1))
        self.bias = layer.get_weights()[1]

        self.filter_num = self.filters.shape[0]
        self.channel_num = self.filters.shape[1]
        self.kernel_shape = self.filters.shape[2:]

        self.padding = layer.padding
        self.strides = layer.strides
        self.dilation_rate = layer.dilation_rate
        self.groups = layer.groups
        self.activation = str(layer.activation.__name__)

    def set_output(self, new_output):
        new_output = new_output[0]
        new_output = numpy.transpose(new_output, (2, 0, 1))
        super().set_output(new_output)


class LEmbedding(LLayer):
    def __init__(self, layer):
        super().__init__()

        self.type = 'Embedding'
        self.matrix = layer.weights

    def set_output(self, new_output):
        new_output = new_output[0]
        length = len(new_output.shape)
        new_output = numpy.transpose(new_output, (length - 1, *range(length - 1)))
        super().set_output(new_output)


class LDefault(LLayer):
    def __init__(self, layer):
        super().__init__()

        self.name = type(layer).__name__

    def set_output(self, new_output):
        pass

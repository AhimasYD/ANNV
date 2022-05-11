import numpy


class LDense:
    def __init__(self, layer):
        self.type = 'Dense'
        self.activation = str(layer.activation.__name__)
        self.units = layer.units
        self.kernel = layer.get_weights()[0]
        self.bias = layer.get_weights()[1]


class LLSTM:
    def __init__(self, layer):
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


class LConv1D:
    def __init__(self, layer):
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


class LConv2D:
    def __init__(self, layer):
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


class LEmbedding:
    def __init__(self, layer):
        self.type = 'Embedding'
        self.matrix = layer.weights


class LDefault:
    def __init__(self, layer):
        self.name = type(layer).__name__

import numpy


class LDense:
    def __init__(self, layer):
        self.type = 'Dense'
        self.activation = str(layer.activation.__name__)
        self.units = layer.units
        self.kernel = layer.weights[0].numpy()
        self.bias = layer.weights[1].numpy()


class LConv2D:
    def __init__(self, layer):
        self.type = 'Conv2D'
        self.filters = numpy.transpose(layer.weights[0].numpy(), (3, 2, 0, 1))
        self.bias = layer.weights[1].numpy()

        self.filter_num = self.filters.shape[0]
        self.channel_num = self.filters.shape[1]
        self.kernel_shape = self.filters.shape[2:]


class LEmbedding:
    def __init__(self, layer):
        self.type = 'Embedding'
        self.matrix = layer.weights


class LDefault:
    def __init__(self, layer):
        self.name = type(layer).__name__

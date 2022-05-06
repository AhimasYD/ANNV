class LDense:
    def __init__(self, layer):
        self.type = 'Dense'
        self.activation = str(layer.activation.__name__)
        self.units = layer.units
        self.kernel = layer.weights[0].numpy()
        self.bias = layer.weights[1].numpy()


class LEmbedding:
    def __init__(self, layer):
        self.type = 'Embedding'
        self.matrix = layer.weights


class LDefault:
    def __init__(self, layer):
        self.name = type(layer).__name__

import pandas as pd
from tensorflow import keras

from .layers import *


class LModel:
    def __init__(self, filename):
        print('LOADING MODEL', filename)
        model = keras.models.load_model(filename)
        print(model.summary())

        self.summary = []
        for layer in model.layers:
            self.summary.append(pd.DataFrame({
                'Name': [layer.name],
                'Type': [layer.__class__.__name__],
                'Shape': [layer.output_shape]
            }))
        self.summary = pd.concat(self.summary, ignore_index=True)

        layer_names = list(map(lambda x: type(x).__name__, model.layers))
        self.layers = []
        for i in range(len(layer_names)):
            name = layer_names[i]
            if name == 'Dense':
                layer = LDense(model.layers[i])
            elif name == 'LSTM':
                layer = LLSTM(model.layers[i])
            elif name == 'Conv1D':
                layer = LConv1D(model.layers[i])
            elif name == 'Conv2D':
                layer = LConv2D(model.layers[i])
            elif name == 'Embedding':
                layer = LEmbedding(model.layers[i])
            else:
                layer = LDefault(model.layers[i])
            self.layers.append(layer)

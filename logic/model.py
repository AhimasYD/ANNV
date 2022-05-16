import numpy as np
import pandas as pd
from tensorflow import keras

from .layers import *


class LModel:
    def __init__(self, filename):
        # print('LOADING MODEL', filename)
        self.k_model = keras.models.load_model(filename)
        # print(model.summary())

        self.summary = []
        for layer in self.k_model.layers:
            self.summary.append(pd.DataFrame({
                'Name': [layer.name],
                'Type': [layer.__class__.__name__],
                'Shape': [layer.output_shape]
            }))
        self.summary = pd.concat(self.summary, ignore_index=True)

        layer_names = list(map(lambda x: type(x).__name__, self.k_model.layers))
        self.layers = []
        for i in range(len(layer_names)):
            name = layer_names[i]
            if name == 'Dense':
                layer = LDense(self.k_model.layers[i])
            elif name == 'LSTM':
                layer = LLSTM(self.k_model.layers[i])
            elif name == 'Conv1D':
                layer = LConv1D(self.k_model.layers[i])
            elif name == 'Conv2D':
                layer = LConv2D(self.k_model.layers[i])
            elif name == 'Embedding':
                layer = LEmbedding(self.k_model.layers[i])
            else:
                layer = LDefault(self.k_model.layers[i])
            self.layers.append(layer)

    def layer_num(self):
        return len(self.layers)

    def load_input(self, filename):
        file_input = None
        try:
            filename = filename
            file_input = np.loadtxt(filename, comments="#", delimiter=",", unpack=False)
        except:
            return "Can't read file"

        try:
            shape = self.k_model.input_shape[1:]
            file_input = file_input.reshape(shape)
            file_input = np.array([file_input])
        except:
            return "Incorrect input shape"

        for i in range(len(self.layers)):
            try:
                inter_model = keras.Model(inputs=self.k_model.input, outputs=self.k_model.layers[i].output)
                output = inter_model.predict(file_input)
                self.layers[i].set_output(output)
            except:
                print(i)
                pass

        return None

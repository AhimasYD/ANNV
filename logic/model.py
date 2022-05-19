import pandas as pd
from tensorflow import keras

from logic.layers import *


class LModel:
    def __init__(self, filename):
        # print('LOADING MODEL', filename)
        self._k_model = keras.models.load_model(filename)
        # print(model.summary())

        self._summary = []
        for layer in self._k_model.layers:
            self._summary.append(pd.DataFrame({
                'Name': [layer.name],
                'Type': [layer.__class__.__name__],
                'Input shape': [layer.input_shape],
                'Output shape': [layer.output_shape]
            }))
        self._summary = pd.concat(self._summary, ignore_index=True)

        layer_names = list(map(lambda x: type(x).__name__, self._k_model.layers))
        self._layers = []
        for i in range(len(layer_names)):
            name = layer_names[i]
            if name == 'Dense':
                layer = LDense(self._k_model.layers[i])
            elif name == 'SimpleRNN':
                layer = LSimpleRNN(self._k_model.layers[i])
            elif name == 'LSTM':
                layer = LLSTM(self._k_model.layers[i])
            elif name == 'GRU':
                layer = LGRU(self._k_model.layers[i])
            elif name == 'Conv1D':
                layer = LConv1D(self._k_model.layers[i])
            elif name == 'Conv2D':
                layer = LConv2D(self._k_model.layers[i])
            elif name == 'Conv3D':
                layer = LConv3D(self._k_model.layers[i])
            elif name == 'Embedding':
                layer = LEmbedding(self._k_model.layers[i])
            else:
                layer = LDefault(self._k_model.layers[i])
            self._layers.append(layer)

    @property
    def layers(self):
        return self._layers

    @property
    def layer_num(self):
        return len(self._layers)

    @property
    def summary(self):
        return self._summary

    def load_input(self, filename):
        file_input = None
        try:
            filename = filename
            file_input = np.loadtxt(filename, comments="#", delimiter=",", unpack=False)
        except:
            return "Can't read file"

        try:
            shape = self._k_model.input_shape[1:]
            if shape[0] is None:
                shape = (1, *shape[1:])
            file_input = file_input.reshape(shape)
            file_input = np.array([file_input])
        except:
            return "Incorrect input shape"

        for i in range(len(self._layers)):
            try:
                inter_model = keras.Model(inputs=self._k_model.input, outputs=self._k_model.layers[i].output)
                output = inter_model.predict(file_input)
                self._layers[i].set_output(output)
            except:
                print(i)
                pass

        return None

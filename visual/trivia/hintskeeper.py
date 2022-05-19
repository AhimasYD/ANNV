from visual.constants import Display, WeightColor, WeightThick, Names, Captions, Bias, Activation


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class HintsKeeper(metaclass=SingletonMeta):
    def __init__(self):
        self._display = Display.COMPACT
        self._color = WeightColor.OFF
        self._thick = WeightThick.OFF
        self._names = Names.HORIZONTAL
        self._captions = Captions.OFF
        self._bias = Bias.OFF
        self._activation = Activation.ON

        self._display_subs = []
        self._color_subs = []
        self._thick_subs = []
        self._names_subs = []
        self._captions_subs = []
        self._bias_subs = []
        self._activation_subs = []

    @property
    def display(self):
        return self._display

    @property
    def color(self):
        return self._color

    @property
    def thick(self):
        return self._thick

    @property
    def names(self):
        return self._names

    @property
    def captions(self):
        return self._captions

    @property
    def bias(self):
        return self._bias

    @property
    def activation(self):
        return self._activation

    @display.setter
    def display(self, value: Display):
        self._display = value
        for callback in self._display_subs:
            callback(value)

    @color.setter
    def color(self, value: WeightColor):
        self._color = value
        for callback in self._color_subs:
            callback(value)

    @thick.setter
    def thick(self, value: WeightThick):
        self._thick = value
        for callback in self._thick_subs:
            callback(value)

    @names.setter
    def names(self, value: Names):
        self._names = value
        for callback in self._names_subs:
            callback(value)

    @captions.setter
    def captions(self, value: Captions):
        self._captions = value
        for callback in self._captions_subs:
            callback(value)

    @bias.setter
    def bias(self, value):
        self._bias = value
        for callback in self._bias_subs:
            callback(value)

    @activation.setter
    def activation(self, value):
        self._activation = value
        for callback in self._activation_subs:
            callback(value)

    def attach_display(self, callback):
        self._display_subs.append(callback)

    def attach_color(self, callback):
        self._color_subs.append(callback)

    def attach_thick(self, callback):
        self._thick_subs.append(callback)

    def attach_names(self, callback):
        self._names_subs.append(callback)

    def attach_captions(self, callback):
        self._captions_subs.append(callback)

    def attach_bias(self, callback):
        self._bias_subs.append(callback)

    def attach_activation(self, callback):
        self._activation_subs.append(callback)

    def detach_display(self, callback):
        self._display_subs.remove(callback)

    def detach_color(self, callback):
        self._color_subs.remove(callback)

    def detach_thick(self, callback):
        self._thick_subs.remove(callback)

    def detach_names(self, callback):
        self._names_subs.remove(callback)

    def detach_captions(self, callback):
        self._captions_subs.remove(callback)

    def detach_bias(self, callback):
        self._bias_subs.remove(callback)

    def detach_activation(self, callback):
        self._activation_subs.remove(callback)

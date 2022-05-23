from PyQt5.QtWidgets import QGraphicsLineItem

from math import isnan

from weak import WeakMethod
from visual.constants import WeightColor, WeightThick, Bias
from visual.trivia import HintsKeeper
from visual.links.constants import WeightType
from visual.links.arrow import Arrow


class VLink:
    def __init__(self, start, end, w_type=WeightType.KERNEL, tooltip=None):
        self._arrow = Arrow(start, end)
        self._type = w_type
        if self._type == WeightType.BIAS:
            self._arrow.set_dashed()

        self._weight = None
        self._maximum = None

        self._color_callback = WeakMethod(self, VLink.set_color_hint)
        self._thick_callback = WeakMethod(self, VLink.set_thick_hint)
        self._bias_callback = WeakMethod(self, VLink.set_bias_hint)
        HintsKeeper().attach_color(self._color_callback)
        HintsKeeper().attach_thick(self._thick_callback)
        HintsKeeper().attach_bias(self._bias_callback)
        self._color = HintsKeeper().color
        self._thick = HintsKeeper().thick
        self._bias = HintsKeeper().bias

        self._update_arrow()

        if tooltip is not None:
            self.set_tooltip(tooltip)

    def __del__(self):
        HintsKeeper().detach_color(self._color_callback)
        HintsKeeper().detach_thick(self._thick_callback)
        HintsKeeper().detach_bias(self._bias_callback)

    def _update_arrow(self):
        if self._type == WeightType.BIAS:
            if self._bias == Bias.ON:
                self._arrow.show()
            else:
                self._arrow.hide()

        if self._weight is None or self._maximum is None:
            return

        try:
            factor = self._weight / self._maximum
        except:
            factor = 0.0

        if self._color == WeightColor.ON:
            self._arrow.set_color(self._weight, self._maximum)
        else:
            self._arrow.reset_color()
        if self._thick == WeightThick.ON:
            self._arrow.set_width(abs(factor))
        else:
            self._arrow.reset_width()

    def set_tooltip(self, tooltip):
        self._arrow.set_tooltip(tooltip)

    def get_item(self):
        return self._arrow

    def set_weight(self, weight, maximum):
        self._weight = weight
        self._maximum = maximum
        self._update_arrow()

    def set_color_hint(self, hint: WeightColor):
        self._color = hint
        self._update_arrow()

    def set_thick_hint(self, hint: WeightThick):
        self._thick = hint
        self._update_arrow()

    def set_bias_hint(self, hint: WeightType):
        self._bias = hint
        self._update_arrow()

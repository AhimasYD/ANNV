from PyQt5.QtWidgets import QGraphicsLineItem

from visual.constants import WeightColor, WeightThick, Bias
from visual.hintskeeper import HintsKeeper

from .constants import WeightType
from .arrow import Arrow


class VLink(QGraphicsLineItem):
    def __init__(self, start, end, w_type=WeightType.KERNEL):
        super().__init__()

        self._arrow = Arrow(start, end)
        self._type = w_type
        if self._type == WeightType.BIAS:
            self._arrow.set_dotted()

        self._weight = None
        self._maximum = None

        HintsKeeper().attach_color(self.set_color_hint)
        HintsKeeper().attach_thick(self.set_thick_hint)
        HintsKeeper().attach_bias(self.set_bias_hint)
        self._color = HintsKeeper().color
        self._thick = HintsKeeper().thick
        self._bias = HintsKeeper().bias

        self._update_arrow()

    def __del__(self):
        HintsKeeper().detach_color(self.set_color_hint)
        HintsKeeper().detach_thick(self.set_thick_hint)

    def _update_arrow(self):
        if self._type == WeightType.BIAS:
            if self._bias == Bias.ON:
                self._arrow.show()
            else:
                self._arrow.hide()

        if self._weight is None or self._maximum is None:
            return
        factor = self._weight / self._maximum
        if self._color == WeightColor.ON:
            self._arrow.set_color(factor)
        else:
            self._arrow.reset_color()
        if self._thick == WeightThick.ON:
            self._arrow.set_width(abs(factor))
        else:
            self._arrow.reset_width()

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

from PyQt5.QtGui import QColor, QBrush


def brush_by_factor(value, maximum):
    try:
        factor = value / maximum
        alpha = abs(int(255 * factor))
    except ZeroDivisionError:
        factor = 0
        alpha = 0

    if factor >= 0:
        brush = QBrush(QColor(255, 0, 0, alpha))
    else:
        brush = QBrush(QColor(0, 0, 255, alpha))
    return brush

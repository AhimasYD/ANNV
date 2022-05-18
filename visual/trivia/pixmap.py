from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from visual.functions import brush_by_factor


MAX_ROWS = 10


class Pixmap(QTableWidget):
    def __init__(self, array, size, hv=True, hh=True, sb=True, mr=MAX_ROWS):
        self.size = size
        self.hv = hv
        self.hh = hh
        self.sb = sb
        self.mr = mr

        maximum = max(array.min(), array.max(), key=abs)
        if len(array.shape) == 2:
            self.rows = array.shape[0]
            self.columns = array.shape[1]
        else:
            self.rows = 1
            self.columns = array.shape[0]

        super().__init__(self.rows, self.columns)

        for i in range(self.rows):
            for j in range(self.columns):
                if len(array.shape) == 2:
                    val = array[i][j]
                else:
                    val = array[j]

                try:
                    alpha = abs(int(255 * (val / maximum)))
                except ValueError:
                    alpha = 0
                if val >= 0:
                    color = QColor(255, 0, 0, alpha)
                else:
                    color = QColor(0, 0, 255, alpha)

                cell = QTableWidgetItem()
                cell.setBackground(QBrush(color))
                cell.setToolTip(str(val))
                self.setItem(i, j, cell)

        self.setVerticalHeaderLabels(list(map(lambda x: str(x), list(range(self.rows)))))
        self.setHorizontalHeaderLabels(list(map(lambda x: str(x), list(range(self.columns)))))

        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.verticalHeader().setDefaultSectionSize(self.size)
        self.horizontalHeader().setDefaultSectionSize(self.size)

        self.verticalHeader().sectionPressed.disconnect()
        self.horizontalHeader().sectionPressed.disconnect()

        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)

        if not hv:
            self.verticalHeader().hide()
        if not hh:
            self.horizontalHeader().hide()
        if not sb:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

    def update_map(self, array):
        maximum = max(array.min(), array.max(), key=abs)
        for i in range(self.rows):
            for j in range(self.columns):
                if len(array.shape) == 2:
                    val = array[i][j]
                else:
                    val = array[j]

                if maximum is not None:
                    brush = brush_by_factor(val, maximum)
                else:
                    brush = brush_by_factor(val, 0.0)
                cell = self.item(i, j)
                cell.setBackground(brush)
                cell.setToolTip(str(val))

    def sizeHint(self):
        max_rows = self.mr if self.mr is not None and self.rows > MAX_ROWS else self.rows

        width = self.size * self.columns + 2
        width += self.verticalHeader().width() if self.hv else 0
        width += self.verticalScrollBar().width() if self.verticalScrollBar().isVisible() else 0

        height = self.size * max_rows + 2
        height += self.horizontalHeader().height() if self.hh else 0
        height += self.horizontalScrollBar().height() if self.horizontalScrollBar().isVisible() else 0

        return QSize(width, height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        hint = self.sizeHint()
        self.setMaximumWidth(hint.width())
        self.setMinimumHeight(hint.height())

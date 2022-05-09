from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


MAX_ROWS = 10


class Pixmap(QTableWidget):
    def __init__(self, array, size, hv=True, hh=True, sb=True):
        maximum = max(array.min(), array.max(), key=abs)
        if len(array.shape) == 2:
            rows = array.shape[0]
            columns = array.shape[1]
        else:
            rows = 1
            columns = array.shape[0]

        super().__init__(rows, columns)

        for i in range(rows):
            for j in range(columns):
                if len(array.shape) == 2:
                    val = array[i][j]
                else:
                    val = array[j]

                alpha = abs(int(255 * (val / maximum)))
                if val >= 0:
                    color = QColor(255, 0, 0, alpha)
                else:
                    color = QColor(0, 0, 255, alpha)

                cell = QTableWidgetItem()
                cell.setBackground(QBrush(color))
                cell.setToolTip(str(val))
                self.setItem(i, j, cell)

        self.setVerticalHeaderLabels(list(map(lambda x: str(x), list(range(rows)))))
        self.setHorizontalHeaderLabels(list(map(lambda x: str(x), list(range(columns)))))

        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.verticalHeader().setDefaultSectionSize(size)
        self.horizontalHeader().setDefaultSectionSize(size)

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

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        width = size * columns
        width += self.verticalHeader().width() if hv else 2
        width += self.verticalScrollBar().height() if sb else 0

        max_rows = MAX_ROWS if rows > MAX_ROWS else rows
        height = size * max_rows
        height += self.horizontalHeader().height() if hh else 0
        height += self.horizontalScrollBar().height() if sb else 0

        self.setMaximumWidth(width)
        self.setFixedHeight(height)

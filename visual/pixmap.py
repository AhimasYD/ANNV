from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Pixmap(QTableWidget):
    def __init__(self, array, size, hv, hh):
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

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMaximumWidth(size * columns + self.verticalHeader().width() + 2)
        self.setFixedHeight(size * rows + self.horizontalHeader().height() + self.horizontalScrollBar().height())

from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

import numpy as np
if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet("QLabel{font-size: 10pt;}")
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec()

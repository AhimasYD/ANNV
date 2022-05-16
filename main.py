from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

import numpy as np
import csv
from numpy import loadtxt



if __name__ == "__main__":
    filename = 'D:\\file.csv'
    lines = loadtxt(filename, comments="#", delimiter=",", unpack=False)
    print(lines)


    app = QApplication([])
    app.setStyleSheet("QLabel{font-size: 10pt;}")
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec()

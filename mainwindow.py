from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic.model import LModel
from visual.model import VModel
from visual.constants import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)

        menu_bar = self.menuBar()
        menu = QMenu('Options', self)

        sub_display = menu.addMenu('Display')
        group = QActionGroup(sub_display)
        texts = ['Compact', 'Extended']
        for text in texts:
            action = QAction(text, sub_display)
            action.setCheckable(True)
            action.setChecked(text == texts[0])

            sub_display.addAction(action)
            group.addAction(action)
        group.setExclusive(True)

        sub_weights = menu.addMenu('Weights')
        group = QActionGroup(sub_display)
        texts = ['Color', 'Thickness']
        for text in texts:
            action = QAction(text, sub_weights)
            action.setCheckable(True)

            sub_weights.addAction(action)
            group.addAction(action)
        group.setExclusive(False)

        sub_text = menu.addMenu('Names')
        group = QActionGroup(sub_display)
        texts = ['Horizontal', 'Vertical']
        for text in texts:
            action = QAction(text, sub_text)
            action.setCheckable(True)
            action.setChecked(text == texts[0])

            sub_text.addAction(action)
            group.addAction(action)
        group.setExclusive(True)

        sub_captions = menu.addMenu('Captions')
        group = QActionGroup(sub_display)
        texts = ['Show', 'Hide']
        for text in texts:
            action = QAction(text, sub_captions)
            action.setCheckable(True)
            action.setChecked(text == texts[0])

            sub_captions.addAction(action)
            group.addAction(action)
        group.setExclusive(True)

        action = QAction('Bias', menu)
        action.setCheckable(True)
        menu.addAction(action)

        menu_bar.addMenu(menu)

        # object_methods = [method_name for method_name in dir(self.tabLayer)
        #                   if callable(getattr(self.tabLayer, method_name))]
        # print(object_methods)
        # pprint(vars(self.tabLayer))
        # self.tabLayer.setExpanding(True)
        # print(self.tabModel.tabModel.setExpanding(True))

        self.actionOpen.triggered.connect(self.open_model)
        self.actionExport.triggered.connect(self.export_image)

        self.scene = QGraphicsScene()
        self.visualView.setScene(self.scene)

    def showMaximized(self):
        super().showMaximized()
        width = int(self.width() * 0.7)
        visualView = self.visualView
        self.visualView.setGeometry(visualView.x(), visualView.y(), width, visualView.height())

    def open_model(self):
        filename, _ = QFileDialog.getOpenFileName()
        self.logic = LModel(filename)
        self.tabModelSummary()
        self.visual = VModel(self.logic, self.scene, Display.COMPACT, False, False, Names.HORIZONTAL, False, False, self.tabLayer)

    def export_image(self):
        self.scene.clearSelection()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.white)

        painter = QPainter(image)
        self.scene.render(painter)
        image.save('D:\lala.png')

    def tabModelSummary(self):
        summary = self.logic.summary

        table = QTableWidget(summary.shape[0], summary.shape[1], self.tabModel)

        vh_name = QTableWidgetItem('Name')
        vh_type = QTableWidgetItem('Type')
        vh_shape = QTableWidgetItem('Shape')
        table.setHorizontalHeaderItem(0, vh_name)
        table.setHorizontalHeaderItem(1, vh_type)
        table.setHorizontalHeaderItem(2, vh_shape)
        table.verticalHeader().hide()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setFocusPolicy(Qt.NoFocus)
        # table.setSelectionModel(QAbstractItemView.NoSelection)

        for i in range(summary.shape[0]):
            c_name = QTableWidgetItem(str(summary.at[i, 'Name']))
            c_type = QTableWidgetItem(str(summary.at[i, 'Type']))
            c_shape = QTableWidgetItem(str(summary.at[i, 'Shape']))

            c_name.setTextAlignment(Qt.AlignCenter)
            c_type.setTextAlignment(Qt.AlignCenter)
            c_shape.setTextAlignment(Qt.AlignCenter)

            table.setItem(i, 0, c_name)
            table.setItem(i, 1, c_type)
            table.setItem(i, 2, c_shape)

        layout = QVBoxLayout()
        layout.addWidget(table)
        self.tabModel.setLayout(layout)

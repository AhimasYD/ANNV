from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *
from visual import *


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

        self.actionOpen.triggered.connect(self.open_model)
        self.actionExport.triggered.connect(self.export_image)

        self.scene = QGraphicsScene()
        self.visualView.setScene(self.scene)

        # Tab Model
        self.model_widget = QWidget()
        model_widget_layout = QVBoxLayout()
        self.model_widget.setLayout(model_widget_layout)

        model_scroll = QScrollArea()
        model_scroll.setWidget(self.model_widget)
        model_scroll.setWidgetResizable(True)

        model_layout = QVBoxLayout()
        model_layout.addWidget(model_scroll)

        self.tabModel.setLayout(model_layout)

        # Tab Layer
        self.layer_widget = QWidget()
        layer_widget_layout = QVBoxLayout()
        self.layer_widget.setLayout(layer_widget_layout)

        layer_scroll = QScrollArea()
        layer_scroll.setWidget(self.layer_widget)
        layer_scroll.setWidgetResizable(True)

        layer_layout = QVBoxLayout()
        layer_layout.addWidget(layer_scroll)

        # Buttons for 1D and 2D Conv
        flat_layout = QVBoxLayout()
        flat_layout.addWidget(QLabel('Filter #'))
        flat_layout_filter = QHBoxLayout()
        flat_layout_filter.addWidget(QPushButton('Prev'))
        # flat_prev = QPushButton('Prev')
        # flat_prev.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        # flat_prev.resize(30, flat_prev.height())
        flat_layout_filter.addWidget(QPushButton('Next'))
        flat_layout.addLayout(flat_layout_filter)
        self.flat_widget = QWidget()
        self.flat_widget.setLayout(flat_layout)
        layer_layout.addWidget(self.flat_widget)

        # Buttons for 3D Conv
        volume_layout_filter = QVBoxLayout()
        volume_layout_filter.addWidget(QLabel('Filter #'))
        volume_layout_filter_buttons = QHBoxLayout()
        volume_layout_filter_buttons.addWidget(QPushButton('Prev'))
        volume_layout_filter_buttons.addWidget(QPushButton('Next'))
        volume_layout_filter.addLayout(volume_layout_filter_buttons)

        volume_layout_depth = QVBoxLayout()
        volume_layout_depth.addWidget(QLabel('Depth #'))
        volume_layout_depth_buttons = QHBoxLayout()
        volume_layout_depth_buttons.addWidget(QPushButton('Prev'))
        volume_layout_depth_buttons.addWidget(QPushButton('Next'))
        volume_layout_depth.addLayout(volume_layout_depth_buttons)

        volume_layout = QHBoxLayout()
        volume_layout.addLayout(volume_layout_filter)
        volume_layout.addLayout(volume_layout_depth)

        self.volume_widget = QWidget()
        self.volume_widget.setLayout(volume_layout)
        layer_layout.addWidget(self.volume_widget)

        self.flat_widget.hide()
        self.volume_widget.hide()

        self.tabLayer.setLayout(layer_layout)

    def showMaximized(self):
        super().showMaximized()
        width = int(self.width() * 0.7)
        visualView = self.visualView
        self.visualView.setGeometry(visualView.x(), visualView.y(), width, visualView.height())

    def open_model(self):
        filename, _ = QFileDialog.getOpenFileName()
        self.logic = LModel(filename)
        self.visual = VModel(self.logic, self.scene, Display.EXTENDED, False, False, Names.HORIZONTAL, False, False,
                             self.layer_widget, self.model_widget, self.flat_widget, self.model_widget)

    def export_image(self):
        self.scene.clearSelection()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.white)

        painter = QPainter(image)
        self.scene.render(painter)
        image.save('D:\lala.png')

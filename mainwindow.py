from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from logic import *
from visual import *

from flatblock import FlatBlock
from volumeblock import VolumeBlock


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)

        self._o_display = Display.COMPACT
        self._o_color = WeightColor.OFF
        self._o_thick = WeightThick.ON
        self._o_names = Names.HORIZONTAL
        self._o_captions = Captions.OFF
        self._o_bias = Bias.OFF

        self._logic = None
        self._visual = None

        menu_bar = self.menuBar()
        menu = QMenu('Options', self)

        sub_display = menu.addMenu('Display')
        group = QActionGroup(sub_display)
        action = QAction('Compact', sub_display)
        action.setCheckable(True)
        action.setChecked(True)
        action.triggered.connect(self.display_compact)
        sub_display.addAction(action)
        group.addAction(action)
        action = QAction('Extended', sub_display)
        action.setCheckable(True)
        action.setChecked(False)
        action.triggered.connect(self.display_extended)
        sub_display.addAction(action)
        group.addAction(action)
        group.setExclusive(True)

        sub_weights = menu.addMenu('Weights')
        group = QActionGroup(sub_display)
        act_color = QAction('Color', sub_weights)
        act_color.setCheckable(True)
        act_color.triggered.connect(self.color_changed)
        sub_weights.addAction(act_color)
        group.addAction(act_color)
        act_thick = QAction('Thickness', sub_weights)
        act_thick.setCheckable(True)
        act_thick.triggered.connect(self.thick_changed)
        sub_weights.addAction(act_thick)
        group.addAction(act_thick)
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
        self.visualView.setRenderHints(QPainter.Antialiasing)

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

        self.flat = FlatBlock()
        self.volume = VolumeBlock()
        layer_layout.addWidget(self.flat)
        layer_layout.addWidget(self.volume)
        self.flat.hide()
        self.volume.hide()

        self.tabLayer.setLayout(layer_layout)

    def showMaximized(self):
        super().showMaximized()
        width = int(self.width() * 0.7)
        visualView = self.visualView
        self.visualView.setGeometry(visualView.x(), visualView.y(), width, visualView.height())

    def open_model(self):
        filename, lala = QFileDialog.getOpenFileName()
        if not filename:
            return

        self._logic = None
        self._visual = None
        self.scene.clear()

        self._logic = LModel(filename)
        self._visual = VModel(self._logic, self.scene,
                              self._o_display, self._o_color, self._o_thick, self._o_names, self._o_captions, self._o_bias,
                              self.model_widget, self.layer_widget, self.flat, self.volume)

    def recreate_visual(self):
        self._visual = None
        self.scene.clear()
        self._visual = VModel(self._logic, self.scene,
                              self._o_display, self._o_color, self._o_thick, self._o_names, self._o_captions, self._o_bias,
                              self.model_widget, self.layer_widget, self.flat, self.volume)

    def export_image(self):
        self.scene.clearSelection()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.white)

        painter = QPainter(image)
        self.scene.render(painter)
        image.save('D:\lala.png')

    def display_compact(self, checked):
        self._o_display = Display.COMPACT
        self.recreate_visual()

    def display_extended(self, checked):
        self._o_display = Display.EXTENDED
        self.recreate_visual()

    def color_changed(self, checked):
        if checked:
            self._o_color = WeightColor.ON
        else:
            self._o_color = WeightColor.OFF
        self._visual.set_weight_color_hint(self._o_color)

    def thick_changed(self, checked):
        if checked:
            self._o_thick = WeightThick.ON
        else:
            self._o_thick = WeightThick.OFF
        self._visual.set_weight_thick_hint(self._o_thick)

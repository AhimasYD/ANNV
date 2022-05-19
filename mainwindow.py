from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from math import ceil

from logic import *
from visual import *
from visual.widgets import FlatBlock, VolumeBlock, clear_layout
from visual.trivia import HintsKeeper


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._hints_keeper = HintsKeeper()

        self._o_display = Display.COMPACT
        self._o_color = WeightColor.OFF
        self._o_thick = WeightThick.ON
        self._o_names = Names.HORIZONTAL
        self._o_captions = Captions.OFF
        self._o_bias = Bias.OFF

        self._visual = None

        self.model_widget = None
        self.layer_widget = None
        self.flat = None
        self.volume = None
        self._init_ui()

    def _init_ui(self):
        uic.loadUi('mainwindow.ui', self)

        menu_bar = self.menuBar()
        menu = QMenu('Options', self)

        sub_display = menu.addMenu('Display')
        group = QActionGroup(sub_display)
        action = QAction('Compact', sub_display)
        action.setCheckable(True)
        action.setChecked(False)
        action.triggered.connect(self.display_compact)
        sub_display.addAction(action)
        group.addAction(action)
        action = QAction('Extended', sub_display)
        action.setCheckable(True)
        action.setChecked(True)
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
        action = QAction('Horizontal', sub_display)
        action.setCheckable(True)
        action.setChecked(True)
        action.triggered.connect(self.names_horizontal)
        sub_text.addAction(action)
        group.addAction(action)
        action = QAction('Vertical', sub_display)
        action.setCheckable(True)
        action.setChecked(False)
        action.triggered.connect(self.names_vertical)
        sub_text.addAction(action)
        group.addAction(action)
        group.setExclusive(True)

        action = QAction('Captions', menu)
        action.setCheckable(True)
        action.triggered.connect(self.captions_changed)
        menu.addAction(action)

        action = QAction('Bias', menu)
        action.setCheckable(True)
        action.triggered.connect(self.bias_changed)
        menu.addAction(action)

        action = QAction('Activation', menu)
        action.setCheckable(True)
        action.setChecked(True)
        action.triggered.connect(self.activation_changed)
        menu.addAction(action)

        menu_bar.addMenu(menu)

        self.actionOpen.triggered.connect(self.open_model)
        self.actionLoad.triggered.connect(self.load_input)
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

        self.flat = FlatBlock('Filter')
        self.volume = VolumeBlock('Filter', 'Depth')
        layer_layout.addWidget(self.flat)
        layer_layout.addWidget(self.volume)
        self.flat.hide()
        self.volume.hide()

        self.tabLayer.setLayout(layer_layout)

    def showMaximized(self):
        super().showMaximized()
        width = int(self.width() * 0.7)
        visual_view = self.visualView
        visual_view.setGeometry(visual_view.x(), visual_view.y(), width, visual_view.height())

    def open_model(self):
        filename, _ = QFileDialog.getOpenFileName()
        if not filename:
            return

        self._visual = None
        self.scene.clear()
        clear_layout(self.layer_widget.layout())

        logic = LModel(filename)
        self._visual = VModel(logic, self.scene, self.model_widget, self.layer_widget, self.flat, self.volume)
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

    def load_input(self):
        filename, _ = QFileDialog.getOpenFileName()
        if not filename:
            return
        self._visual.load_input(filename)

    def export_image(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Export Image', '', '*.png')
        if not filename:
            return
        if not filename.endswith('.png'):
            filename += '.png'

        self.scene.clearSelection()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

        rect = self.scene.sceneRect()
        # rect = QRectF(rect.x() - SCENE_RECT_PADDING, rect.y() - SCENE_RECT_PADDING,
        #               rect.width() + 4 * SCENE_RECT_PADDING, rect.height() + 4 * SCENE_RECT_PADDING)

        image = QImage(ceil(rect.width()), ceil(rect.height()), QImage.Format_ARGB32_Premultiplied)
        # image.fill(Qt.white)

        painter = QPainter(image)
        painter.setRenderHints(QPainter.Antialiasing)
        self.scene.render(painter)
        res = image.save(filename)
        print('RESULT', res)

    def display_compact(self, checked):
        self._o_display = Display.COMPACT
        self._hints_keeper.display = Display.COMPACT
        self.recreate_visual()

    def display_extended(self, checked):
        self._o_display = Display.EXTENDED
        self._hints_keeper.display = Display.EXTENDED
        self.recreate_visual()

    def color_changed(self, checked):
        if checked:
            self._hints_keeper.color = WeightColor.ON
        else:
            self._hints_keeper.color = WeightColor.OFF

    def thick_changed(self, checked):
        if checked:
            self._hints_keeper.thick = WeightThick.ON
        else:
            self._hints_keeper.thick = WeightThick.OFF

    def names_horizontal(self, checked):
        self._hints_keeper.names = Names.HORIZONTAL

    def names_vertical(self, checked):
        self._hints_keeper.names = Names.VERTICAL

    def captions_changed(self, checked):
        if checked:
            self._hints_keeper.captions = Captions.ON
        else:
            self._hints_keeper.captions = Captions.OFF

    def bias_changed(self, checked):
        if checked:
            self._hints_keeper.bias = Bias.ON
        else:
            self._hints_keeper.bias = Bias.OFF

    def activation_changed(self, checked):
        if checked:
            self._hints_keeper.activation = Activation.ON
        else:
            self._hints_keeper.activation = Activation.OFF

    def recreate_visual(self):
        if not self._visual:
            return

        logic = self._visual.logic
        self._visual = None
        self.scene.clear()
        clear_layout(self.layer_widget.layout())

        self._visual = VModel(logic, self.scene, self.model_widget, self.layer_widget, self.flat, self.volume)
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

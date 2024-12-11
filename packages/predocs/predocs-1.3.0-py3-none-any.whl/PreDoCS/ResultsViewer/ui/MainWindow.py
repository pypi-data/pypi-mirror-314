#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

import logging
import os
import traceback

from PySide6.QtWidgets import QMainWindow, QApplication, QFrame, QWidget, QVBoxLayout, QSplitter, QGridLayout
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QFileDialog, QMessageBox

from PreDoCS.ResultsViewer.views import ElementLoadStateView, MaterialDistributionStateView
from PreDoCS.ResultsViewer.ui.MainWindow_ui import Ui_MainWindow
from lightworks.opti.optimisation_interface import OptimisationInterface


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.filename = ''
        self.solver = None

        # self.settings_layout = QGridLayout()
        # self.plotSettingsWidget.setLayout(self.settings_layout)
        # self.plot_layout = QGridLayout()
        # self.plotWidget.setLayout(self.plot_layout)

        self._views = [
            MaterialDistributionStateView(self),
            ElementLoadStateView(self),
        ]

        for view in self._views:
            self.plotTypeComboBox.addItem(view.title, view)
            self.settingsStackedWidget.addWidget(view.settings_widget)
            self.plotsStackedWidget.addWidget(view.plot_widget)
        self.plotTypeComboBox.currentIndexChanged.connect(self.plot_type_changed)
        self.plot_type_changed()

        self.actionOpen.triggered.connect(self.action_open)
        self.actionReload.triggered.connect(self.action_reload)
        self.actionClose.triggered.connect(self.action_close)

    #def clear(self):
    #    self.plotSettingsWidget.s

    def plot_type_changed(self):
        view_index = self.plotTypeComboBox.currentIndex()

        self.settingsStackedWidget.setCurrentIndex(view_index)
        self.plotsStackedWidget.setCurrentIndex(view_index)

    def load_file(self, filename: str):
        if os.path.exists(filename):
            try:
                self.filename = filename
                self.setWindowTitle(f'PreDoCS Results Viewer - {filename}')
                structural_model, solver = OptimisationInterface.load(*os.path.split(filename))
                self.solver = solver
                for view in self._views:
                    view.init_view(self.solver)
            except:
                ex_str = traceback.format_exc()
                logging.warning(ex_str)
                QMessageBox.warning(self, 'Open Results File', ex_str)
        else:
            QMessageBox.warning(self, 'Open Results File',
                                self.tr('The file "{}" does not exists.').format(filename))

    def action_reload(self):
        self.load_file(self.filename)

    def action_open(self):
        settings = QSettings()
        last_project_dir = settings.value('last_project_dir', '.')
        file_name, filtr = QFileDialog.getOpenFileName(self, self.tr('Open Results File'),
                                                       dir=last_project_dir,
                                                       filter='PreDoCS Solver Results (*.bin);;All Files (*.*)')
        if file_name:
            self.load_file(file_name)
            settings.setValue('last_project_dir', os.path.split(file_name)[0])

    def action_close(self):
        self.close()

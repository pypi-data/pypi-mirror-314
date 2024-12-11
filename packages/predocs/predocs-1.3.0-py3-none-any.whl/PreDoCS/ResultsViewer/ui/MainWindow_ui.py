# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSplitter,
    QStackedWidget, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionReload = QAction(MainWindow)
        self.actionReload.setObjectName(u"actionReload")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.saveAllPushButton = QPushButton(self.groupBox)
        self.saveAllPushButton.setObjectName(u"saveAllPushButton")

        self.verticalLayout.addWidget(self.saveAllPushButton)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.plotTypeComboBox = QComboBox(self.groupBox)
        self.plotTypeComboBox.setObjectName(u"plotTypeComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.plotTypeComboBox)


        self.verticalLayout.addLayout(self.formLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.plotSettingsGroupBox = QGroupBox(self.widget)
        self.plotSettingsGroupBox.setObjectName(u"plotSettingsGroupBox")
        self.gridLayout_3 = QGridLayout(self.plotSettingsGroupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.plotSettingsWidget = QWidget(self.plotSettingsGroupBox)
        self.plotSettingsWidget.setObjectName(u"plotSettingsWidget")
        self.gridLayout_2 = QGridLayout(self.plotSettingsWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.settingsStackedWidget = QStackedWidget(self.plotSettingsWidget)
        self.settingsStackedWidget.setObjectName(u"settingsStackedWidget")
        self.settingsStackedWidget.setEnabled(True)

        self.gridLayout_2.addWidget(self.settingsStackedWidget, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.plotSettingsWidget, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.plotSettingsGroupBox)

        self.splitter.addWidget(self.widget)
        self.plotsStackedWidget = QStackedWidget(self.splitter)
        self.plotsStackedWidget.setObjectName(u"plotsStackedWidget")
        self.splitter.addWidget(self.plotsStackedWidget)

        self.gridLayout_4.addWidget(self.splitter, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionReload)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)

        self.retranslateUi(MainWindow)

        self.settingsStackedWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PreDoCS Results Viewer", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionReload.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"General", None))
        self.saveAllPushButton.setText(QCoreApplication.translate("MainWindow", u"save all plots", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Plot Type", None))
        self.plotSettingsGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Plot Settings", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi


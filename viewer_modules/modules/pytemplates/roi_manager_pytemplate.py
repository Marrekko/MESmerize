# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'roi_manager_pytemplate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(644, 511)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.dockWidgetContents)
        self.tabWidget.setObjectName("tabWidget")
        self.tabStandard = QtWidgets.QWidget()
        self.tabStandard.setObjectName("tabStandard")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabStandard)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnAddROI = QtWidgets.QPushButton(self.tabStandard)
        self.btnAddROI.setObjectName("btnAddROI")
        self.gridLayout_2.addWidget(self.btnAddROI, 0, 0, 1, 1)
        self.checkBoxShowAllROIs = QtWidgets.QCheckBox(self.tabStandard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxShowAllROIs.sizePolicy().hasHeightForWidth())
        self.checkBoxShowAllROIs.setSizePolicy(sizePolicy)
        self.checkBoxShowAllROIs.setMaximumSize(QtCore.QSize(16777215, 20))
        self.checkBoxShowAllROIs.setChecked(True)
        self.checkBoxShowAllROIs.setObjectName("checkBoxShowAllROIs")
        self.gridLayout_2.addWidget(self.checkBoxShowAllROIs, 1, 0, 1, 2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.tabStandard)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.listwROIs = QtWidgets.QListWidget(self.tabStandard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwROIs.sizePolicy().hasHeightForWidth())
        self.listwROIs.setSizePolicy(sizePolicy)
        self.listwROIs.setMinimumSize(QtCore.QSize(0, 0))
        self.listwROIs.setMaximumSize(QtCore.QSize(100, 16777215))
        self.listwROIs.setObjectName("listwROIs")
        self.verticalLayout_2.addWidget(self.listwROIs)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.tabStandard)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.listwROIDefs = QtWidgets.QListWidget(self.tabStandard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwROIDefs.sizePolicy().hasHeightForWidth())
        self.listwROIDefs.setSizePolicy(sizePolicy)
        self.listwROIDefs.setMinimumSize(QtCore.QSize(0, 0))
        self.listwROIDefs.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listwROIDefs.setObjectName("listwROIDefs")
        self.verticalLayout.addWidget(self.listwROIDefs)
        self.gridLayout_2.addLayout(self.verticalLayout, 2, 1, 1, 1)
        self.lineEdROIDef = QtWidgets.QLineEdit(self.tabStandard)
        self.lineEdROIDef.setObjectName("lineEdROIDef")
        self.gridLayout_2.addWidget(self.lineEdROIDef, 3, 0, 1, 2)
        self.BtnSetROIDefs = QtWidgets.QPushButton(self.tabStandard)
        self.BtnSetROIDefs.setObjectName("BtnSetROIDefs")
        self.gridLayout_2.addWidget(self.BtnSetROIDefs, 4, 0, 1, 2)
        self.tabWidget.addTab(self.tabStandard, "")
        self.tabMetaROI = QtWidgets.QWidget()
        self.tabMetaROI.setObjectName("tabMetaROI")
        self.tabWidget.addTab(self.tabMetaROI, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "ROI Manager"))
        self.btnAddROI.setText(_translate("DockWidget", "Add ROI"))
        self.checkBoxShowAllROIs.setToolTip(_translate("DockWidget", "Show all ROIs or just the one selected from the list"))
        self.checkBoxShowAllROIs.setText(_translate("DockWidget", "Show all on image"))
        self.label.setText(_translate("DockWidget", "ROIs"))
        self.listwROIs.setToolTip(_translate("DockWidget", "ARRAYS START AT ZERO!"))
        self.label_2.setText(_translate("DockWidget", "Tags"))
        self.listwROIDefs.setToolTip(_translate("DockWidget", "ROI Definitions pulled from your config file.\n"
"To add more definitions go to Main Menu -> Edit -> Project Configuration"))
        self.lineEdROIDef.setPlaceholderText(_translate("DockWidget", "Add Tag to ROI Definition"))
        self.BtnSetROIDefs.setText(_translate("DockWidget", "Set ROI tag"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabStandard), _translate("DockWidget", "Standard ROIs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMetaROI), _translate("DockWidget", "Meta ROIs"))


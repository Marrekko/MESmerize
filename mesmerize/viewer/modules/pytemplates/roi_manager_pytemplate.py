# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_files/roi_manager_pytemplate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(393, 536)
        DockWidget.setMinimumSize(QtCore.QSize(393, 412))
        DockWidget.setFloating(True)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.dockWidgetContents)
        self.tabWidget.setObjectName("tabWidget")
        self.tabStandard = QtWidgets.QWidget()
        self.tabStandard.setObjectName("tabStandard")
        self.gridLayout = QtWidgets.QGridLayout(self.tabStandard)
        self.gridLayout.setObjectName("gridLayout")
        self.btnAddROI = QtWidgets.QPushButton(self.tabStandard)
        self.btnAddROI.setObjectName("btnAddROI")
        self.gridLayout.addWidget(self.btnAddROI, 2, 0, 1, 1)
        self.checkBoxShowAll = QtWidgets.QCheckBox(self.tabStandard)
        self.checkBoxShowAll.setObjectName("checkBoxShowAll")
        self.gridLayout.addWidget(self.checkBoxShowAll, 2, 1, 1, 1)
        self.checkBoxLivePlot = QtWidgets.QCheckBox(self.tabStandard)
        self.checkBoxLivePlot.setObjectName("checkBoxLivePlot")
        self.gridLayout.addWidget(self.checkBoxLivePlot, 2, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.tabStandard)
        self.label.setMaximumSize(QtCore.QSize(16777215, 75))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidgetROIs = QtWidgets.QListWidget(self.tabStandard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetROIs.sizePolicy().hasHeightForWidth())
        self.listWidgetROIs.setSizePolicy(sizePolicy)
        self.listWidgetROIs.setMinimumSize(QtCore.QSize(50, 0))
        self.listWidgetROIs.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.listWidgetROIs.setFont(font)
        self.listWidgetROIs.setObjectName("listWidgetROIs")
        self.verticalLayout.addWidget(self.listWidgetROIs)
        self.gridLayout.addLayout(self.verticalLayout, 4, 0, 1, 1)
        self.verticalLayoutTags = QtWidgets.QVBoxLayout()
        self.verticalLayoutTags.setObjectName("verticalLayoutTags")
        self.label_2 = QtWidgets.QLabel(self.tabStandard)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayoutTags.addWidget(self.label_2)
        self.listWidgetROITags = QtWidgets.QListWidget(self.tabStandard)
        self.listWidgetROITags.setObjectName("listWidgetROITags")
        self.verticalLayoutTags.addWidget(self.listWidgetROITags)
        self.gridLayout.addLayout(self.verticalLayoutTags, 4, 1, 1, 5)
        self.lineEditROITag = ROITagLineEdit(self.tabStandard)
        self.lineEditROITag.setObjectName("lineEditROITag")
        self.gridLayout.addWidget(self.lineEditROITag, 5, 0, 1, 6)
        self.btnSetROITag = QtWidgets.QPushButton(self.tabStandard)
        self.btnSetROITag.setObjectName("btnSetROITag")
        self.gridLayout.addWidget(self.btnSetROITag, 6, 0, 1, 6)
        self.btnPlot = QtWidgets.QPushButton(self.tabStandard)
        self.btnPlot.setObjectName("btnPlot")
        self.gridLayout.addWidget(self.btnPlot, 2, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 5, 1, 1)
        self.btnSwitchToManualMode = QtWidgets.QPushButton(self.tabStandard)
        self.btnSwitchToManualMode.setEnabled(False)
        self.btnSwitchToManualMode.setObjectName("btnSwitchToManualMode")
        self.gridLayout.addWidget(self.btnSwitchToManualMode, 3, 2, 1, 2)
        self.pushButtonImportFromImageJ = QtWidgets.QPushButton(self.tabStandard)
        self.pushButtonImportFromImageJ.setObjectName("pushButtonImportFromImageJ")
        self.gridLayout.addWidget(self.pushButtonImportFromImageJ, 3, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.tabStandard)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tabStandard)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.horizontalSliderSpotSize = QtWidgets.QSlider(self.tabStandard)
        self.horizontalSliderSpotSize.setMinimum(1)
        self.horizontalSliderSpotSize.setMaximum(20)
        self.horizontalSliderSpotSize.setPageStep(1)
        self.horizontalSliderSpotSize.setProperty("value", 1)
        self.horizontalSliderSpotSize.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderSpotSize.setObjectName("horizontalSliderSpotSize")
        self.gridLayout.addWidget(self.horizontalSliderSpotSize, 1, 0, 1, 4)
        self.tabWidget.addTab(self.tabStandard, "")
        self.tabMetaROI = QtWidgets.QWidget()
        self.tabMetaROI.setObjectName("tabMetaROI")
        self.tabWidget.addTab(self.tabMetaROI, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        self.tabWidget.setCurrentIndex(0)
        self.lineEditROITag.returnPressed.connect(self.btnSetROITag.click)
        self.horizontalSliderSpotSize.valueChanged['int'].connect(self.label_4.setNum)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "&ROI Manager"))
        self.btnAddROI.setText(_translate("DockWidget", "Add ROI"))
        self.checkBoxShowAll.setText(_translate("DockWidget", "Show all"))
        self.checkBoxLivePlot.setText(_translate("DockWidget", "Live plot"))
        self.label.setText(_translate("DockWidget", "ROIs"))
        self.label_2.setText(_translate("DockWidget", "Tags"))
        self.lineEditROITag.setPlaceholderText(_translate("DockWidget", "Add Tag to ROI Definition"))
        self.btnSetROITag.setText(_translate("DockWidget", "Set ROI tag"))
        self.btnPlot.setText(_translate("DockWidget", "Plot"))
        self.btnSwitchToManualMode.setText(_translate("DockWidget", "Switch to manual mode"))
        self.pushButtonImportFromImageJ.setText(_translate("DockWidget", "Import from ImageJ"))
        self.label_3.setText(_translate("DockWidget", "Spot size"))
        self.label_4.setText(_translate("DockWidget", "1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabStandard), _translate("DockWidget", "Standard ROIs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMetaROI), _translate("DockWidget", "Meta ROIs"))

from ..roi_manager_modules.roi_tag_line_edit import ROITagLineEdit

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 13 2018

@author: kushal

Chatzigeorgiou Group
Sars International Centre for Marine Molecular Biology

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
"""

from .common import ViewerInterface
from pyqtgraphCore.Qt import QtCore, QtGui, QtWidgets
from .pytemplates.roi_manager_pytemplate import *
import numpy as np
from MesmerizeCore import configuration
from MesmerizeCore.packager import viewerWorkEnv
from pyqtgraphCore.graphicsItems import ROI


class ModuleGUI(ViewerInterface, QtWidgets.QDockWidget):
    def __init__(self, parent, viewer_ref):
        ViewerInterface.__init__(self,  viewer_ref)

        QtWidgets.QDockWidget.__init__(self, parent)
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)

    def add_roi(self, load=None):
        self.workEnv_changed()

        self.vi.viewer_ref.workEnv.ROIList.append(ROI.PolyLineROI([[0,0], [10,10], [30,10]],
                                                closed=True, pos=[0,0], removable=True))

        self.vi.viewer_ref.workEnv.ROIList[-1].tags = dict.fromkeys(configuration.cfg.options('ROI_DEFS'), '')

        curve = self.vi.viewer_ref.ui.roiPlot.plot()
        self.vi.viewer_ref.workEnv.CurvesList.append(curve)

        self.vi.viewer_ref.workEnv.CurvesList[-1].setZValue(len(self.workEnv.CurvesList))
        # Just some plot initializations, these are these from the original pyqtgraph ImageView class
        self.vi.viewer_ref.ui.roiPlot.setMouseEnabled(True, True)
        self.vi.viewer_ref.ui.splitter.setSizes([self.height() * 0.6, self.height() * 0.4])
        self.vi.viewer_ref.ui.roiPlot.show()

        # Connect signals to the newly created ROI
        self.vi.viewer_ref.workEnv.ROIList[-1].sigRemoveRequested.connect(self.delROI)
        self.vi.viewer_ref.workEnv.ROIList[-1].sigRemoveRequested.connect(self._workEnv_changed)
        self.vi.viewer_ref.workEnv.ROIList[-1].sigRegionChanged.connect(
            self.updatePlot)  # This is how the curve is plotted to correspond to this ROI
        self.vi.viewer_ref.workEnv.ROIList[-1].sigRegionChanged.connect(self._workEnv_changed)
        self.vi.viewer_ref.workEnv.ROIList[-1].sigHoverEvent.connect(self.boldPlot)
        self.vi.viewer_ref.workEnv.ROIList[-1].sigHoverEvent.connect(self.setSelectedROI)
        self.vi.viewer_ref.workEnv.ROIList[-1].sigHoverEnd.connect(self.resetPlot)

        # Add the ROI to the scene so it can be seen
        self.vi.viewer_ref.view.addItem(self.workEnv.ROIList[-1])

        if load is not None:
            self.vi.viewer_ref.workEnv.ROIList[-1].setState(load)

        self.vi.viewer_ref.ui.listwROIs.addItem(str(len(self.workEnv.ROIList) - 1))
        #        self.ROIlist.append(self.polyROI)
        #        d = self.ROItagDict.copy()
        #        self.ROItags.append(d)
        # Update the plot to include this ROI which was just added
        self.vi.viewer_ref.updatePlot(len(self.workEnv.ROIList) - 1)
        self.vi.viewer_ref.ui.listwROIs.setCurrentRow(len(self.workEnv.ROIList) - 1)
        # So that ROI.tags is never = {}, which would result in NaN's
        self.vi.viewer_ref.setSelectedROI(len(self.workEnv.ROIList) - 1)

    def add_roi_tag(self):
        pass

    def add_roi_tags_list_text(self):
        pass

    def set_selected_roi(self):
        pass

    def show_all_rois(self):
        pass

    def del_roi(self):
        pass

    def update_plot(self):
        pass

    def bold_plot(self):
        pass

    def reset_plot(self):
        pass

    def plot_all(self):
        pass

#!/usr/bin/env python

#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

__all__ = ["StatisticsTool"]

from datetime import datetime

import numpy as np
from taurus.external.qt import Qt
from taurus.external.qt.QtWidgets import QCheckBox, QVBoxLayout, \
    QSplitter, QWidget, QGridLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QLabel, QDateTimeEdit
from taurus.qt.qtgui.container import TaurusWidget
from taurus_pyqtgraph.taurusplotdataitem import TaurusPlotDataItem


class StatisticsTool(Qt.QAction):
    """
    This tool inserts an action in the menu of the :class:`pyqtgraph.PlotItem`
    to which it is attached to show statistics like
    min, max, mean, std, rms of curves.It is implemented as an Action,
    and provides a method to attach it to a
    PlotItem.
    """

    def __init__(self, parent=None, itemClass=None):
        Qt.QAction.__init__(self, "Calculate statistics", parent)
        self.parent = parent
        self.triggered.connect(self._onTriggered)
        self.plotItem = None
        self.legend = None
        if itemClass is None:
            itemClass = TaurusPlotDataItem
        self.itemClass = itemClass

    def attachToPlotItem(self, plot_item, parentWidget=None):
        """
        Use this method to add this tool to a plot

        :param plot_item: (PlotItem)
        """
        self.plotItem = plot_item
        if self.plotItem.legend is not None:
            self.legend = self.plotItem.legend

        menu = self.plotItem.getViewBox().menu
        menu.addAction(self)
        self.setParent(parentWidget or menu)

    def _onTriggered(self):
        StatisticsToolDlg.display(self.parent, self.plotItem.listDataItems())


class StatisticsToolDlg(TaurusWidget):
    def __init__(self, parent, data_items):
        super().__init__()

        self.parent = parent
        self.dataItems = data_items

        self.layout = QVBoxLayout()

        self.splitter = QSplitter()

        self.setupXLimitsFragment()
        self.setupStatsPickerFragment()
        self.setupTableFragment()

        self.calculateButton = QPushButton('(re)calculate')
        self.calculateButton.clicked.connect(lambda _: self.fillTable())

        self.layout.addWidget(self.calculateButton)
        self.setLayout(self.layout)

    def setupXLimitsFragment(self):
        """Method to setup the x_limits fragment of the StatisticalToolDlg."""
        self.xLimitsWidget = QWidget()
        self.xLimitsLayout = QGridLayout()

        self.checkboxMin = QCheckBox('min')
        self.checkboxMin.clicked.connect(lambda _: self.inputMin.setDisabled(
            not self.checkboxMin.isChecked()))
        self.inputMin = QDateTimeEdit()
        self.inputMin.setDisplayFormat("yyyy-MM-dd'T'HH:mm:ss.zzz")
        self.inputMin.setDateTime(
            datetime.fromtimestamp(self._get_min_range()))
        self.inputMin.setDisabled(True)
        self.xLimitsLayout.addWidget(QLabel("X limits"))
        self.xLimitsLayout.addWidget(self.checkboxMin, 1, 0)
        self.xLimitsLayout.addWidget(self.inputMin, 1, 1)

        self.checkboxMax = QCheckBox('max')
        self.checkboxMax.clicked.connect(lambda _: self.inputMax.setDisabled(
            not self.checkboxMax.isChecked()))
        self.inputMax = QDateTimeEdit()
        self.inputMax.setDisplayFormat("yyyy-MM-dd'T'HH:mm:ss.zzz")
        self.inputMax.setDateTime(
            datetime.fromtimestamp(self._get_max_range()))
        self.inputMax.setDisabled(True)
        self.xLimitsLayout.addWidget(self.checkboxMax, 2, 0)
        self.xLimitsLayout.addWidget(self.inputMax, 2, 1)

        self.xLimitsWidget.setLayout(self.xLimitsLayout)

        self.layout.addWidget(self.xLimitsWidget)

    def setupStatsPickerFragment(self):
        """
        Method to setup the stats_picker fragment of the StatisticalToolDlg.
        """
        self.statsPickerWidget = QWidget()
        self.statsPickerLayout = QGridLayout()
        self.statsCheckboxes = []

        self.statsPickerLayout.addWidget(QLabel("Stats"), 0, 0)

        self.stats = ["points", "min", "max", "mean", "std", "rms"]
        for i, stat in enumerate(self.stats):
            check_box = QCheckBox(stat)
            check_box.setChecked(True)
            check_box.clicked.connect(
                lambda checked, col=i:
                self.tableWidget.setColumnHidden(col, not checked)
            )
            self.statsPickerLayout.addWidget(check_box, 1, i)
            self.statsCheckboxes.append(check_box)

        self.statsPickerWidget.setLayout(self.statsPickerLayout)
        self.layout.addWidget(self.statsPickerWidget)

    def setupTableFragment(self):
        """Method to setup the table fragment of the StatisticalToolDlg."""
        self.tableWidget = QTableWidget(0, 0)

        self.fillTable()

        self.layout.addWidget(self.tableWidget)

    def fillTable(self):
        """Method to fill the table of the StatisticalToolDlg."""
        start = float("-inf")
        end = float("inf")
        if self.checkboxMin.isChecked():
            start = float(
                datetime.fromisoformat(self.inputMin.text()).timestamp())
        else:
            self.inputMin.setDateTime(
                datetime.fromtimestamp(self._get_min_range()))

        if self.checkboxMax.isChecked():
            end = float(
                datetime.fromisoformat(self.inputMax.text()).timestamp())
        else:
            self.inputMax.setDateTime(
                datetime.fromtimestamp(self._get_max_range()))

        rows = [item for item in self.dataItems if item.name()]
        columns = []
        for idx, item in enumerate(self.statsCheckboxes):
            if item.isChecked():
                columns.append(self.stats[idx])

        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setRowCount(len(rows))

        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.tableWidget.setVerticalHeaderLabels(
            [item.name() for item in rows])

        for x in range(len(rows)):
            for y in range(len(columns)):
                item = rows[x]
                if item.xData is not None and item.yData is not None:
                    yData = [y for _, y in
                             filter(lambda item: start < item[0] < end,
                                    zip(item.xData, item.yData))]
                    xData = [x for x in
                             filter(lambda x: start < x < end, item.xData)]
                else:
                    yData, xData = None, None

                yStat = self.calcStat(columns[y], yData)
                if columns[y] in ["min", "max"]:
                    xStat = self.calcStat(columns[y], xData, time=True)
                    if xStat is not None:
                        self.tableWidget.setItem(x, y, QTableWidgetItem(
                            "t={}\ny={}".format(xStat, yStat)))
                    else:
                        self.tableWidget.setItem(x, y, QTableWidgetItem(""))
                else:
                    if yStat is not None:
                        self.tableWidget.setItem(x, y, QTableWidgetItem(
                            "{:g}".format(yStat)))
                    else:
                        self.tableWidget.setItem(x, y, QTableWidgetItem(""))
        self.tableWidget.resizeRowsToContents()

    def calcStat(self, stat, data, time=False):
        """Method to calculate the statistics for the given data."""
        if data is None or not len(data):
            return None
        else:
            return {
                'points': len(data),
                'min': datetime.fromtimestamp(
                    min(data)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                if time else min(data),
                'max': datetime.fromtimestamp(
                    max(data)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                if time else max(data),
                'mean': np.mean(data),
                'std': np.std(data) if len(data) >= 2 else None,
                'rms': np.sqrt(np.mean(np.array(data) ** 2)),
            }[stat]

    def _get_min_range(self):
        return min([min(curve.xData) for curve in self.dataItems if
                    curve.xData is not None])

    def _get_max_range(self):
        return max([max(curve.xData) for curve in self.dataItems if
                    curve.xData is not None])

    @staticmethod
    def display(parent, data_items):
        """Static method to display the StatisticalToolDlg."""
        dlg = Qt.QDialog(parent)
        dlg.setWindowTitle("Curve Stats Dialog")
        dlg.setWindowIcon(Qt.QIcon("logos:taurus.png"))
        layout = Qt.QVBoxLayout()
        w = StatisticsToolDlg(
            parent=parent,
            data_items=data_items
        )
        layout.addWidget(w)
        dlg.setLayout(layout)
        dlg.exec_()


def _demo_Statisticaltool():
    import sys
    import numpy
    import pyqtgraph as pg
    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusPlotDataItem

    app = TaurusApplication()

    # a standard pyqtgraph plot_item
    w = pg.PlotWidget()

    # add legend to the plot, for that we have to give a name to plot items
    w.addLegend()

    # adding a regular data item (non-taurus)
    c1 = pg.PlotDataItem(name="st plot", pen="b", fillLevel=0, brush="c")
    c1.setData(numpy.arange(300) / 300.0)
    w.addItem(c1)

    # adding a taurus data item
    c2 = TaurusPlotDataItem(name="st2 plot", pen="r", symbol="o")
    c2.setModel("eval:rand(222)")

    w.addItem(c2)

    # attach to plot item
    tool = StatisticsTool(itemClass=TaurusPlotDataItem)
    tool.attachToPlotItem(w.getPlotItem())

    w.show()

    tool.trigger()

    sys.exit(app.exec_())


if __name__ == "__main__":
    _demo_Statisticaltool()

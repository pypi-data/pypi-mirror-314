import csv
from datetime import datetime
import itertools
import os

import numpy as np
from pyqtgraph.exporters.CSVExporter import Exporter, PlotItem
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.widgets.FileDialog import FileDialog


LastExportDirectory = None


class Taurus4TextExporter(Exporter):
    """
    Attempt to imitate the data export format used for taurustrend in Taurus 4
    (and maybe older). Tab separated values, with (somewhat) ISO timestamps
    and a two line info header

    # DATASET= "tango://tangohost:10000/sys/tg_test/1/double_scalar[0]"
    # SNAPSHOT_TIME= 2024-01-31_10:22:59.803364
    2024-01-31_10:21:50.839317      -214.70028819767657
    2024-01-31_10:21:53.840938      -193.20642255951807
    2024-01-31_10:21:56.840750      -181.02017659616354

    Note that Taurus4 did not support exporting if there several attributes in
    a single file, but instead wrote to several files called set001.dat, ...
    """
    Name = "Taurus 4 compatible ASCII export"
    windows = []

    def __init__(self, item):
        Exporter.__init__(self, item)

        self.index_counter = itertools.count(start=0)
        self.data = []
        self.models = []

    def parameters(self):
        return None

    def fileSaveDialog(self, filter=None, opts=None,
                       mode=QtWidgets.QFileDialog.FileMode.AnyFile):
        # Overriding the default method to allow setting the mode
        if opts is None:
            opts = {}
        self.fileDialog = FileDialog()
        self.fileDialog.setFileMode(mode)
        self.fileDialog.setAcceptMode(
            QtWidgets.QFileDialog.AcceptMode.AcceptSave)
        if filter is not None:
            if isinstance(filter, str):
                self.fileDialog.setNameFilter(filter)
            elif isinstance(filter, list):
                self.fileDialog.setNameFilters(filter)
        global LastExportDirectory
        exportDir = LastExportDirectory
        if exportDir is not None:
            self.fileDialog.setDirectory(exportDir)
        self.fileDialog.show()
        self.fileDialog.opts = opts
        self.fileDialog.fileSelected.connect(self.fileSaveFinished)

    def _exportPlotDataItem(self, plotDataItem) -> None:
        if hasattr(plotDataItem, 'getOriginalDataset'):
            # try to access unmapped, unprocessed data
            cd = plotDataItem.getOriginalDataset()
        else:
            # fall back to earlier access method
            cd = plotDataItem.getData()
        if cd[0] is not None:
            # data found, append it
            self.data.append(cd)

    @staticmethod
    def _format_row(row):
        for i, item in enumerate(row):
            if item and i % 2 == 0:
                yield datetime.fromtimestamp(item).isoformat(sep="_")
                continue
            if isinstance(item, str):
                yield item
                continue
            yield np.format_float_positional(item, precision=10)

    def export(self, fileName=None):
        if not isinstance(self.item, PlotItem):
            raise TypeError("Must have a PlotItem selected for CSV export.")

        if not self.data:
            for item in self.item.items:
                if hasattr(item, "getFullModelName"):
                    self.models.append(item.getFullModelName())
                if hasattr(item, 'implements') and item.implements('plotData'):
                    self._exportPlotDataItem(item)

        single = len(self.data) == 1

        if fileName is None:
            if single:
                self.fileSaveDialog(filter=["*.csv", "*.tsv"])
            else:
                # For multiple attributes, the Taurus 4 behavior is
                # to ask for a directory
                self.fileSaveDialog(
                    mode=QtWidgets.QFileDialog.FileMode.Directory)
        else:
            for i, (model, dataset) in enumerate(zip(self.models, self.data),
                                                 start=1):
                if single:
                    path = fileName
                else:
                    path = os.path.join(fileName, f"set{i:03}.dat")
                print("Saving {} at {}".format(model, path))
                with open(path, 'w', newline='') as csvfile:
                    # Write "Taurus 4 like" header
                    # TODO what does the [0] mean here?
                    csvfile.write(f'# DATASET= "{model}[0]"\n')
                    snapshot_time = datetime.now().isoformat(sep="_")
                    csvfile.write(f'# SNAPSHOT_TIME= {snapshot_time}\n')

                    # Write data rows
                    delimiter = "\t"
                    writer = csv.writer(csvfile, delimiter=delimiter,
                                        quoting=csv.QUOTE_MINIMAL)
                    for row in itertools.zip_longest(*dataset, fillvalue=""):
                        writer.writerow(self._format_row(row))

            self.data.clear()


Taurus4TextExporter.register()

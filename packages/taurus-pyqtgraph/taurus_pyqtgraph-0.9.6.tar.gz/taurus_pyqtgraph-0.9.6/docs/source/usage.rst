=======================
How to taurus-pyqtgraph
=======================

Taurus Plot basic usage
-----------------------
A Taurus plot leverages Taurus's capabilities to visualize data.
These plots are often used in scientific and industrial contexts where real-time monitoring of data is crucial.
Taurus plots can display a variety of data types.

**Plot data using the command line:**

1. Open a terminal and type:

.. code-block:: console

    $ taurus plot "eval:Q(rand(333),'mm')"

2. Now repeat the above but add a tango array attribute:

.. code-block:: console

    $ taurus plot "eval:Q(rand(333),'mm')" sys/tg_test/1/wave

As you can see plotting attributes using taurus_pyqtgraph is easy and effortless thanks to the taurus framework.

TaurusTrend basic usage
-----------------------
TaurusTrend is a widget provided by the Taurus framework, specifically designed for plotting time-based data trends in real-time.

**Plot time data using the command line:**

1. Open a terminal and type:

.. code-block:: console

    $ taurus trend "eval:rand()"

2. Now repeat the above but add a tango scalar attribute:

.. code-block:: console

    $ taurus trend "eval:rand()" sys/tg_test/1/double_scalar_rww


Non-programmatic usage
----------------------

**Execute a taurus trend with a random eval and a Tango attribute**
...................................................................

To do it type:

.. code-block:: console

    $ taurus trend "eval:rand()" sys/tg_test/1/double_scalar_rww

**Explore the x_axis menu**
...........................
 .. image:: imgs/x_axis.png
    :alt: X axis Submenu

1. Make a right-click on the taurus trend and select 'X axis' submenu on the contextual menu.
2. A description on the functions can be read at the final of this exercise.
3. You can modify the time range you want to look at by doing it manually on the 'Manual' option or even better, using the 'Set View Range' editable dropdown menu. This dropdown menu have some predefined values, but you can edit it to the time you want by following the convention, don't worry if you make a syntax mistake there will be a message box with the syntax expected. Try to set the range to 5 minutes.
4. The time range option can be found on the plot configuration menu as well.

***Options on the X_axis submenu:***

 + Fixed range scale: It fixes the visible time range on the trend in order to keep just a slice of data visible to the user.
 + Manual: It allows to select a customizable time range.
 + Auto: It allows to select the % of data visible to the user, the options 'Visible Data Only' and 'Auto Pan Only' make this % more accurate depending on your needs.
 + Invert Axis: It inverts the axis direction.
 + Mouse Enabled: It prevents the axis to be moved by the mouse.
 + Link Axis: It allows the axis to be moved to a defined ViewBox, by default there is only one.
 + Set View Range: As explained on the exercise you can select predefined time ranges or type a custom one.
 + Log Scale: It allows to set the axis to logarithmic mode, which in that case is not useful, but it could be interesting for some scenarios.


**Explore the y_axis menu**
...........................

 .. image:: imgs/y_axis.png
    :alt: Y axis Submenu

1. Make a right-click on the taurus trend and select 'Y axis' submenu on the contextual menu.
2. A description on the functions can be read at the final of this exercise.
3. Select the option 'Log Scale'. You will see that data is now represented with a logarithmic scale (the gaps on the tango attribute are normal due to the fact that log(0) is not a valid operation)
4. Now deselect 'Log Scale' to restore the visualization.

***Options on the Y_axis submenu:***

 + Manual: It allows to select a customizable range between the values.
 + Auto: It allows to select the % of data visible to the user, the options 'Visible Data Only' and 'Auto Pan Only' make this % more accurate depending on your needs.
 + Invert Axis: It the axis direction.
 + Mouse Enabled: It prevents the axis to be moved by the mouse.
 + Link Axis: It allows the axis to be moved to a defined ViewBox, by default there is only one.
 + Log Scale: It allows to set the axis to logarithmic mode, which in that case is not useful, but it could be interesting for some scenarios.


**Explore the mouse mode option**
.................................
 .. image:: imgs/mouse_mode.png
    :alt: Example on how to use the 1 button mode for the mouse

1. Make a right-click on the taurus trend and select 'Mouse mode' submenu on the contextual menu.
2. Here you have two options, the 3 button mode and the 1 button mode, try it out, explanation can be found at the end of this exercise.
3. For the rest of the session set it to 3 button mode.

***Options on the mouse mode submenu:***

 + 3 button: Acts with drag mode, you can drag the trend or the plot to the direction you want.
 + 1 button: Acts with a range selector, you can select what data you can view with a rectangular selection.


**Explore the Change curves titles option**
...........................................

 .. image:: imgs/change_titles.png
    :alt: Change curves titles option

1. Make a right-click on the taurus trend and select 'Change curves titles' submenu on the contextual menu.
2. A pop-up will appear with an editable dropdown, you can use the patterns from the dropdown and combine some of them. In this case type: _{dev.name}/{attr.label}_
3. You will notice that the legend has changed.
4. You can modify the curves titles from the 'Model selection' menu.

**Explore the model selection tool**
....................................

The model selection tool in taurus_pyqtgraph works the same way as Taurus, you can have a look at the Taurus exercises for more information.
However, we have some extra options in the case of taurus plot and taurus trend.

 .. image:: imgs/model_selector.png
    :alt: Model selection window

1. Make a right-click on the taurus trend and select 'Model selection tool' submenu on the contextual menu.
2. The left part of the window is the source data selector, this has been explained at the taurus exercises, but the right part is unique for taurus trend and taurus plot.
3. You can see that we have the source and the title of each curve, you can add, delete and edit curves.
4. Here you can change the curves titles by clicking the 'Change Curves Titles' button, the functionality is the same as the one that is at the contextual menu.


**Explore the calculate statistics option**
...........................................

 .. image:: imgs/calculate_statistics.png
    :alt: Calculate statistics option


1. Make a right-click on the taurus trend and select 'Calculate Statistics' option on the contextual menu.
2. Here you can explore all the statistics calculated for each curve that you have on your taurus trend.
3. Try to hide some of them by clicking on the checkbox.
4. Anytime you can re-calculate the statistics by clicking on the bottom button.

**Explore the plot configuration option**
.........................................

 .. image:: imgs/plot_configuration.png
    :alt: Plot configuration option


1. Make a right-click on the taurus trend and select the 'Plot Configuration' option on the contextual menu.
2. Try to change the line style of one of the curves, by clicking on the desired curve and using the dropdown menu.
3. Try to change the color, and style of symbols and click the apply button under the curves.
4. Now open the plot configuration again, select the first curve and change the axis to Y2, then click apply and close the window.
5. You will see that now the curves are separated and you will have 2 axis, like the image below:

 .. image:: imgs/different_axis.png
    :alt: Curves on different axis

Play with all the other options to modify the trend to you needs, there are a lot of options.

**Explore the Data inspector mode**
...................................

 .. image:: imgs/data_inspector.png
    :alt: Data inspector mode


1. Make a right-click on the taurus trend and select 'Data inspector' checkbox on the contextual menu.
2. If you move the mouse along the curves you will see a tooltip for each curve and point that it has.
3. To disable the inspector mode you have to deselect the 'Data inspector' checkbox on the contextual menu.

**Explore Change forced read period option**
............................................

 .. image:: imgs/change_read_period.png
    :alt: Change force read period pop-up


The force reading period refers to the interval at which the library forcibly reads data from the data source, even if there hasn't been an explicit change or event triggering a read.
With this option we can control the amount of points that are plotted.

1. Make a right-click on the taurus trend and select 'Change forced read period' option on the contextual menu.
2. A pop-up will appear, then you can type the 'polling period' and click 'OK', for testing purposes type 500.
3. Every half a second a new point will appear.
4. If you want to disable it type 0 again and the polling will be disabled.

**Explore Change buffers size option**
......................................

 .. image:: imgs/change_buffer.png
    :alt: Change buffer size pop-up


The buffer data size is the maximum number of points that will be kept in memory for each curve.

1. Make a right-click on the taurus trend and select 'Change buffers size' option on the contextual menu.
2. Change the buffers size to 500, you will see that the number of points will be decreased once the limit is reached.

**Explore the Export tool**
...........................

.. image:: imgs/export.png
    :alt: Export data pop up


The export option is designed to transform the plot to other formats, a detailed list of formats can be found at the end of this exercise.

1. Make a right-click on the taurus trend and select 'Export' option on the contextual menu.
2. Select the item named 'Plot'.
3. Select the option 'CSV' on 'Export format'.
4. Click the export button, you will be prompted with the desired path to store the csv file.
5. Open the file and check that the csv file has been generated correctly.

 .. image:: imgs/export_result.png
    :alt: Visualize the result of the export

***Options on the export tool:***

 + CSV: It exports the data using comma separated values to a file. It can be configured to change the separator and the precission.
 + HDF5: It exports the data using the HDF5 file format.
 + Matplotlib Window: It shows the data with matplotlib.
 + SVG: It exports the data using an image in the SVG format. (Not working properly right now) `#129`_
 + ASCII: It exports the data using the Taurus 4 compatible ASCII format.

**Real use case for monitoring memory usage of a process**
..........................................................

Combining taurus trend with eval we can get the memory usage and get a trend with the current status.

 .. image:: imgs/example_1.png
    :alt: Monitor the memory usage of a process using eval

1. First of all select a running process id from the ones that are running on your pc, to do it you can type
top and anotate the one that has more memory usage for example.
2. Now that you have the PID of the process you want to monitor, you can monitor the memory usage by typing:

.. code-block:: console

    $ taurus trend -r500 "eval:@psutil.*/Process(REPLACE_THIS_BY_PID).memory_info().rss/2**10"`

**Real use case integrating  archiving**
........................................

Taurus trend has the possibility to plot archiving data by selecting it on the contextual menu, but this option just appears if you have `PyHDB++`_ installed and configured.

The Archiving menu have the following options:
 - Autoreload: If enabled, Taurus Trend will load data on the fly by moving the DateTime axis to the left.
 - Load Once (Ctrl+L): It loads the data for the current time window.
 - Decimate and Redraw (Ctrl+R): It will discard the current data and redraw data from archiving
   but decimating to have less resolution. (If you zoom in and click this option you will have more resolution)
 - Configure decimation: It shows a dialog to configure decimation for the queries to PyHDB++.

Here you can see a GIF with the archiving option working, and if you want to have a look at it you can check out the `TangoBox OVA`_ and this `TangoBox issue`_ to check how to configure it.

 .. image:: imgs/archiving_trend.gif
    :alt: Taurus Trend with archiving properly configured and requesting past data

**Extra tip: Auto arrange symbol**
..................................

Did you notice the small button at the left-bottom of the taurus trend or taurus plot?

If you click on it the widget will make the data fit on the widget.

Programmatic usage
------------------

**Open a Taurus Plot programmatically**
.......................................

To open a Taurus Plot programmatically you need the following, take into account that a TaurusApplication or a
QApplication (from PyQt) is needed to be able to render the plot

.. code-block:: python

    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusPlot

    app = TaurusApplication()

    plot = TaurusPlot()
    plot.setWindowTitle("My Taurus Plot")
    plot.show()

    app.exec_()



**Add raw data to a Taurus Plot programmatically**
..................................................

1. Create a TaurusApplication and the TaurusPlot object

.. code-block:: python

    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusPlot, TaurusPlotDataItem
    app = TaurusApplication()
    plot = TaurusPlot()
    plot.setWindowTitle("My Taurus Plot")
    plot.show()

2. Add data to the plot using the TaurusPlotDataItem object, and execute the application

.. code-block:: python

    x, y = [[1, 2, 3, 4, 5], [11, 12, 13, 14, 15]]

    # If you want the curve to have a name and color then define name and, pen.
    item = TaurusPlotDataItem(name="Curve1", pen="b")
    item.setData(x=x, y=y)

    plot.addItem(item)

    app.exec_()


You can have as many Curves as you want:

.. code-block:: python

    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusPlot, TaurusPlotDataItem

    app = TaurusApplication()

    plot = TaurusPlot()
    plot.setWindowTitle("My Taurus Plot")
    plot.show()

    x, y = [[1, 2, 3, 4, 5], [11, 12, 13, 14, 15]]

    # If you want the curve to have a name and color then define name and, pen.
    item1 = TaurusPlotDataItem(name="Curve1", pen="b") # Curve 1 blue
    item1.setData(x=x, y=y)

    x, y = [[1, 2, 3, 4, 5], [5, 10, 0, -5, -10]]

    item2 = TaurusPlotDataItem(name="Curve2", pen="r") # Curve 2 red
    item2.setData(x=x, y=y)


    # Add the items to the plot
    plot.addItem(item1)
    plot.addItem(item2)

    app.exec_()

Since taurus_pyqtgraph inherits its functionality from pyqtgraph you can have a complete list of what
TaurusPlotDataItem can accept as an argument from its parent `PlotDataItem`_.

**Using models with Taurus Plot programmatically**
..................................................

We have seen that we can plot data from Tango or other data sources by calling the command line and
passing the model as arguments, but we can also do it programmatically with setModel or addModels methods.

.. code-block:: python

    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusPlot

    app = TaurusApplication()

    plot = TaurusPlot()
    plot.setWindowTitle("My Taurus Plot")
    plot.show()

    plot.setModel("sys/tg_test/1/wave")

    app.exec_()

And we can mix different types of data sources, we don't need to stick with one type, for example:

.. code-block:: python

    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusPlot

    app = TaurusApplication()

    plot = TaurusPlot()
    plot.setWindowTitle("My Taurus Plot")
    plot.show()

    plot.setModel("sys/tg_test/1/wave")
    plot.addModels(["eval:Q(rand(333))", "eval:Q(rand(333)+2)"])

    app.exec_()


**Open a Taurus Trend programmatically**
........................................

To open a Taurus Trend programmatically you need the following, take into account that a TaurusApplication or a
QApplication (from PyQt) is needed to be able to render the plot

.. code-block:: python

    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusTrend

    app = TaurusApplication()

    trend = TaurusTrend()
    trend.setWindowTitle("My Taurus Trend")
    trend.show()

    app.exec_()


**Add raw data to a Taurus Plot programmatically**
..................................................

.. code-block:: python

    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusTrend, TaurusTrendSet
    from pyqtgraph import mkPen

    app = TaurusApplication()

    trend = TaurusTrend()
    trend.setWindowTitle("My Taurus Trend")
    trend.show()

    set1 = TaurusTrendSet(name="Curve1")

    x = [1724234271, 1724234273, 1724234276, 1724234278, 1724234285,
         1724234287, 1724234289, 1724234292, 1724234294, 1724234296]

    y = [1, 2, 3, 4, 10, 0, 15, 3, -5, -10]

    set2 = TaurusTrendSet(name="Curve2")

    y2 = [-1, -2, -3, -4, -10, 0, -15, -3, 5, 10]

    set1.setData(x=x, y=y, name="Curve1", pen=mkPen(color="red"))
    set2.setData(x=x, y=y2, name="Curve2", pen=mkPen(color="blue"))

    trend.addItem(set1)
    trend.addItem(set2)

    app.exec_()



For a whole set of parameters that you can set to pen (to customize color, width, symbols, etc)
you can have a look at the `PyQtGraph Style Guide`_.


**Using models with Taurus trend programmatically**
...................................................

Like the Taurus Plot we can set models to a Taurus Trend programmatically too.

.. code-block:: python

    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusTrend

    app = TaurusApplication()

    trend = TaurusTrend()
    trend.setWindowTitle("My Taurus Trend")
    trend.show()

    trend.setModel("sys/tg_test/1/double_scalar")
    trend.addModels(["sys/tg_test/1/ampli", "eval:rand()*10"])

    app.exec_()

Remember that you can mix things using the eval feature of Taurus.
To know more check the `Taurus Core Evaluation`_ documentation.


**Using models with individual curves**
.......................................

1. Create a TaurusApplication and the TaurusTrend object

.. code-block:: python

    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusTrend, TaurusTrendSet

    app = TaurusApplication()

    trend = TaurusTrend()
    trend.setWindowTitle("My Taurus Trend")
    trend.show()

2. Add data to the trend using the TaurusTrendSet object, and execute the application

.. code-block:: python

    set1 = TaurusTrendSet(name="Curve1")
    # In this case we will use a random generator using eval as a model
    set1.setModel("eval:rand()")

    trend.addItem(set1)

    app.exec_()

Like the TaurusPlot we can add as many curves (or trend sets as desired)

.. code-block:: python

    set1 = TaurusTrendSet(name="Curve1", pen=mkPen(color="red"))
    # In this case we will use a random generator using eval as a model
    set1.setModel("eval:rand()")

    set2 = TaurusTrendSet(name="Curve2", pen=mkPen(color="blue"))
    set2.setModel("eval:rand()+2")

    trend.addItem(set1)
    trend.addItem(set2)

    app.exec_()


**Set Taurus Trend to have a Logarithmic Y Axis**
.................................................

You can use the method setAxisLogMode to set the logarithmic mode on the axis of a taurus trend.
Possible options are:

.. code-block:: python

    setAxisLogMode("left", True)
    setAxisLogMode("bottom", True)
    setAxisLogMode("y", True) # The same as left
    setAxisLogMode("x", True) # The same as bottom

Example:

.. code-block:: python

    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusTrend

    app = TaurusApplication()

    trend = TaurusTrend()
    trend.setWindowTitle("My Taurus Trend")
    trend.show()

    trend.setModel("sys/tg_test/1/double_scalar")
    trend.setAxisLogMode("left", True)

    app.exec_()


Custom widget examples
----------------------

**Custom BarGraph Plot using TaurusBaseComponent**
..................................................

`TaurusBaseComponent`_ is a generic Taurus component that can be used to create custom widgets.
It covers the inheritance, parameters, and functions of the TaurusBaseComponent class.
Some important points are that it provides functions for setting the model, displaying the value,
filtering events, and managing the event buffer. It also has functions for getting information about the model,
such as the name, type, and model object. Additionally, it has functions for manipulating the model,
such as setting the model and getting a piece of the model.

Here is a simple example of a customization of Taurus Plot to represent data in bar graph format:

1. Class definition

.. code-block:: python

    from taurus import Attribute
    from taurus.qt.qtgui.base import TaurusBaseComponent
    from pyqtgraph import BarGraphItem


    class TaurusBarGraphItem(TaurusBaseComponent):
        """
        This class aims to simplify the process of generating Bar plots using a tango attribute as data source.
        """

        def __init__(self, name=None, parent=None, design_mode=False, **kwargs):
            """
            Parameters
            ----------
            :param name: Optional name of the plot, this name will be shown on the legend if specified.
            :param parent: Specify the parent, not mandatory and None by default.
            :param design_mode:
            :param kwargs: It is expected from the client to specify the width, pen and brush.
                If not a default value is set.
            """
            super().__init__(name, parent, design_mode, **kwargs)
            opts = dict(
                x=0 if 'x' not in kwargs else kwargs['x'],
                height=0.5 if 'height' not in kwargs else kwargs['height'],
                width=0.5 if 'width' not in kwargs else kwargs['width'],
                brush='b' if 'brush' not in kwargs else kwargs['brush'],
                pen='b' if 'pen' not in kwargs else kwargs['pen'],
                name=name,
            )
            self.bar_graph_item = BarGraphItem(**opts)

        def setModel(self, model, key=None):
            super().setModel(model)
            y = Attribute(model).rvalue.magnitude
            x = [i for i in range(len(y))]
            self.mount_plot(x, y)

        def handleEvent(self, evt_src, evt_type, evt_value):
            """
            Here we define what to do when be received a Tango event.
            """
            super().handleEvent(evt_src, evt_type, evt_value)
            y = evt_value.rvalue
            x = range(len(y))
            self.mount_plot(x, y)

        def mount_plot(self, x, y):
            """
            Sets up the internal bar_graph_item with the data given as parameters.
            """
            opts = dict(
                x=x,
                height=y,
            )
            self.bar_graph_item.setOpts(**opts)

2. Usage

.. code-block:: python

    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    from taurus_pyqtgraph import TaurusPlot, TaurusPlotDataItem

    app = TaurusApplication(sys.argv)

    plot = TaurusPlot()
    plot.setWindowTitle("My Custom Plot")
    plot.show()

    bar_graph = TaurusBarGraphItem(name="Wave", width=0.5, brush='r', pen='r')
    bar_graph.setModel("sys/tg_test/1/wave")

    curve = TaurusPlotDataItem(name="Wave curve", pen="b")
    curve.setModel("sys/tg_test/1/wave")

    plot.addItem(bar_graph.bar_graph_item)  # Here we are adding the bar_graph
    plot.addItem(curve)  # Here we are adding the curve with the same info

    app.exec_()

The result can be seen in the following screenshot

 .. image:: imgs/bar_graph_example.png
    :alt: Custom plot using Taurus Plot represented with bar graph format


Known issues
----------------------
- When using numpy <1.17, trying to add symbols to a curve raises the exception
 "AttributeError: module 'numpy.core.umath' has no attribute 'clip'"

.. _`PyHDB++`: https://gitlab.com/tango-controls/hdbpp/libhdbpp-python
.. _TangoBox OVA: https://gitlab.com/tango-controls/tangobox
.. _TangoBox issue: https://gitlab.com/tango-controls/tangobox/-/issues/57
.. _PlotDataItem: https://pyqtgraph.readthedocs.io/en/latest/api_reference/graphicsItems/plotdataitem.html
.. _Taurus Core Evaluation: https://taurus-scada.org/devel/api/taurus.core.evaluation.html
.. _PyQtGraph Style Guide: https://pyqtgraph.readthedocs.io/en/latest/user_guide/style.html
.. _TaurusBaseComponent: https://taurus-scada.org/devel/api/taurus.qt.qtgui.base-TaurusBaseComponent.html
.. _#129: https://gitlab.com/taurus-org/taurus_pyqtgraph/-/issues/129

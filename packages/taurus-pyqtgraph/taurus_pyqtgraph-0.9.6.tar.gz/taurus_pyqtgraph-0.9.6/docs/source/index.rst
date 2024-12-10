############################################
Taurus_pyqtgraph
############################################

Welcome to Taurus_pyqtgraph's documentation!

This python3 package is designed to extend the capabilities of the Taurus framework,
which is primarily used for controlling and monitoring various systems.
By leveraging the robust visualization tools provided by PyQtGraph,
taurus-pyqtgraph offers a seamless way to create highly customized and interactive
data visualizations within the Taurus environment.

 .. image:: imgs/plot_example.png
     :alt: taurus-pyqtgraph example plot with an attribute

Key aspects:
------------

Taurus-pyqtgraph integrates seamlessly with Taurus, allowing users to:
 - Visualize live data: Data streams from Taurus can be plotted dynamically, providing real-time plots or trends using taurus-compatible attributes.
 - Create custom dashboards: Users can construct personalized trends and integrate those trends on Taurus applications.
 - Analyze historical data: Stored data can be retrieved and visualized for historical analysis by installing and configuring `PyHDB++`_.


Existing application using taurus_pyqtgraph
-------------------------------------------
There are a lot of applications (most of them are on internal repositories), but there is a new one named `TangoBrowser`_ that have been published and can be installed.

Tango browser is a tango and archiving tool to look for attributes in use or ever archived.
This tool is a graphical interface to search tango attributes archived or not.

Due to the fact that this GUI have been developed using taurus you can drag&drop from the list above to the taurus trend and it will start to plot the attribute.

 .. image:: imgs/tango_browser.png
     :alt: TangoBrowser application with a search and a trend with data

Index
------------

.. toctree::
   :maxdepth: 5

   installation
   api
   usage


.. _PyHDB++: https://tango-controls.gitlab.io/hdbpp/libhdbpp-python
.. _TangoBrowser: https://gitlab.com/tango-controls/hdbpp/libhdbpp-tangobrowser

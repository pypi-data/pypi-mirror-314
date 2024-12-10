.. highlight:: shell

============
Installation
============

You can choose your favorite way of installing the package, but after a successful installation,
the module will be accessible as taurus.qt.qtgui.tpg and taurus_pyqtgraph.
Furthermore, tpg will be registered as an alternative implementation for plots and trends in the taurus CLI.


Installation from PyPi Stable release
-------------------------------------

To install taurus_pyqtgraph, run this command in your terminal:

.. code-block:: console

    $ pip install taurus_pyqtgraph # Without installing Archiving Pyhdb++ support


If you rather prefer to install the taurus_pyqtgraph package with archiving support enabled then run this command:

.. code-block:: console

    $ pip install taurus_pyqtgraph[Archiving] # Installing Archiving Pyhdb++ support

This is the preferred method to install taurus_pyqtgraph, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

Installation from Conda repositories
------------------------------------

Alternatively you can install taurus_pyqtgraph using Conda:

.. code-block:: console

    $ conda install -c conda-forge -c taurus-org taurus_pyqtgraph


Installation from GitLab sources
--------------------------------

If you prefer to install the taurus_pyqtgraph package from sources directly you will have all new features added to
the development branch, but be careful, because API may change or a feature may be removed.

To install the taurus_pyqtgraph from sources you can use the following commands:

.. code-block:: console

    $ git clone https://gitlab.com/taurus-controls/taurus_pyqtgraph.git
    $ git checkout origin develop # Or any desired branch (stable, develop, ...)
    $ cd taurus_pyqtgraph
    $ # Now you have to choose if you want to edit code and make you own tests or install it as it is.
    $ # (Choose one of the following)
    $ pip install . # This command will install taurus_pyqtgraph
    $ pip install -e. # This command will install taurus_pyqtgraph in editable mode
    $ # Or with archiving support
    $ pip install .[Archiving] # This command will install taurus_pyqtgraph and pyhdbpp
    $ pip install -e.[Archiving] # This command will install taurus_pyqtgraph and pyhdbpp in editable mode


.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/



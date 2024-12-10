import os
import sys

sys.path.insert(0, os.path.abspath("../../"))


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Taurus Pyqtgraph'
copyright = '2024, ALBA - CELLS'
author = 'ALBA - CELLS'
release = '0.9.6'
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_mdinclude"
]


templates_path = ['_templates']
exclude_patterns = []

pygments_style = "sphinx"
autodoc_default_options = {"members": True, "private-members": True}

autoclass_content = 'both'
html_logo = 'imgs/logo.png'
html_favicon = 'imgs/logo.ico'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    "sticky_navigation": True,
    "collapse_navigation": False
}

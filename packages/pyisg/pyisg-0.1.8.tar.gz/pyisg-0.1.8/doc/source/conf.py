# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------

project = "pyisg"
copyright = "2024, Kentaro Tatsumi"
author = "Kentaro Tatsumi"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # "myst_parser",
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

autosectionlabel_prefix_document = True

myst_enable_extensions = [
    "deflist",
    "attrs_inline",
    "dollarmath",
]

myst_heading_anchors = 2

source_suffix = {
    ".rst": "restructuredtext",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

autodoc_member_order = "bysource"
# autodoc_typehints = 'both'

nb_execution_mode = "off"

html_title = "pyisg"

html_theme_options = {
    "use_repository_button": True,
    "repository_url": "https://github.com/paqira/pyisg",
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/paqira/pyisg",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pyisg/",
            "icon": "https://img.shields.io/pypi/v/pyisg?logo=PyPI&label=PyPI",
            "type": "url",
        },
    ],
}

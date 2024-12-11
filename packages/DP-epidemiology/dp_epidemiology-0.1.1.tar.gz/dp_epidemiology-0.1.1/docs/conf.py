# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DP_epidemiology'
copyright = '2024, Shubham Kumar, Milan Anand Raj, Divya Gupta'
author = 'Shubham Kumar, Milan Anand Raj, Divya Gupta'
release = '0.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [ 
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    ]

intersphinx_disabled_domains = ["std"]

templates_path = ['_templates']

# -- Options for EPUB output
epub_show_urls = "footnote"


exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'

html_theme = "sphinx_rtd_theme"

html_static_path = ['_static']

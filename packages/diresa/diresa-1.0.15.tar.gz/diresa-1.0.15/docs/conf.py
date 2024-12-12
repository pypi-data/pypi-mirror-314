# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/diresa'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DIRESA'
copyright = '2024, Geert De Paepe, ETRO VUB'
author = 'Geert De Paepe'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx_rtd_theme', 'sphinx_copybutton']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
html_theme = "sphinx_rtd_theme"
html_theme_options = {"logo_only": True}
html_logo = "images/diresa.png"
html_show_sourcelink = True
gitlab_url = "https://gitlab.com/etrovub/ai4wcm/public/diresa"
autodoc_default_options = {
    'member-order': 'bysource',
    'undoc-members': False,
    'special-members': '__init__',
}
autodoc_mock_imports = ["tensorflow", "tensorflow_probability", "keras", "diresa"]


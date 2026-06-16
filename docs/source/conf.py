# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# Ashida Added 1
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

project = 'alt_generate_zh_name'
copyright = '2026, Ashida.Shi'
author = 'Ashida.Shi'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Ashida Changed 2
# extensions = []
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',  # 可以在文档中直接查看源码链接
    'sphinx.ext.napoleon',  # 支持更美观的 docstring 风格
]

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Ashida Changed 3
# html_theme = 'alabaster'
html_theme = 'furo'
html_static_path = ['_static']

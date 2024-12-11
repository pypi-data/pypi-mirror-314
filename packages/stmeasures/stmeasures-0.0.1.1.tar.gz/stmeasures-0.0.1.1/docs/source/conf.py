import pathlib
import sys

project_root = pathlib.Path(__file__).parents[2].resolve()
libdir = project_root / "stmeasures"

sys.path.insert(0, str(libdir))

project = 'stmeasures'
copyright = '2024, TT2024-B106'
author = 'TT2024-B106'

# TODO: versioningit?
release = '0.0.1'
version = '0.0.1'

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

html_theme = 'sphinx_rtd_theme'

epub_show_urls = 'footnote'

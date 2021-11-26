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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'BDF-Manual'
copyright = '2021, WangC'
author = 'WangC'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_panels",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    'sphinxcontrib.bibtex',
    'sphinx.ext.mathjax'
]

bibtex_bibfiles = ['refs.bib']

mathjax3_config = {
    "tex": {"extensions": ["mhchem.js"]}
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'zh'

numfig = True

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

latex_engine = 'xelatex'

latex_elements = {
    'preamble': r'''
\usepackage[version=4]{mhchem}
\hypersetup{unicode=true}
\usepackage{ctex}
\addto\captionsenglish{\renewcommand{\chaptername}{}}
'''
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "LZ0211", # Username
    "github_repo": "BDF-Manual", # Repo name
    "github_version": "master", # Version
    #"conf_py_path": "/source/", # Path in the checkout to the docs root
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


from pygments.lexer import RegexLexer,words,include,bygroups
from pygments.token import *
import re

class BDFLexer(RegexLexer):
   
    name = 'BDF'
    aliases = ['bdf']
    filenames = ['*.inp']
    mimetypes = ['text/x-bdf']

    flags = re.IGNORECASE

    tokens = {
        'root': [
            include('comment'),
            (r'\b(geometry)([\s\S]+)(end geometry)\b',bygroups(Keyword.Namespace, Text, Keyword.Namespace)),
            (r'\b(basis-multi)([\s\S]+)(end basis)\b',bygroups(Keyword.Namespace, Text, Keyword.Namespace)),
            include('modules'),
            include('keywords'),
            include('bool'),
            include('numbers'),
            ('.+', Text),
        ],
        'modules': [
            (words((
                '$compass', '$bdfopt', '$drt', '$elecoup', '$expandmo', '$grad', '$localmo',
                '$mcscf', '$mp2', '$mrci', '$resp', '$scf', '$tddft', '$traint',
                '$xianci', '$xuanyuan','$end'), suffix=r'\b'),
             Name.Function),
        ],
        "keywords": [
            (words((
                'basis', 'charge', 'spin', 'title', 'RI-J','RI-K','RI-C','Group','Unit','Thresh','maxmem','RS','Heff','Hsoc','NuclearInuc','Cholesky','Occupy','Alpha','Beta','DFT','NPTRAD','NPTANG','COSXNGRID','Grid','Gridtype','Partitiontype','Numinttype','Guess'), suffix=r'\b'),
             Name.Attribute),
        ],
        "bool": [
            (words((
                'Nosymm', 'norotate', 'skeleton', 'extcharge', 'uncontract', 'primitive', 'direct', 'scalar','direct','soint','RHF','UHF','ROHF','RKS','UKS','ROKS','D3','NosymGrid'), suffix=r'\b'),
            Name.Builtin),
        ],
        'numbers': [
            (r'\d+\.\d+', Number.Float),
            (r'\d+[ed][+-]?[0-9]+', Number.Float),
            (r'\d+', Number.Integer),
        ],
        'comment': [
            (r'#.*', Comment.Single),
            (r'^\*.*', Comment.Single),
            (r'\n(\*.*)', bygroups(Comment.Single)),
            (r'\n(%.*)', bygroups(Comment.Preproc)),
        ]
    }

def setup(sphinx):
    sphinx.add_lexer("bdf", BDFLexer)

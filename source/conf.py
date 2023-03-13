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
author = '索兵兵, 王聪 等'


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

bibtex_default_style = 'mystyle'

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
\usepackage{cite}
\usepackage{longtable}
\documentclass[openany]{book}
\usepackage[version=4]{mhchem}
\hypersetup{unicode=true}
\usepackage{ctex}
\parindent 2em
\definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
\renewcommand\familydefault{\ttdefault}
\renewcommand\CJKfamilydefault{\CJKrmdefault}
\addto\captionsenglish{\renewcommand{\chaptername}{}}
'''
}

pdf_documents = [
    ('index', u'Introduction', u'Installation', u'Input and Output', u'User Guide', u'Easyinput Guide', u'Input Library', u'Example', u'Application', u'FQA', u'Cite'),
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_logo = './images/BDF_logo.png'

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

# pygments_style = 'colorful'


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
            (r'\b(geometry)([^\$]*)?(end geometry)\b',bygroups(Keyword.Namespace, Text, Keyword.Namespace)),
            (r'\b(basis-multi)([\s\S]*)?(end basis)\b',bygroups(Keyword.Namespace, Text, Keyword.Namespace)),
            (r'\b(basis-block)([\s\S]*)?(end basis)\b',bygroups(Keyword.Namespace, Text, Keyword.Namespace)),
            (r'\b(geometry2)([^\$]*)?(end geometry2)\b',bygroups(Keyword.Namespace, Text, Keyword.Namespace)),
            (r'\b(title)(\s*\n[^\n]*\n)',bygroups(Name.Builtin,Name.Constant)),
            include('modules'),
            include('keywords'),
            include('values'),
            (r'C\([123456is]\)|C\([23456][vh]\)|D\([23456]h?\)|S\([468]\)|S\(10\)|T\(d\)|O\(h\)|I\(h\)',Name.Constant),
            (r'STO-\dG|3-21\+*G|6-311?\+*G\S*|(aug-)?cc-p[VCw]\S+|(ma-)?Def2-[SDTQ]Z?V\(?P\S*|Sapporo-\S*|Stuttgart-\S*|Dirac-Dyall\S*|(Modified-)?LANL\d+\S*|\d+(m|g)w',Name.Constant),
            include('bool'),
            include('numbers'),
            (r'\S+', Text),
            (r'\s+', Text),
        ],
        'modules': [
            (words((
                '$compass', '$bdfopt', '$drt', '$elecoup', '$expandmo', '$grad', '$localmo',
                '$mcscf', '$mp2', '$mrci', '$resp', '$scf', '$tddft', '$traint',
                '$xianci', '$xuanyuan','$nmr','$end'), suffix=r'\b'),
             Name.Function),
        ],
        "keywords": [
            (words((
                'basis', 'charge', 'spin', 'title', 'RI-J','RI-K','RI-C', 'Geometry', 'Group', 'Unit', 'Thresh', 'RS','Heff','Hsoc','Nuclear','Reled','Relefg', 'Cholesky','Occupy','Alpha','Beta','DFT','NPTRAD','NPTANG','COSXNGRID','Grid','Gridtype','Partitiontype','Numinttype','ThreshRho','ThreshBSS','Coulpot','Coulpotmax','Coulpottol','Maxitter','Vshift','Damp','ThrEne','ThrDen', 'ThreshConverg', 'MaxDiis','Iaufbau','Smeartemp','Blkiop','Iviop','Print','IprtMo','Tollin','IfPair','hpalpha','hpbeta','Pinalpha','Pinbeta','Imethod','Isf','Itda','Ialda','Itest','icorrect','iact','elw','eup','Idiag','Iguess','Crit_e','Cirt_vec','Iroot','Nroot','Istore','Nprt','Cdthrd','Nfiles','Isoc','Ifgs','Imatsoc','Imatrsf','Imatrso','Ntoanalyze','Memjkop','Imemshrink','Solver','Imulti','Noncoupl','Multistate','Maxcycle','TolGrad','TolEne', 'TolStep','IOpt','Update','ICoord','ILine','Constrain','Hess','ReCalcHess','NumHessStep','Nrootgrad','Maxiter','IntCre','Ishell','Cutcpm','Printgrad','Iprt', 'NOrder','Dimer-Block','End','Delta','NEB-Block','NImage','NEBk','NEBMode','NFrame','Geometry2','NDeg','NTemp','Temp','NPress','Press','Scale', 'NFiles','Imethod','Method','Nrootgrad','Cthrd','Ignore','IRepIRoot','JahnTeller','Pola','States','Pairs','Step','Iprt','Nexcit','Electrans','Dft','Mboys','Hybridboys','Hybridthre','Thresh','Tailcut','Threshpop','Maxcycle','Orbital','Frozocc','Frozvir','Iapair','Nolmocls','Nolmoact','Nolmovir','AVAS','Scri','Iprtmo','Frozen','Symmetry','Nelectron','Core','Delete','Close','Active','Actel','Roots','Guess','Mixorb','Maxmem',"Rsomega",
                'Spinmulti','icg','igiao','igatom','cgcoord','cgunit'), suffix=r'\b'),
             Name.Builtin),
        ],
        "bool": [
            (words((
                'Nosymm', 'norotate', 'skeleton', 'saorb', 'check', 'restart', 'extcharge', 'uncontract', 'primitive', 'direct', 'scalar','direct','soint','NuclearInuc', 'RHF','UHF','ROHF','RKS','UKS','ROKS','D3','NosymGrid','DirectGrid','NoDirectGrid','NoGridSwitch','COSX','MPEC+COSX','NoDiis','Noscforb','Pyscforb','Molden','Checklin','Aokxc','Lefteig','Geom','Line','Quad','Fnac','Single','Double','Noresp','Fdif','Reduced','GSApr','Boys','Pipek','Mulliken','Lowdin','Jacobi','Trust','Rohfloc','Mcscffloc','Orbread','Flmo','Anaylze','Momatch','Directgrid','Overlap','UTDDFT','TDDFT','FCIDUMP','Nature','Dryrun','PHO','Readhess','Dimer','NoInterpolation','Crude','NEB',), suffix=r'\b'),
            Name.Attribute),
        ],
        "values": [
            (words((
                'Angstrom','Ang','Bohr','Coarse','Medium','Strict','read', 'b3lyp', 'b3pw91', 'bp86', 'LSDA', 'SVWN5', 'SAOP', 'BLYP', 'PBE', 'PW91', 'OLYP', 'KT2', 'TPSS', 'M06L', 'GB3LYP', 'BHHLYP', 'PBE0', 'HFLYP', 'VBLYP', 'wB97', 'wB97X', 'CAM-B3LYP', 'LC-BLYP', 'TPSSh', 'M062X', 'B2PLYP', 'only', 'init', 'final', 'init+final', 'S-CD', '1c-CD',  'ADZP-ANO', 'ANO-DK3', 'ANO-R', 'ANO-R0', 'ANO-R1', 'ANO-R2', 'ANO-R3', 'ANO-RCC', 'ANO-RCC-VDZ', 'ANO-RCC-VDZP', 'ANO-RCC-VTZP', 'ANO-RCC-VQZP', 'ANO-RCC-VTZ', 'jorge-DZP', 'jorge-TZP', 'jorge-QZP', 'jorge-DZP-DKH', 'jorge-TZP-DKH', 'jorge-QZP-DKH', 'SARC-DKH2', 'SARC2-QZV-DKH2', 'SARC2-QZVP-DKH2', 'x2c-SVPall', 'x2c-TZVPall', 'x2c-TZVPPall', 'x2c-QZVPall', 'x2c-QZVPPall', 'x2c-SVPall-2c', 'x2c-TZVPall-2c', 'x2c-TZVPPall-2c', 'x2c-QZVPall-2c', 'x2c-QZVPPall-2c', 'UGBS', 'Dirac-RPF-4Z', 'Dirac-aug-RPF-4Z', 'SVP-BSEX', 'DZP', 'DZVP', 'TZVPP', 'IGLO-II', 'IGLO-III', 'Sadlej-pVTZ', 'Wachters+f', 'Pitzer-AVDZ-PP', 'Pitzer-VDZ-PP', 'Pitzer-VTZ-PP', 'CRENBL', 'CRENBS', 'DHF-SVP', 'DHF-TZVP', 'DHF-TZVPP', 'DHF-QZVP', 'DHF-QZVPP', 'SBKJC-VDZ', 'SBKJC-POLAR', 'pSBKJC', 'Aoper', 'Boper', 'Bfreq','None','1Soc','2Soc','3Soc','4Soc','5Soc','6Soc','7Soc','8Soc','9Soc','MECP','CI'), suffix=r'\b'),
            Name.Constant),
        ],
        'numbers': [
            (r'[+-]?\d+\.\d+', Number.Float),
            (r'[+-]?\d+(\.)?[ed][+-]?[0-9]+', Number.Float),
            (r'\d+', Number.Integer),
        ],
        'comment': [
            (r'\/\*.*?\*\/', Comment.Single),
            (r'#.*', Comment.Single),
            (r'^\*.*', Comment.Single),
            (r'\n(\*.*)', bygroups(Comment.Single)),
            (r'%.*', Comment.Preproc),
        ]
    }


def setup(sphinx):
    sphinx.add_lexer("bdf", BDFLexer)

import pybtex.plugin
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.template import field

class MyStyle(UnsrtStyle):
    def format_title(self, e, which_field):
        return field(which_field)

pybtex.plugin.register_plugin('pybtex.style.formatting', 'mystyle', MyStyle)

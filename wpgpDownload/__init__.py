# -*- coding: utf-8 -*-

"""Top-level package for wplib."""

__author__ = """Nikolaos Ves"""
__email__ = 'vesnikos@gmail.com'
__version__ = '0.1.1'

from .utils.misc import ROOT_DIR, CSV_SIGNATURE, DATA_DIR

from .utils.isos import Countries
from .utils.dl import wpFtp
from .utils.wpcsv import Product
from .utils.convenience_functions import  download_country_covariates, download_CSVFileAllCovariates


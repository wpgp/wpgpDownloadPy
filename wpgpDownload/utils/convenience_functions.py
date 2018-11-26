# a set of convenience functions
from __future__ import print_function
import gzip
import shutil
import sys

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory


from wpgpDownload.utils.misc import ROOT_DIR
from configparser import ConfigParser




from wpgpDownload.utils.dl import wpFtp
from wpgpDownload.utils.misc import CSV_SIGNATURE, DATA_DIR

config = ConfigParser()
config.read(Path(ROOT_DIR / 'configuration.ini').as_posix())
manifest_file = config['ftp']['manifest']

_ftp = wpFtp()
if _ftp.csv_signature != CSV_SIGNATURE:
    print('The current manifest file is either missing or outdated. It is advised to fetch the most recent '
          'from the FTP.\n You can do this by running: \n'
          '>>> from wplib.utils.convenience_functions import refresh_csv\n'
          '>>> refresh_csv()')


def refresh_csv():
    with TemporaryDirectory() as t_dir:
        output_dir = Path(t_dir)
        csv_file = _ftp.download(manifest_file, output_dir)
        csv_file = Path(csv_file)

        # compress and replace the local manifest file in the data folder
        with csv_file.open(mode='rb') as f_in:
            f_out = DATA_DIR / 'wpgpDatasets.csv.gz'
            with gzip.open(f_out, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


# TODO: make test case for this
def download_country_covariates(ISO, out_folder, prod_name):
    """
    :param filter: A list of CvtName to the download.
    :type filter: List
    """

    from wpgpDownload.utils.isos import Countries
    from wpgpDownload.utils.wpcsv import Product

    if prod_name is None:
        raise ValueError('prod_name cannot be None.')

    # list-ize the filter param if a string
    if isinstance(prod_name, str):
        prod_name = [prod_name, ]

    country = Countries.get(ISO)

    products = Product(country.alpha3)
    download_list = []
    for idx, p in products:
        if p.dataset_name in prod_name:
            prod_name.pop(prod_name.index(p.dataset_name))
            download_list.append(p)

    # empty download list
    if not len(download_list):
        raise ValueError('None of the product(s) you have requested exist in the manifest')

    # products that were not found
    if len(prod_name) > 0:
        for p in prod_name:
            print('%s was not found in the manifest file' % p, file=sys.stderr)

    p_out = Path(out_folder)
    if not p_out.exists():
        p_out.mkdir(parents=True)

    for e in download_list:
        _ftp.download(e.path, out_folder)


def download_CSVFileAllCovariates(dest_folder):
    dst = Path(dest_folder)
    if not dst.exists():
        dst.mkdir(parents=True)
    _ftp.download(manifest_file, dst)

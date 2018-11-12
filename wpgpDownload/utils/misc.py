import gzip
from hashlib import md5
from typing import Union

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


def library_root_path()->Path:
    path = Path(Path(__file__).parent / '..')
    return path


def data_folder()->Path:
    return library_root_path() / 'data'


def csv_file()->Path:
    return data_folder() / 'wpgAllCovariates.csv.gz'


def md5_digest(file: Union[Path, str], gz=False)->str:
    """
     Returns the MD5 signature of the file.
    :param file: path to the file to generate the md5 signature.
    :param gz: If the file is compressed by the gz library.
    :return: MD5 hash string

    """
    file = Path(file)
    # if the file doesn't exist, return 0
    if not file.is_file():
        return '0'

    m = md5()
    if file.suffixes[-1].lower() == '.gz':
        gz = True

    # open/read the file with gzip module.
    if gz:
        m.update(gzip.open(file.as_posix()).read())
    else:
        m.update(file.open(mode='rb').read()).hex()

    return m.digest().hex()


CSV_SIGNATURE = md5_digest(csv_file())
ROOT_DIR = library_root_path()
DATA_DIR = data_folder()

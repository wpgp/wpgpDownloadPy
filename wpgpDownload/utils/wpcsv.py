from collections import namedtuple
import warnings
import platform
import sys
import gzip
import csv

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

BASE_ROOT = Path(__file__).parent
CSV_FILE = BASE_ROOT / '..' / 'data' / 'wpgpDatasets.csv.gz'
_Product = namedtuple('Product', 'idx numeric alpha3 country_name dataset_name description path')
_records = []

if platform.system() == 'Windows':
    if sys.version_info.major == 3 and sys.version_info.minor >= 6:
        encoding = 'oem'
    else:
        encoding = 'utf-8'
else:
    encoding = 'utf-8'

if sys.version_info >= (3,):
    with gzip.open(CSV_FILE, 'rt', encoding=encoding, errors='replace') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, 1):
            # add each row to the records list
            _records.append(
                # idx numeric alpha3 country_name dataset_name description path
                _Product(int(row['ID']), row['ISO'], row['ISO3'], row['Country'], row['Covariate'], row['Description'],
                         Path(row['PathToRaster']))
            )
else:
    CSV_FILE = CSV_FILE.as_posix()
    with gzip.open(CSV_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, 1):
            # add each row to the records list
            _records.append(
                # idx numeric alpha3 country_name dataset_name description path
                _Product(int(row['ID']), row['ISO'], row['ISO3'], row['Country'], row['Covariate'], row['Description'],
                         Path(row['PathToRaster']))
            )

ISO_LIST = sorted(set(r.alpha3 for r in _records))


def _build_index(iso):
    # ISO should not be none
    if iso is None:
        raise TypeError('ISO should not be None')
    # ISO should exist
    if iso not in ISO_LIST:
        raise ValueError('This ISO does not exist in the ISO list.')
    res = dict((r.idx, r) for r in _records if r.alpha3 == iso)
    if len(res) == 0:
        raise ValueError('No products were found with that ISO.')

    return res


NOT_FOUND = object()


class _Products(object):

    def __init__(self, iso):
        self.products = _build_index(iso)

    def get(self, idx, default=NOT_FOUND):
        res = self.products.get(idx, default)
        if res == NOT_FOUND:
            raise KeyError
        return res

    def __getitem__(self, item):
        return self.get(item)

    def iter_download_urls(self):
        for p in self.products.values():
            yield p.path

    def __iter__(self):
        for k, v in self.products.items():
            yield v

    # def __len__(self):
    #     return len(list(self.products))

    def description_contains(self, filter):
        result = []
        for k, v in self.products.items():
            if filter.lower() in v.description.lower():
                result.append(v)
        return result

Product = _Products

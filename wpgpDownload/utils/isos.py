import csv
import platform
import sys
from numbers import Integral
from collections import namedtuple

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


if platform.system() == 'Windows':
    if sys.version_info.major == 3 and sys.version_info.minor >= 6:
        encoding = 'oem'
    else:
        encoding = 'utf-8'
else:
    encoding = 'utf-8'

# taken from iso3166 package
BASE_ROOT = Path(__file__).parent
csv_file = BASE_ROOT / '..' / 'data' / 'WPGP_ISO_Country_codes.csv'
_records = []
Country = namedtuple('Country', 'numeric alpha3 name')

# populate from csv file
file_handler = open(csv_file.as_posix(), 'r', encoding=encoding, errors='replace')
for row in map(Country._make, csv.reader(file_handler)):
    _records.append(row)

NOT_FOUND = object()


def _build_index(idx):
    return dict((r[idx].upper(), r) for r in _records)


_by_name = _build_index(2)
_by_alpha3 = _build_index(1)
_by_numeric = _build_index(0)


class _CountryLookup(object):

    @staticmethod
    def get(key, default=NOT_FOUND):
        if isinstance(key, Integral):
            r = _by_numeric.get(str(key), default)
        elif isinstance(key, str):
            k = key.upper()
            if len(k) > 3:
                r = _by_name.get(k, default)
            else:  # key <= 3
                if k.isdigit():
                    r = _by_numeric.get(k, default)
                else:
                    r = _by_alpha3.get(k, default)
        else:
            r = default
        if r == NOT_FOUND:
            raise KeyError(key)
        return r

    def __len__(self):
        return len(_records)

    def __iter__(self):
        return iter(_records)

    def __contains__(self, item):
        try:
            self.get(item)
            return True
        except KeyError:
            return False


Countries = _CountryLookup()

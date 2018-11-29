#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

NUMBER_OF_VALID_COUNTRIES = 249


@pytest.fixture(scope='module')
def csv_file():
    from wpgpDownload.utils.misc import csv_file
    return csv_file()


@pytest.fixture(scope='module')
def csv_signature():
    from wpgpDownload.utils import misc
    return misc.CSV_SIGNATURE


# noinspection SpellCheckingInspection
def test_wplib_builin_md5_signature(csv_file):
    from wpgpDownload.utils.misc import md5_digest
    md5 = md5_digest(csv_file)
    assert md5 == 'e169744a9e84120230f916a73fd8a658'


# noinspection SpellCheckingInspection
def test_wplib_dl_ftp_md5_signature():
    from wpgpDownload.utils.dl import wpFtp
    ftp = wpFtp()

    assert ftp.csv_signature == 'e169744a9e84120230f916a73fd8a658'


# noinspection SpellCheckingInspection
def test_wplib_compare_signatures(csv_signature):
    from wpgpDownload.utils.dl import wpFtp
    ftp = wpFtp()

    assert csv_signature == ftp.csv_signature


# noinspection SpellCheckingInspection
def test_wplib_isos():
    from wpgpDownload.utils import Countries

    c = Countries
    assert len(c) == NUMBER_OF_VALID_COUNTRIES
    assert c.get(531).__repr__() == "Country(numeric='531', alpha3='CUW', name='Curacao')"
    assert c.get('GRC').__repr__() == "Country(numeric='300', alpha3='GRC', name='Greece')"
    assert c.get('United States').__repr__() == "Country(numeric='840', alpha3='USA', name='United States')"


# noinspection SpellCheckingInspection
def test_wplib_dl(tmpdir):
    from wpgpDownload.utils import wpFtp
    ftp = wpFtp()
    res = ftp.download('GIS/Population/Global_2000_2020/2000/SLV/slv_ppp_2000.tif', tmpdir)
    assert res == tmpdir / 'slv_ppp_2000.tif'


def test_wplib_has_internet():
    from wpgpDownload.utils import has_internet

    assert has_internet() is True


def test_wplib_dl_err_non_existant_file(tmpdir):
    from wpgpDownload.utils import wpFtp
    from ftplib import error_perm

    ftp = wpFtp()
    with pytest.raises(error_perm, match='FTP complained for file:*'):
        res = ftp.download('NON_EXISTANT_FILE', tmpdir)


# noinspection SpellCheckingInspection
def test_wplib_dl_fail_bad_hostname():
    from wpgpDownload.utils import wpFtp
    server = "ftp.worldpop.org2.uk"

    with pytest.raises(ValueError,
                       match=r'Could not reach FTP server. Please check if FTP server address is correct'):
        ftp = wpFtp(server)


def test_wplib_conv_function_warn_on_not_avail_prod(capsys, tmpdir):
    from wpgpDownload.utils.convenience_functions import download_country_covariates as dl

    dl('GRC', tmpdir, ['ppp_2002', 'ppp_1999', 'ppp_1998'])
    captured = capsys.readouterr()
    assert 'ppp_1999' in captured.err
    assert 'ppp_1998' in captured.err
    assert 'ppp_2002' not in captured.err


def test_wplib_conv_function_err_on_not_avail_prod():
    from wpgpDownload.utils.convenience_functions import download_country_covariates as dl
    with pytest.raises(ValueError):
        dl(ISO='GRC', out_folder='.', prod_name='zzzzz')


def test_wplib_conv_function_err_on_empty_prod_request():
    from wpgpDownload.utils.convenience_functions import download_country_covariates as dl
    with pytest.raises(ValueError):
        dl(ISO='GRC', out_folder='.', prod_name='')
    with pytest.raises(ValueError):
        dl(ISO='GRC', out_folder='.', prod_name=None)
    with pytest.raises(TypeError):
        dl(ISO='GRC', out_folder='.')


def test_wplib_util_wpcsv_products_contain():
    from wpgpDownload.utils.wpcsv import Product
    product = Product('GRC')
    results = sorted(product.description_contains('people per grid-cell'))

    assert len(results) == 21
    for year, r in enumerate(results, 2000):
        assert r.country_name == 'Greece'
        assert r.dataset_name == 'ppp_%s' % year
        assert r.path == Path('GIS/Population/Global_2000_2020/%s/GRC/grc_ppp_%s.tif' % (year, year))

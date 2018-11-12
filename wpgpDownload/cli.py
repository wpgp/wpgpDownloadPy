# -*- coding: utf-8 -*-

"""Console script for wpgpDownload."""
import shutil
import sys
import os
import click
import gzip

from tempfile import TemporaryDirectory
from configparser import ConfigParser

try:
    from pathlib import Path
except ImportError:
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from pathlib2 import Path

from wpgpDownload import wpFtp
from wpgpDownload import CSV_SIGNATURE, DATA_DIR, ROOT_DIR


# noinspection SpellCheckingInspection
@click.group()
@click.pass_context
def wpgp_download(ctx):
    """Console script for wpgpDownload."""
    ctx.ensure_object(dict)

    config = ConfigParser()
    config.read(ROOT_DIR / 'configuration.ini')
    ftp = wpFtp()
    #
    ctx.obj['ftp'] = ftp
    ctx.obj['manifest_file'] = manifest_file = config['ftp']['manifest']

    if ftp.csv_signature != CSV_SIGNATURE:
        txt = 'There is an updated manifest file.\n' \
              'It is recommended to update the existing for access the most current WorldPop datasets'
        try:
            if click.confirm(txt, default=True):
                with TemporaryDirectory() as t_dir:
                    output_dir = Path(t_dir)
                    csv_file = ftp.download(manifest_file, output_dir)
                    csv_file = Path(csv_file)

                    # compress and replace the local manifest file in the data folder
                    with csv_file.open(mode='rb') as f_in:
                        f_out = DATA_DIR / 'wpgAllCovariates.csv.gz'
                        with gzip.open(f_out, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)

        # the user has chosen to ABORT the operation
        except click.Abort as e:
            return 1

    return 0


# noinspection PyShadowingBuiltins
@wpgp_download.command()
@click.option('-f', '--format', type=click.Choice(['screen', 'json']), default='screen')
@click.pass_context
def isos(ctx, format):
    from wpgpDownload import Countries
    if format == 'screen':
        c = Countries
        for e in c:
            click.echo('{numeric},{alpha3},{name}'.format(numeric=e.numeric, alpha3=e.alpha3, name=e.name))
    if format == 'json':
        import json
        json_string = json.dumps(Countries.by_iso3)
        click.echo(json_string)

    sys.exit(0)


# noinspection PyShadowingBuiltins
@wpgp_download.command()
@click.option('-i', '--iso', type=click.STRING, required=True)
@click.option('--datasets', is_flag=True, is_eager=True,
              help='Print the ISO\'s datasets along with their IDs and exit.')
@click.option('--id', multiple=True, type=int)
@click.option('--method', type=click.Choice(['native', 'wget', 'curl', 'none']), default='native')
@click.option('-o', '--output_folder', type=click.Path(exists=True), help='Folder where any downloads will be stored')
@click.option('-f', '--filter', type=str,
              help='String-Text to filter the results. This string is checked against the description of a product')
@click.pass_context
def download(ctx, iso, method, output_folder, datasets, id, filter):
    from wpgpDownload import Countries
    from wpgpDownload.utils.wpcsv import Product
    try:
        c = Countries.get(iso)

    except KeyError:
        click.echo('%s is not a valid ISO code')
        sys.exit(1)

    products = Product(c.alpha3)
    if filter:
        products = products.filter(filter)

    if datasets:
        for p in products:
            idx, record = p
            if len(id) > 0 and idx not in id:
                continue
            click.echo('{}\t{}\t{}'.format(idx, record.description, record.path))
        sys.exit(0)

    ftp = ctx.obj['ftp']
    out_folder = output_folder or Path(os.getcwd())

    for p in products:
        idx, record = p
        if len(id) > 0 and idx not in id:
            continue

        if method == 'none':
            for p in products.iter_download_urls():
                click.echo(p)
            sys.exit(0)

        elif method == 'wget':
            raise NotImplemented('yet')
            # wget = which('wget') or 'wget'
            #
            # for p in products.iter_download_urls():
            #     url = p
            #     basename = Path(p).name
            #
            #     out_file_path = Path(out_folder).joinpath(basename).as_posix()
            #     click.echo(f"{wget} --ftp-user='{username}' --ftp-password='{password}' -O {out_file_path} "
            #                f"{root_url}/{url}")
            return 0

        elif method == 'curl':
            raise NotImplemented('yet')
            return 0

        elif method == 'native':
            remote_file = record.path
            ftp.download(remote_file, out_folder, progress_bar=True)
    return 0


if __name__ == "__main__":
    sys.exit(wpgp_download())  # pragma: no cover

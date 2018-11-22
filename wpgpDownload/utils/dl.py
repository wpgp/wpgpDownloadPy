import ftplib
import logging
import os
from configparser import ConfigParser
from datetime import datetime
from socket import gaierror
from io import BytesIO
import click

from ftplib import error_perm

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from wpgpDownload.utils.misc import ROOT_DIR

_config = ConfigParser()
_config.read(Path(ROOT_DIR / 'configuration.ini').as_posix())


class wpFtp(object):
    """
    Convenience Class for ftp operations.
    ftp = wpFtp(server,username,password)
    """
    timeout = 10  # ftp timeout, in seconds
    logger = logging.getLogger('library::wpFtp')
    logger.setLevel(logging.INFO)

    def __init__(self, server=_config['ftp']['server'], username='anonymous', password=''):
        self.server = server
        self.username = username
        self.password = password
        try:
            self.ftp = ftplib.FTP(self.server, username, password, timeout=self.timeout)
        except gaierror:
            raise ValueError('Could not reach FTP server. Please check if FTP server address is correct.')
        except ftplib.error_perm:
            raise ValueError('FTP server denied us. Please check username/password')

        self.ftp.sendcmd("TYPE i")  # switch to binary mode

    def __repr__(self):
        return type(self).__name__ + ' <' + self.username + '@' + self.server + '>'

    def __del__(self):
        if hasattr(self, 'ftp'):
            self.ftp.close()

    @property
    def csv_signature(self):
        bio = BytesIO()
        p = Path(_config['ftp']['sig'])
        self.ftp.retrbinary('RETR ' + p.as_posix(), bio.write)
        bio.seek(0)
        result = bio.read().decode('utf-8')
        result = result.strip()
        result = result.split(' ')[0]
        return result

    def get_timestamp(self, ftp_absolute_path):
        """ Get Time stamp of file in the ftp. Returns None if fails """

        p = Path(ftp_absolute_path)
        response_code, time = self.ftp.sendcmd('MDTM %s' % p.as_posix()).split()

        if response_code != '213':
            raise Exception("Not ok return code (%s), when tried to retrieve timestamp" % response_code)

        return datetime.strptime(time, '%Y%m%d%H%M%S')

    def get_filesize(self, ftp_absolute_path):
        """ Returns the file size from the ftp.
            Return None if the file is not in the ftp. """

        p = Path(ftp_absolute_path)
        try:
            filesize = self.ftp.size(p.as_posix())
        except error_perm as e:
            print('Could not get file size: %s' % p.as_posix())
            raise error_perm
        # if response_code != '213':
        #     raise wpException("Not ok return code (%s), when tried to retrieve filesize" % response_code)
        if filesize >= 0:
            return filesize

        return None

    def download(self, from_ftp_absolute_path, to_local_absolute_path,
                 progress_bar=False, callback=None):
        """ Download a file from the remote ftp, stores is locally.

        If file exists locally, it is removed beforehand.
        :param progress_bar: If true it will show a progress bar in the stdout.
        :param callback: Callback function to call with chunks of data.
        :param from_ftp_absolute_path: String or Path pointing to the file to be downloaded. Absolute Path
        :param to_local_absolute_path: String or Path to a FOLDER where to save the file from the ftp. Absolute Path
        :return Path object to downloaded file.
        :rtype Path, None
        """
        p_ftp = Path(from_ftp_absolute_path)
        p_local = Path(to_local_absolute_path).joinpath(p_ftp.name)
        file_size = self.get_filesize(p_ftp)
        if file_size is None:
            raise ValueError('%s does not exist in the FTP.' % p_ftp.name)
        if p_local.is_file():
            os.remove(p_local.as_posix())
        with click.progressbar(length=file_size, label=p_ftp.name, width=70) as bar:
            with p_local.open('wb') as fp:
                def __callback(data):
                    fp.write(data)
                    bar.update(len(data))
                    if callback:
                        callback(data)

                # retrbinary does not allow canceling.
                self.ftp.retrbinary('RETR ' + p_ftp.as_posix(), __callback)

        return p_local

import socket

from wpgpDownload.utils.dl import wpFtp
from wpgpDownload.utils.isos import Countries

from wpgpDownload.utils.convenience_functions import download_country_covariates


# https://stackoverflow.com/a/33117579/528025
def has_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        return False


wplib
=====


QuickStart
-----

#### Install

```bash
pip install git+https://github.com/wpgp/wpgpDownloadPy
```
----
#### Download (CLI)

```bash
# list available downloads for Greece (GRC) having the word distance in their description.
$ wplib download -f GRC -f distance --dataset

# download the datases with id 23456 and 23457
$ wplib download -f GRC --id 23457 --id 23456
```

#### Download (Library)
```python
from wplib.utils.convenience_functions import download_country_covariates as dl
dl(ISO='GRC',out_folder='.',filter='ccidadminl1')
dl('GRC','.',['ccilc_dst011_2002','ccilc_dst011_2002'])
``` 
----
#### Explore (CLI)

#### Explore (Library)

Installation
------------

It is recommended to create a new virtual environment using a modern python interpreter (>3.6).

If you don't know what a virtual environment is, basically an isolated replication of your python interpreter
and when used all installations or changes are happening in it shielding your default interpreter.

For more information you can read Python's ve (virtual enviroment) tutorial [here][1].

Using pip one can install this package directly from github

```bash
pip install git+https://github.com/wpgp/wplib
```

This should install the latest version in to your active python environment.


API
---

The library contains a bot high level functions and convience functions to browse and download worldpop products. It's usage is straight forward.

```python
from wplib.utils.wpcsv import Product
products = Product('GRC')  # Where instead of GRC it could be any ISO code.

#  to list all the products for GRC
for idx, p in products:
    print('%s/%s\t%s\t%s' % (idx, p.Name,p.CvtName,p.Path))

# idx           -> Position in the CSV file.
# alpha3        -> alphabetical ISO
# numeric       -> Numerical ISO code
# Name          -> English Name of the Country
# CvtName       -> Covariate Name
# Description   -> Desription of the Covariate
# Path          -> Ftp Path

# You can filter the products, focusing only in the products you are instrested:
from wplib.utils.wpcsv import Product
products = Product('IRQ')
# as before but this time only list products that contain the word 'night' in their description:
results = products.filter('night')
for idx, p in results:
    print('%s/%s\t%s\t%s' % (idx, p.Name,p.CvtName,p.Path))

```

Downloading Products
====================

Products can be fetched from the FTP location either using the CLI or the build-in downloader


Using the CLI
-------------

The command line way is the most straight forward way to locate and download Worldpop products. 


```bash
# To list all products for a specific ISO
$ wplib download -i GRC --datasets


```

If you want to download ALL the products for that ISO:
```bash
# if -o is omitted it will download by default in the working directory
$ wplip download -i GRC -o /dest/folder
```

If you want to download specific datasets
```bash
# Download ALL the datasets that
# containing the word 'distance' for Nepal (NPL)
$ wplib download -i NPL -f distance
```

You can download individual datasets as well
```bash
# list available downloads for Greece (GRC) having the word distance in their description.
$ wplib download -f GRC -f distance --dataset

# download the datases with id 23456 and 23457
$ wplib download -f GRC --id 23457 --id 23456
```

API
---

In a similar way it is possible to download worldpop datasets using the API:

```python
from wplib.utils.convenience_functions import download_country_covariates as dl
dl(ISO='GRC',out_folder='.',filter='ccidadminl1')
dl('GRC','.',['ccilc_dst011_2002','ccilc_dst011_2002'])
``` 



[1]: https://docs.python.org/3/tutorial/venv.html

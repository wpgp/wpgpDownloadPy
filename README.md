
wpgpDownload
=====

About
-----

The WorldPop Global High Resolution Population Denominators Project, funded by the Bill and Melinda Gates Foundation (OPP1134076), has produced an open-access archive of 3-arc seconds (approximately 100m at the equator) gridded population datasets, also structured by gender and age groups, for 249 countries, dependencies, and territories for 21-years (2000-2020), using the methods described by Stevens et al., 2015 (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0107042), Gaughan et al., 2016 (https://www.nature.com/articles/sdata20165), and Pezzulo et al., 2017 (https://www.nature.com/articles/sdata201789). In addition, the project has also made available the covariate datasets used as inputs to produce the gridded population datasets (Lloyd et al., under review). These datasets are available for download from the WorldPop website and FTP server using a range of methods and tools.

QuickStart
-----

#### Install

```bash
pip install git+https://github.com/wpgp/wpgpDownloadPy
```
----

#### List ISOS (CLI)

To list all the available ISOs along with their ISO numeric/letter code and their English Name

```bash
$ wpgpDownload isos
```

#### Download (CLI)

```bash
# list available downloads for Greece (GRC) having the 
# word distance in their description.
$ wpgpDownload download -i GRC -f distance --datasets


# List all the available datasets for an iso:
wpgpDownload download -i GRC --datasets

# download the datases with id 23456 and 23457
# Note the id's should exist.

$ wpgpDownload download -i GRC --id 23457 --id 23456
```

#### Download (Library)
```python
from wpgpDownload.utils.convenience_functions import download_country_covariates as dl
dl(ISO='GRC', out_folder='.', prod_name='ccidadminl1')
dl('GRC','.',['ppp_2002','ppp_2013'])
``` 
----
#### Explore (CLI)
(TODO)

#### Explore (Library)
(TODO)


Installation
------------

It is recommended to create a new virtual environment with a modern python interpreter (>3.6)
to isolate your installations from your default interpreter.

For more information on what is a virtual enviroment (ve), you can check Python's tutorial on the subject [here][1].

Using pip, one can install the package directly from github : 

```bash
pip install git+https://github.com/wpgp/wpgpDownloadPy
```

This should install the latest version into your active python environment.


API
---

The library contains both high-level and convience functions to browse and download WorldPop products.

```python
from wpgpDownload.utils.wpcsv import Product
products = Product('GRC')  # Where instead of GRC it could be any ISO code.

#  to list all the products for GRC
for idx, p in products:
    print('%s/%s\t%s\t%s' % (idx, p.Name,p.CvtName,p.Path))

# Other covariates that you can call from a Product:
# idx           -> Position in the CSV file.
# alpha3        -> alphabetical ISO
# numeric       -> Numerical ISO code
# Name          -> English Name of the Country
# CvtName       -> Covariate Name
# Description   -> Desription of the Covariate
# Path          -> Ftp Path

# You can description_contains the products, focusing only on the products in which you are interested:
from wpgpDownload.utils.wpcsv import Product
products = Product('IRQ')
# as before but this time only list products that contain the word 'night' in their description:
results = products.description_contains('night')
for idx, p in results:
    print('%s/%s\t%s\t%s' % (idx, p.Name,p.CvtName,p.Path))

```

Downloading Products
====================

Products can be fetched from the FTP location either using the CLI or the built-in downloader


Using the CLI
-------------

The command-line method is the most straightforward to locate and download WorldPop products. 


```bash
# To list all products for a specific ISO
$ wpgpDownload download -i GRC --datasets


```

To download ALL the products for that ISO:
```bash
# if -o is omitted, it will download by default into the working directory
$ wpgpDownload download -i GRC -o /dest/folder
```

To download specific datasets:
```bash
# Download ALL the datasets that
# contain the word 'distance' for Nepal (NPL)
$ wpgpDownload download -i NPL -f distance
```

To download individual datasets:
```bash
# list available downloads for Greece (GRC) having the word 'distance' in their description.
$ wpgpDownload download -f GRC -f distance --dataset

# download the datasets with id 23456 and 23457
$ wpgpDownload download -f GRC --id 23457 --id 23456
```

API
---

In a similar way, it is possible to download WorldPop datasets using the API:

```python
from wpgpDownload.utils.convenience_functions import download_country_covariates as dl
# if you want one covatiate
dl(ISO='GRC',out_folder='.',description_contains='ccidadminl1')
# of multiple
dl('GRC','.',['ppp_2002','ppp_2013'])
``` 



[1]: https://docs.python.org/3/tutorial/venv.html

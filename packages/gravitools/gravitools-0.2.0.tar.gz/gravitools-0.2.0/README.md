![gravitools](https://gitlab.opencode.de/bkg/gravitools/raw/main/data/logo/gt_name.png)

A collection of tools to analyze gravimeter data.

This Python package is a collaborative effort by the gravity metrology group at
the [German Federal Agency for Carthography and Geoesy (BKG)][BKG] and the
[hydrology section][Hydrology] at [GFZ German
Research Centre for Geosciences][GFZ].

[BKG]: https://bkg.bund.de
[Hydrology]: https://www.gfz-potsdam.de/sektion/hydrologie
[GFZ]: https://www.gfz-potsdam.de


## Features

* Read and process raw data of the [Exail Absolute Quantum Gravimeter
  (AQG)][AQG]
* Apply standardized or customized AQG data processing and outlier detection
* Read and write processed datasets with metadata to .nc-files in
  [NETCDF4-format][NETCDF4]
* Handle Earth orientation parameters (EOP) from [iers.org][IERS] for polar
  motion correction
* Evaluate tilt calibration measurements
* Visualize data with matplotlib
* CLI for standard processing of AQG raw data to .nc-file
* Dashboard for real-time processing and visualization during measurements (on AQG laptop)
* Dashboard includes a proposed standard template for a measurement protocol

[AQG]: https://www.ixblue.com/quantum-gravimeter
[NETCDF4]: https://www.unidata.ucar.edu/software/netcdf
[IERS]: https://www.iers.org

### Planned

* Handling of [Scintrex CG6][CG6] data and standard analyses
* Generation of PDF-report for tilt calibration analyses

[CG6]: https://scintrexltd.com/product/cg-6-autograv-gravity-meter/


## Dependencies

* Python 3.8 or later
* [allantools](https://github.com/aewallin/allantools) (LGPLv3+ license)
* [fpdf2](https://pypi.org/project/fpdf2/) (LGPLv3)
* [matplotlib](https://matplotlib.org/) (PSF license)
* [netcdf4-python](https://github.com/Unidata/netcdf4-python) (MIT license)
* [numpy](https://numpy.org/) (BSD license)
* [pandas](https://pandas.pydata.org/) (BSD license)
* [pyyaml](https://pyyaml.org/) (MIT license)
* [requests](https://pypi.org/project/requests/) (Apache 2 license)
* [xarray](https://xarray.pydata.org/) (Apache 2 license)

### Optional

#### AQG dashboard

* [PySide6](https://pypi.org/project/PySide6/) (LGPLv3 license)
* [pyqtgraph](https://www.pyqtgraph.org/) (MIT license)

#### Documentation

* [mkdocs](https://pypi.org/project/mkdocs/) (BSD license)
* [mkdocstrings-python](https://pypi.org/project/mkdocstrings-python/) (ISC
  license)
* [mkdocs-material](https://pypi.org/project/mkdocs-material/) (MIT license)
* [mkdocs-jupyter](https://pypi.org/project/mkdocs-jupyter/) (Apache 2 license)

#### Unit tests

* [pytest](https://pypi.org/project/pytest/) (MIT license)
* [pytest-cov](https://pypi.org/project/pytest-cov/) (MIT license)


## Installation

For the latest stable release, install from PyPI.org

```console
    $ pip install gravitools
```

For the latest (development) version, install from Git repository

```console
    $ pip install git+https://gitlab.opencode.de/bkg/gravitools.git
```

For further install instructions please see the respective section in the
documentation.


## Getting started with AQG data processing

Example usage:

```py
    from gravitools.aqg import read_aqg_raw_dataset

    # Read raw data to an AQGRawData object (which wraps a pandas.DataFrame)
    raw = read_aqg_raw_dataset("20240620_163341.zip")

    # Apply standard processing
    raw.process()

    # Finalize processing by converting to an AQGDataset (which wraps an
    # xarray.Dataset)
    dataset = raw.to_dataset()

    # Save processed dataset to file in NETCDF-4 format
    dataset.to_nc("20240620_163341.nc")

    # Generate and save a measurement report in PDF format
    dataset.save_report("report_20240620_163341.pdf")
```


## AQG dashboard

The dashboard has to be run on the AQG laptop in order to profit from its full
functionality. It has the purpose to provide an alternative, customizable way
of viewing and interacting with measurement data, during the process of live
measurements. This is especially helpful for updated, on-the-fly outlier
detection and plots of parameters as time series (e.g. temperatures, tilts).
More information on this, including all offered options, are addressed in the
documentation.

Install gravitools with the optional dependencies for the dashboard, preferably
in an isolated virtual environment.

```console
    $ pip install gravitools[dashboard]
```

Run the dashboard

```console
    $ gt-aqg-dash
```

You can now access the dashboard at `http://localhost:8000/`.


## Documentation

The documenation is available at [readthedocs.io][docu_rtd].

[docu_rtd]: https://gravitools.readthedocs.io/en/latest/

To build the documentation, clone the repository and install gravitools with
the necessary dependencies into a virtual environment.

```console
    $ git clone https://gitlab.opencode.de/bkg/gravitools.git
    $ cd gravitools/
    $ python -m venv venv
    $ source venv/bin/activate
    $ pip install -e .[docs]
```

Build the documentation

```console
    $ mkdocs build
```

The documentation can be accessed at `public/index.html`.


## Conventions

### Data

* All corrections are *subtracted* from the measured gravity value.
* Units are assumed as follows (if not provided and parameters are passed only
  as numbers). Input data in other units is converted.
    - Gravity: nm s^-2^
    - Gravity gradient: nm s^-2^ m^-1^
    - Heights: m
    - Tilt angle: rad
    - Polar angles: arcsec
    - Coordinates: degree
    - Orientation of sensor: degree from North
* Timestamps are always UTC.

### Terminology

Point
: A precisely defined measurement location, usually identified by a point code.
For example, the gravimeter lab at the Geodetic Observatory Wettzell has points
WET_CA, WET_DA, WET_EA, and WET_FA. The vertical gravity gradient is a property
of each point. An Earth tide model can apply to multiple points.

`site_name`
: The AQG control software has an input field for the measurement site name. It
is recored in the metadata (.info file) as `measurement_site_name`. Here, this
parameter name is shortened to `site_name` and its value kept unchanged. Since
this field can contain supplementary metadata, such as sensor orientation, it
is not necessarily identical to the point code. When reading a dataset,
Gravitools attempts to guess the point code and sensor orientation from the
`site_name` by a formatting pattern.

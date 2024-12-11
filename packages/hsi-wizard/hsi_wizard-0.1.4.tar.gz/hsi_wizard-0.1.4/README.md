[![Documentation Status](https://readthedocs.org/projects/hsi-wizard/badge/?version=latest)](https://hsi-wizard.readthedocs.io)
[![codecov](https://codecov.io/gh/BlueSpacePotato/hsi-wizard/graph/badge.svg?token=85ASSSF2ZN)](https://codecov.io/gh/BlueSpacePotato/hsi-wizard)

# HSI Wizard

See Beyond the Visible: The Magic of Hyperspectral Imaging

<img src="./resources/imgs/logo/linkedin_banner_image_2.png" alt="">

HSI Wizard is a Python package designed to create a streamlined environment for hyperspectral imaging (HSI) analysis, from basic spectral analysis to advanced AI methods.

# Features
- DataCube Class for managing and processing HSI data.
- Spectral plotting and visualization.
- Clustering and spectral analytics.
- Tools for merging and processing spectral data.
- Data loaders for various file formats (e.g., NRRD, Pickle, TDMS, and XLSX).
- Decorators for method tracking, input validation, and execution time logging.

# Requirements
- [Python](https://www.python.org) >3.10

---

# Installation

## Via pip

You can install the package via pip:

```bash
pip install hsi-wizard
```

## Compile from Source

Alternatively, you can compile HSI Wizard from source:

```bash
python -m pip install -U pip setuptools wheel            # Install/update build tools
git clone https://github.com/BlueSpacePotato/hsi-wizard   # Clone the repository
cd hsi-wizard                                             # Navigate into the directory
python -m venv .env                                       # Create a virtual environment
source .env/bin/activate                                  # Activate the environment
pip install -e .                                          # Install in editable mode
pip install wheel                                         # Install wheel
pip install --no-build-isolation --editable .             # Compile and install hsi-wizard
```

---

# Documentation

The full documentation is available on ReadTheDocs:

### [Click here for Docs!](https://hsi-wizard.readthedocs.io)

---

# Usage

After installing the package, you can import the DataCube, read function, and plotter for quick HSI data analysis:
```python
from wizard import DataCube, read, plotter

# Load an HSI datacube from a file
datacube = read('path_to_file')

# Visualize the datacube
plotter(datacube)
```

---

# Modules

## Core
`DataCube`

The `DataCube` class is the primary object for storing and working with hyperspectral data. It contains attributes for the data cube, wavelengths, and metadata, as well as methods for data manipulation.

## Exploration
`plotter`

The `plotter` function enables you to easily visualize datacubes using various plotting methods, making it easier to explore hyperspectral data interactively.

## Utils
`helper`

Helper functions, such as find_nex_greater_wave and find_nex_smaller_wave, provide utilities for working with spectral data. These functions allow you to quickly find neighboring wavelengths based on a given value and a deviation.

`decorator`

This module contains decorators used throughout the package. Key decorators include:

check_load_dc: Ensures that loading functions return valid numpy arrays.
check_path: Validates file paths before processing.
track_execution_time: Measures and prints the execution time of functions for performance tracking.

## File Loaders

The package supports various file formats for hyperspectral data, including .nrrd, .pickle, .tdms, and .xlsx. Each file format has a dedicated loader function.

---

## Key Concepts

### DataCube
- A `DataCube` is a 3D array of shape `(v, x, y)`:
  - `x` and `y` represent the pixel dimensions.
  - `v` represents the spectral depth (wavelength).

Example:

```python
from hsi_wizard import DataCube

# Define an empty DataCube
datacube = DataCube()

# Access a spectrum for a specific pixel
spectrum = datacube[:, 3, 3]

# Access a 2D slice of the cube at a specific wavelength
img_2d = datacube[3]
```

### Difference Between `read` and `load`

- **`read`**: Used for importing dedicated file types (e.g., `.csv`, `.fsm`).
- **`load`**: Used for loading pre-processed data (e.g., existing numpy arrays).

---

## Pre-Processing Levels

Based on the idea from [DOI](https://www.doi.org/10.1007/s40010-017-0433-y), we categorize the processing stages:

- **Level 0**: Raw data captured directly from the sensor.
- **Level 1**: Data processed in a straightforward manner (e.g., noise reduction).
- **Level 2**: Heavily processed data, ready for advanced analysis.

---

## To-Do List
- [ ] Improved hyperparameter tuning using [evol](https://github.com/godatadriven/evol)
- [ ] R-support with [patsy](https://github.com/pydata/patsy)
- [x] Enhanced template creator.
- [ ] Functions for merging multiple spectra.
- [ ] Append spectra to existing datasets.
- [x] Saving files as `.nrrd`.
- [ ] Data normalization.
- [ ] Gaussian filter application.
- [ ] Reflectance calculation:
  \[
  I_{\text{ref}} = \frac{I_{\text{raw}} - I_{\text{dark}}}{I_{\text{white}} - I_{\text{dark}}}
  \]
- [ ] Optical density calculation:
  \[
  I_{\text{abs}} = -\log\left(\frac{I_{\text{raw}}}{I_{\text{ref}}}\right)
  \]
- [ ] Principal Component Analysis (PCA).
- [ ] Classification using Support Vector Machines (SVM).

---

## Changelog

The changelog will be added when the beta version is stable.

---

## Contributing

If you would like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. Please ensure that you adhere to the code style and include tests for any new features.

---

## Acknowledgements

Thanks to [Shopify](https://www.shopify.com) for providing a free logo-building tool via [Hatchful](https://www.shopify.com/tools/logo-maker).

Icons made by [Good Ware](https://www.flaticon.com/authors/good-ware) from [Flaticon](https://www.flaticon.com).

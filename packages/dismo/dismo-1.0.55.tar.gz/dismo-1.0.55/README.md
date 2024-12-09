# DIscrete Spatial MOdels

[![pipeline status](https://gitlab.com/qtb-hhu/dismo/badges/main/pipeline.svg)](https://gitlab.com/qtb-hhu/dismo/-/commits/main)
[![coverage report](https://gitlab.com/qtb-hhu/dismo/badges/main/coverage.svg)](https://gitlab.com/qtb-hhu/dismo/-/commits/main)
[![Documentation](https://img.shields.io/badge/Documentation-Gitlab-success)](https://qtb-hhu.gitlab.io/dismo/)
[![PyPi](https://img.shields.io/pypi/v/dismo)](https://pypi.org/project/dismo/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Downloads](https://pepy.tech/badge/dismo)](https://pepy.tech/project/dismo)

dismo is a Python package for building and analysing discrete spatial models based on ordinary differential equations.
Its primary purpose is to allow arbitrarily complex internal and transport processes to easily be mapped over multiple different regular grids.
For this it features one, two and three-dimensional layouts, with standard and non-standard (e.g. hexagonal or triangular) grids.


## Installation

If you quickly want to test out dismo, or do not require assimulo support, install dismo via

```bash
pip install dismo
```

To enable assimulo support, the easiest way is to install it via mamba using the [mambaforge](https://github.com/conda-forge/miniforge#mambaforge) distribution

```bash
mamba create -n py311 python=3.11 assimulo
mamba activate py311
pip install dismo
```

## License

[GPL 3](https://gitlab.com/qtb-hhu/dismo/blob/main/LICENSE)

## Documentation

The official documentation is hosted [here on gitlab](https://qtb-hhu.gitlab.io/dismo/).

## Issues and support

If you experience issues using the software please contact us through our [issues](https://gitlab.com/qtb-hhu/dismo/issues) page.

## Contributing to dismo

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.
See our [contribution guide](https://gitlab.com/qtb-hhu/dismo/blob/main/CONTRIBUTING.md) for more information.

## How to cite

dismo is currently in the publication process. You will find citing information here as soon as possible.

<!-- If you use this software in your scientific work, please cite [this article](https://rdcu.be/ckOSa):

van Aalst, M., Ebenhöh, O. & Matuszyńska, A. Constructing and analysing dynamic models with dismo v1.2.3: a software update. BMC Bioinformatics 22, 203 (2021)

- [doi](https://doi.org/10.1186/s12859-021-04122-7)
- [bibtex file](https://gitlab.com/qtb-hhu/dismo/blob/main/citation.bibtex) -->

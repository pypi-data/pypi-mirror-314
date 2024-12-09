# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dismo']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.8,<4.0',
 'numpy>=1.26,<2.0',
 'pandas>=2.1,<3.0',
 'pyarrow',
 'scipy>=1.12.0,<2.0.0',
 'typing-extensions>=4.9.0,<5.0.0']

setup_kwargs = {
    'name': 'dismo',
    'version': '1.0.55',
    'description': 'A subpackage of modelbase that enables investigation of PDE models',
    'long_description': '# DIscrete Spatial MOdels\n\n[![pipeline status](https://gitlab.com/qtb-hhu/dismo/badges/main/pipeline.svg)](https://gitlab.com/qtb-hhu/dismo/-/commits/main)\n[![coverage report](https://gitlab.com/qtb-hhu/dismo/badges/main/coverage.svg)](https://gitlab.com/qtb-hhu/dismo/-/commits/main)\n[![Documentation](https://img.shields.io/badge/Documentation-Gitlab-success)](https://qtb-hhu.gitlab.io/dismo/)\n[![PyPi](https://img.shields.io/pypi/v/dismo)](https://pypi.org/project/dismo/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n[![Downloads](https://pepy.tech/badge/dismo)](https://pepy.tech/project/dismo)\n\ndismo is a Python package for building and analysing discrete spatial models based on ordinary differential equations.\nIts primary purpose is to allow arbitrarily complex internal and transport processes to easily be mapped over multiple different regular grids.\nFor this it features one, two and three-dimensional layouts, with standard and non-standard (e.g. hexagonal or triangular) grids.\n\n\n## Installation\n\nIf you quickly want to test out dismo, or do not require assimulo support, install dismo via\n\n```bash\npip install dismo\n```\n\nTo enable assimulo support, the easiest way is to install it via mamba using the [mambaforge](https://github.com/conda-forge/miniforge#mambaforge) distribution\n\n```bash\nmamba create -n py311 python=3.11 assimulo\nmamba activate py311\npip install dismo\n```\n\n## License\n\n[GPL 3](https://gitlab.com/qtb-hhu/dismo/blob/main/LICENSE)\n\n## Documentation\n\nThe official documentation is hosted [here on gitlab](https://qtb-hhu.gitlab.io/dismo/).\n\n## Issues and support\n\nIf you experience issues using the software please contact us through our [issues](https://gitlab.com/qtb-hhu/dismo/issues) page.\n\n## Contributing to dismo\n\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.\nSee our [contribution guide](https://gitlab.com/qtb-hhu/dismo/blob/main/CONTRIBUTING.md) for more information.\n\n## How to cite\n\ndismo is currently in the publication process. You will find citing information here as soon as possible.\n\n<!-- If you use this software in your scientific work, please cite [this article](https://rdcu.be/ckOSa):\n\nvan Aalst, M., Ebenhöh, O. & Matuszyńska, A. Constructing and analysing dynamic models with dismo v1.2.3: a software update. BMC Bioinformatics 22, 203 (2021)\n\n- [doi](https://doi.org/10.1186/s12859-021-04122-7)\n- [bibtex file](https://gitlab.com/qtb-hhu/dismo/blob/main/citation.bibtex) -->\n',
    'author': 'Marvin van Aalst',
    'author_email': 'marvin.vanaalst@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<3.13',
}


setup(**setup_kwargs)

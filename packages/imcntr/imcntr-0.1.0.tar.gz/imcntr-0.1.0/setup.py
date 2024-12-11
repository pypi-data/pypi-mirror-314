# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['imcntr']

package_data = \
{'': ['*']}

install_requires = \
['jupyter>=1.1.1,<2.0.0',
 'pyserial>=3.5',
 'sphinx-autoapi>=3.3.3,<4.0.0',
 'sphinx-rtd-theme>=3.0.2,<4.0.0']

extras_require = \
{':python_version >= "3.9" and python_version < "4.0"': ['myst-nb>=1.1.2,<2.0.0']}

setup_kwargs = {
    'name': 'imcntr',
    'version': '0.1.0',
    'description': 'A package providing an API for imaging controller based on an Arduino Nano Every to communicate via serial port.',
    'long_description': '# imcntr\n\nA package providing an API for imaging controller based on an Arduino Nano Every to communicate via serial port.\n\n## Installation\n\n```bash\n$ pip install imcntr\n```\n\n## Usage\n\nThis package was developed to communicate with the controller of the neutron imaging experiment at TRIGA Mark II at Atominstitut of TU Wien. `imcntr` provides an API to access controller functionality via Python scripts. Communication is done via a serial port. The controller, and thus the package, can be used in general for imaging experiments with radiation. The controller provides a set of functions, such as moving the sample in and out of the beam, rotating the sample for tomographic experiments, and opening and closing the beam shutter. It provides an API to access controller functionality via Python scripts.\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`imcntr` was created by Clemens Trunner. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`imcntr` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Clemens Trunner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)

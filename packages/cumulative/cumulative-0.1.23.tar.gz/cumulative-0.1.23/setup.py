# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cumulative',
 'cumulative.datasets',
 'cumulative.examples',
 'cumulative.loaders',
 'cumulative.transforms',
 'cumulative.transforms.frame',
 'cumulative.transforms.row',
 'cumulative.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.1',
 'mltraq>=0.1.156',
 'pandas>=1.5.3',
 'scikit-learn>=1.2.2',
 'scipy>=1.11.4',
 'tqdm>=4.66.1']

setup_kwargs = {
    'name': 'cumulative',
    'version': '0.1.23',
    'description': 'Manipulate and Visualize Time Series Collections',
    'long_description': '<p align="center">\n<img width="75%" height="75%" src="https://elehcimd.github.io/cumulative/assets//img/logo-wide-black.svg" alt="Cumulative Logo">\n</p>\n\n<p align="center">\n<img src="https://elehcimd.github.io/cumulative/assets/img/badges/test.svg" alt="Test">\n<img src="https://elehcimd.github.io/cumulative/assets//img/badges/coverage.svg" alt="Coverage">\n<img src="https://elehcimd.github.io/cumulative/assets//img/badges/python.svg" alt="Python">\n<img src="https://elehcimd.github.io/cumulative/assets//img/badges/pypi.svg" alt="PyPi">\n<img src="https://elehcimd.github.io/cumulative/assets//img/badges/license.svg" alt="License">\n<img src="https://elehcimd.github.io/cumulative/assets//img/badges/code-style.svg" alt="Code style">\n</p>\n\n---\n\n<h1 align="center">\nManipulate and Visualize Time Series Collections\n</h1>\n\nAn open-source Python library for Data Scientists to efficiently manipulate collections of time series data. Features include data loading, transformation, persistence, and visualization.\n\n---\n\n* **Documentation**: [https://elehcimd.github.io/cumulative](https://elehcimd.github.io/cumulative)\n* **Source code**: [https://github.com/elehcimd/cumulative](https://github.com/elehcimd/cumulative) (License: [BSD 3-Clause](https://elehcimd.github.io/cumulative/license/))\n* **Discussions**: [Ask questions, share ideas, engage](https://github.com/elehcimd/cumulative/discussions)\n* **Funding**: You can [star](https://github.com/elehcimd/cumulative) the project on GitHub and [hire me](https://www.linkedin.com/in/dallachiesa/) to make sense of your time series.\n\n---\n\n',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele.dallachiesa@sigforge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://elehcimd.github.io/cumulative/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0',
}


setup(**setup_kwargs)

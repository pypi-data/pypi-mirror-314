# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['speedtab']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=2.58.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'speedtab',
    'version': '0.2.4.5',
    'description': 'Convenient wrapper for working with Google Spreadsheets',
    'long_description': None,
    'author': 'Bogdan Gergel',
    'author_email': 'bogger147@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BoggerSancho/SpeedTab-beta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

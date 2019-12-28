# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['lib']

package_data = \
{'': ['*']}

install_requires = \
['asyncio==3.4.3',
 'discord.py==1.2.5',
 'flask',
 'pymysql==0.7.2',
 'python-dotenv',
 'requests==2.21.0']

setup_kwargs = {
    'name': 'lib',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

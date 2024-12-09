# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trollbot']

package_data = \
{'': ['*']}

install_requires = \
['python-socketio==4.6.1']

entry_points = \
{'console_scripts': ['sample = examples.01_sample:ignore',
                     'testcmd = examples.02_test_cmd:ignore']}

setup_kwargs = {
    'name': 'trollbot',
    'version': '1.0',
    'description': 'A python library dedicated to making bots for Trollbox (and chatrooms alike)',
    'long_description': '# Trollbot\n*Amazing names*\n\nWith this library you will be able to easily create trollbox bots.\n\nIf you need any assistance, please check the examples folder for some examples.\n\nDocumentation will arrive soon. I have marked which functions you should use whilst developing your bot in the trollbot/bot.py Bot class, and if you wish to use any features that have not yet been implement, then you need to manually do that with the socketio object contained within the Bot object (bot.socket).',
    'author': 'mewhenthe',
    'author_email': 'xsare435@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

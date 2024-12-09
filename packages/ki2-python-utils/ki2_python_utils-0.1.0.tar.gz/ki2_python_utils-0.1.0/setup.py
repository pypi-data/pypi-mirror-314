# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ki2_python_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ki2-python-utils',
    'version': '0.1.0',
    'description': '',
    'long_description': "# ki2 - Python Utility Elements\n\n## Installation\n\nTo install using pip:\n\n```\npip install ki2-python-utils\n```\n\nOr, if you're using Poetry:\n\n```\npoetry add ki2-python-utils\n```\n",
    'author': 'Adrien KERFOURN',
    'author_email': 'ak.sitecontact@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

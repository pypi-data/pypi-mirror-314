# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whylabs_toolkit',
 'whylabs_toolkit.container',
 'whylabs_toolkit.helpers',
 'whylabs_toolkit.monitor',
 'whylabs_toolkit.monitor.diagnoser',
 'whylabs_toolkit.monitor.diagnoser.converters',
 'whylabs_toolkit.monitor.diagnoser.helpers',
 'whylabs_toolkit.monitor.diagnoser.models',
 'whylabs_toolkit.monitor.diagnoser.recommendation',
 'whylabs_toolkit.monitor.manager',
 'whylabs_toolkit.monitor.models',
 'whylabs_toolkit.monitor.models.analyzer',
 'whylabs_toolkit.utils']

package_data = \
{'': ['*'], 'whylabs_toolkit.monitor': ['schema/*']}

install_requires = \
['jsonschema>=4.17.3,<5.0.0',
 'pydantic>=1.10.15,<2.0.0',
 'typing-extensions>=4.11.0,<5.0.0',
 'urllib3>=2.0.2,<2.1',
 'whylabs-client>=0.6.3,<0.7.0',
 'whylogs>=1.1.26,<2.0.0']

extras_require = \
{'diagnoser': ['pandas>=2.0.3,<3.0.0',
               'numpy>=1.24.1,<2.0.0',
               'tabulate>=0.8.9,<0.9.0',
               'isodate>=0.6.1,<0.7.0',
               'python-dateutil>=2.8.2,<3.0.0']}

setup_kwargs = {
    'name': 'whylabs-toolkit',
    'version': '0.1.2',
    'description': 'Whylabs Toolkit package.',
    'long_description': "# WhyLabs Toolkit\n\nThe WhyLabs Toolkit package contains helper methods to help users interact with our internal APIs. Users will benefit from using it if they want to abstract some of WhyLabs' internal logic and also automate recurring API calls.\n\n\n## Basic usage\nTo start using the `whylabs_toolkit` package, install it from PyPI with:\n```bash\npip install whylabs_toolkit\n``` \n\n## Packages\n\nThe available packages that we have enable different use-cases for the `whylabs_toolkit`. To get started, navigate to one of the following sections and find useful tutorials there.\n\n| Package                                                                                                                   | Usage                                                                  |\n|---------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|\n| [Monitor Manager](https://github.com/whylabs/whylabs-toolkit/blob/mainline/whylabs_toolkit/monitor/manager/README.md)     | Author and modify existing WhyLabs monitor with Python.                |\n| [Monitor Diagnoser](https://github.com/whylabs/whylabs-toolkit/blob/mainline/whylabs_toolkit/monitor/diagnoser/README.md) | Diagnose problems with monitors.                                       |\n| [WhyLabs Helpers](https://github.com/whylabs/whylabs-toolkit/blob/mainline/whylabs_toolkit/helpers/README.md)             | Interact with and modify your Datasets and ML Models specs in WhyLabs. |\n\n## Development\n\nTo start contributing, you will manage dependencies with [Poetry](https://python-poetry.org/) and also a handful of `Makefile` commands. To install all necessary dependencies and activate the virtual environment, run:\n\n```bash\nmake setup && poetry shell\n```\n\n## Get in touch\nIf you want to learn more how you can benefit from this package or if there is anything missing, please [contact our support](https://whylabs.ai/contact-us), we'll be more than happy to help you!",
    'author': 'Murilo Mendonca',
    'author_email': 'murilommen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

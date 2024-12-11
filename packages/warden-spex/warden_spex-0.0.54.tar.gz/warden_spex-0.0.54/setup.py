# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['warden_spex']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.10.0',
 'mltraq>=0.1.156,<0.2.0',
 'numpy>=2.1.3,<3.0.0',
 'pydantic>=2.10.3,<3.0.0',
 'pytest>=8.2.2,<9.0.0',
 'rbloom>=1.5.1,<2.0.0',
 'ruff>=0.0.128']

setup_kwargs = {
    'name': 'warden-spex',
    'version': '0.0.54',
    'description': 'Statistical Proof of Execution (SPEX) by Warden Protocol',
    'long_description': '# Statistical Proof of Execution (SPEX)\n\nThis repository serves as entrypoint for documentation and implementation of the SPEX protocol.\nSPEX is open source and brought to you by [Warden Protocol](https://wardenprotocol.org/).\nWe encourage developers to use and extend SPEX in their own initiatives.\n\n## Motivations\n\nAs a developer, you want to protect your computational pipeline from manipulation.\nSPEX offers third parties a **secure**, **fast** and **simple** interface for verifying computation\nsuch as in data processing pipelines and ML/AI inference workloads.\n\n## Installation\n\nTo install SPEX:\n\n```\npip install warden_spex --upgrade\n```\n\n**Important**: SPEX is progressing rapidly and interfaces might change at any time.\nPin its exact version for your project, to make sure it all works.\nHave tests for your project, and update it once you verify that things work correctly.\n\n## Usage\n\nSPEX is a protocol defining the communication between the actors ***user***, ***solver*** and ***verifier***. The interaction:\n\n1. The ***user*** requests the execution of a computational pipeline to ***solver*** given some `inputs`\n2. The ***Solver*** computes the `outputs` and their `receipt`, communicating them back to the ***user***\n3. The ***User*** requests the verification of the computation to ***verifier*** given `inputs` and `receipt`\n\nThe core building block of the implementation is the `Solver` abstract class defined in [models.py](./src/warden_spex/models.py)\nthat the developer needs to implement.\nA reference implementation for the class is provided by the `SimpleSolver` class in [test_spex.py](./tests/test_spex.py), \nwhich implements the `solve` (step 2) and `verify` (step 3) methods.\n\nThe verification process re-executes a randomized portion of the computational pipeline to verify its integrity,\nevaluating a certain percentage of the computation.\n\n## LICENSE\n\n```\nCopyright 2024 Warden Protocol <https://wardenprotocol.org/>\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n```',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele@wardenprotocol.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<4.0',
}


setup(**setup_kwargs)

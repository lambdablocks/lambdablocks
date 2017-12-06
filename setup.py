# Copyright 2017 The Lambda-blocks developers. See AUTHORS for details.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
https://packaging.python.org/tutorials/distributing-packages/
"""

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lambdablocks',
    version='0.1',

    description='Data processing with topologies of blocks',
    long_description=long_description,
    url='https://github.com/lambdablocks/lambdablocks',

    # Author details
    author='The Lambda-blocks developers',
    author_email='todo@example.org',

    # Choose your license
    license='Apache Software License',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='blocks engine',

    packages=['lb', 'lb.blocks', 'lb.plugins'],

    # install_requires=['yaml', 'matplotlib', 'requests-oauthlib'],
    install_requires=['pyyaml'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['nose2', 'nose2-cov'],
    },
    package_data={
    },

    scripts=['bin/blocks.py'],
)

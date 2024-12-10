# This file is part of pdu-control
# Copyright (C) 2023 Safran
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='pducontrol',
    version='1.5.1',
    packages=["pducontrol"],
    entry_points={
        'console_scripts': [
            'pducontrol=pducontrol.__main__:main'
        ]
    },
    install_requires=[
        'requests',
        'tabulate',
        'argcomplete',
        'xmltodict'
    ],
    author='Pol Bodet, Nicolas Carrier, Jeremy Connat, Jai Mehra',
    author_email="pol.bodet@orolia.com",
    url="https://bitbucket.org/spectracom/pdu-control/src/master/",
    description='A simple package to control PDUs',
    long_description_content_type="text/markdown",
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    license="LGPLv3+"
)

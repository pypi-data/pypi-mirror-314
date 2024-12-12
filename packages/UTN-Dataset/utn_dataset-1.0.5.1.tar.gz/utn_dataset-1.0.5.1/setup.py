# Copyright (C) 2024 <UTN FRA>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
from UTN_Dataset import VERSION

setup(
    name= 'UTN_Dataset',
    version=VERSION,
    description= 'Set de datos con informacion de pokemones',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author= 'Facundo Falcone',
    author_email="ffalcone@fra.utn.edu.ar",
    maintainer='Facundo Falcone',
    maintainer_email="ffalcone@fra.utn.edu.ar",
    url= 'https://pypi.org/project/UTN-Dataset/',
    packages= find_packages(),
    py_modules=['UTN_Dataset'],
    requires=['setuptools', 'tabulate'],
    install_requires=['setuptools', 'tabulate'],
    include_package_data=True,
    entry_points={
      'console_scripts': ['UTN_Dataset=UTN_Dataset.funciones:saludo']  
    },
    script_name='UTN_Dataset:saludo',
    keywords=['UTN_Dataset', 'UTN-FRA'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11'
)
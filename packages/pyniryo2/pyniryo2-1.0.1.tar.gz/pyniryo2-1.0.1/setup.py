# coding=utf-8

from io import open
from setuptools import find_packages, setup

version = '1.0.1'


with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

with open('requirements.txt', 'r') as f:
    REQUIRES = [str(line.replace("\n", "")) for line in f.readlines()]

kwargs = {
    'name': 'pyniryo2',
    'version': version,
    'description': 'Package to control Niryo Robot "Ned" through TCP',
    'long_description': readme,
    'long_description_content_type': 'text/markdown',
    'author': 'Niryo',
    'author_email': 'v.pitre@niryo.com',
    'maintainer': 'Valentin Pitre',
    'maintainer_email': 'v.pitre@niryo.com',
    'install_requires': REQUIRES,
    'include_package_data': True,
    'url': 'https://github.com/NiryoRobotics/pyniryo2',
    'license': 'GNU 3.0',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Topic :: Education",
    ],
    'packages': find_packages(exclude=('tests', 'tests.*')),
}

setup(**kwargs)

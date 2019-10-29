from setuptools import setup, find_packages
from os.path import dirname, join, abspath
import sys

from activity_tracker.meta import __version__, __package_name__, __author_name__, __application_name__
from activity_tracker.meta import __author_email__, __package_description__, __package_long_description__

project_root = dirname(abspath(__file__))
with open(join(project_root, f'requirements_{sys.platform}.txt')) as read_file:
    required_packages = read_file.read().splitlines()

setup(
    name=__package_name__,
    version=__version__,
    author=__author_name__,
    author_email=__author_email__,
    description=__package_description__,
    long_description=__package_long_description__,
    install_requires=required_packages,
    packages=find_packages(),
    package_data={'': ['../data/*.sh', '../data/*.scpt', '../data/*.json']},
    entry_points={
        'gui_scripts': [
            f'{__application_name__} = activity_tracker.app:main'
        ],
    }
)

from setuptools import setup, find_packages
import sys
from os.path import expanduser, join
from activity_tracker.meta import __version__, __application_name__, __author_name__
from activity_tracker.meta import __author_email__, __package_description__, __package_long_description__


env_name = 'activity'
anaconda_runtime = expanduser(f'~/anaconda3/envs/{env_name}/lib/libpython3.7m.dylib')

APP = ['activity_tracker/app.py']
OPTIONS = {
    'packages': ['rumps', 'Quartz'],
    'argv_emulation': True,
    'plist': {
        'PyRuntimeLocations': [
            '@executable_path/../Frameworks/libpython3.7m.dylib',
            anaconda_runtime
        ]
    }
}
DATA_FILES = [('', ['scripts'])]

setup(
    app=APP,
    data_files=DATA_FILES,
    # name='activity-tracker',
    name=__application_name__,
    version=__version__,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    author=__author_name__,
    author_email=__author_email__,
    description=__package_description__,
    long_description=__package_long_description__,
    packages=find_packages(),
)
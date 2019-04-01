import sys

from setuptools import setup

sys.path.append('.')
import translator

setup(
    name='translator',
    version=translator.__version__,
    author='Balazs Kulcsar',
    author_email='kulcsarb@gmail.com',
    description='Translator API',
    packages=['translator'],
    entry_points={
        'console_scripts': [
            'translator-api=translator.api'
        ]
    }
)

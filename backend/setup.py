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
    install_requires=[
        'eventlet',
        'socketio',
        'dotenv',
        'celery'
    ],
    entry_points={
        'console_scripts': [
            'translator-api=translator.api'
        ]
    }
)

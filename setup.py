import re

from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'todo.py')) as f:
    version = re.match('.*__version__ = \'(.*?)\'', f.read(), re.S).group(1)


dependencies = [
    'easycli',
]


setup(
    name='todo',
    version=version,
    packages=find_packages(exclude=['tests']),
    py_modules=['todo'],
    install_requires=dependencies,
    include_package_data=True,
    license='MIT',
    entry_points={
        'console_scripts': [
            'todo = todo:Todo.quickstart',
        ]
    }
)


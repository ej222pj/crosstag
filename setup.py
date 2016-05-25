# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='crosstag',
    version='2.0.0',
    description='Tag-in an member handing system for a gym',
    long_description=(read('README.md') + '\n\n' +
                      read('HISTORY.rst') + '\n\n' +
                      read('AUTHORS.rst')),
    url='https://github.com/ej222pj/crosstag',
    license='MIT',
    author='Johan Lundstrom',
    author_email='lundstrom.se@gmail.com',
    py_modules=['crosstag'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['Flask', 'Flask-WTF', 'Jinja2', 'WTForms',
                      'grequests', 'pyfiglet', 'pypyodbc', 'py-bcrypt'],
)
# -*- coding: utf-8 -*-
import sys

from setuptools import setup
from setuptools.command.test import test


class Tox(test):
    def initialize_options(self):
        test.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        sys.exit(tox.cmdline())

setup(
    name='timer.py',
    version='0.1',
    description='Wrapper around the timerfd interface to create a pollable timer.',
    url='https://github.com/hackaugusto/timer.py',
    author='Augusto F. Hack',
    author_email='hack.augusto@gmail.com',
    license='MIT',

    py_modules=['timer'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    keywords=['timer'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
)

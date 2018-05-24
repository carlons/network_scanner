from __future__ import print_function
from setuptools.command.test import test as TestCommand
import io
import codecs
import setuptools
import os
import sys

sys.path.append('/home/carlons/workspace_py/network_scanner/')
with io.open("README.md", "r") as fh:
    long_description = fh.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setuptools.setup(
    name='network_scanner',
    version='0.1.0',
    url='http://github.com/carlons/',
    license='Apache Software License',
    author='Xikun Huang',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    author_email='huangxikun@amss.ac.cn',
    description='network_scanner',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    platforms='any',
    test_suite='',
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
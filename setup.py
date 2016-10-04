from setuptools import setup
import sys
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='confipy',
    version='0.0.1',
    packages=['confipy'],
    url='https://github.com/mansenfranzen/confipy',
    license='MIT',
    author='Franz Woellert',
    author_email='franz.woellert@gmail.com',
    description='A convenient config file reader.',
    install_requires=['PyYAML', 'six'],
    download_url = 'https://github.com/mansenfranzen/confipy/tarball/0.0.1',
    keywords = ['config', 'yaml'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest}
)

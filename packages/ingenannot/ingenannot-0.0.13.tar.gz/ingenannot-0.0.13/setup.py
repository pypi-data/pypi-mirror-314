import sys
import unittest
import logging

from distutils.cmd import Command
from distutils.core import setup, Extension
from unittest import TextTestRunner, TestLoader, TestSuite


#class TestSuite(Command):
#    user_options = []

#    def initialize_options(self):
#        pass

#    def finalize_options(self):
#        pass

#    def run(self):

#        logging.disable(logging.CRITICAL)

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


def get_version():
    sys.path.insert(0, "ingenannot")
    import version
    return version.__version__

#exec(open("Ingenannot/version.py").read())


setup(name='ingenannot',
#      version = __version__,
      version = get_version(),
      description='InGenAnnot: Inspection of Gene Annotation',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Nicolas Lapalu',
      author_email='nicolas.lapalu@inrae.fr',
      url="https://forgemia.inra.fr/bioger/ingenannot",
      license_files = ('LICENSE',),
      install_requires=[
          'numpy',
          'pysam',
          'matplotlib',
          'pandas',
          'upsetplot',
          'seaborn',
          'scikit-bio'
          ],
      entry_points = {
        'console_scripts': ['ingenannot=ingenannot.main:main'],
      },
      packages = ['ingenannot','ingenannot.commands','ingenannot.entities','ingenannot.utils'],
      test_suite = 'tests',
#      cmdclass={
#          'test': TestSuite
#      },
      classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.7",
      ]
      )

import os, sys, re, codecs
from setuptools import setup, find_packages

def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()

long_description = read('README.md')

setup(name="wikigps",
      version="0.1",
      description="A tool for automatically attaching GPS coordinates from a wikipedia page to a photo.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
      ],
      keywords='wikipedia gps photos exif jpg jpeg',
      author='Colm O\'Connor',
      author_email='colm.oconnor.github@gmail.com',
      license='MIT',
      install_requires=['argh', 'requests', 'jexifs',],
      package_data={},
      entry_points=dict(console_scripts=['wikigps=wikigps:cli.run',]),
      zip_safe=False,
)

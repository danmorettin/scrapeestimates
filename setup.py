
""" to allow 'python setup.py develop' at the command line """

from setuptools import setup, find_packages

setup(name='scrapeestimates',
      version='1.1.0',
      packages=find_packages(),
      install_requires=[
        'pandas',
        'requests',
        'lxml'
      ],
      entry_points={'console_scripts': [
        'scrapeestimates = scrapeestimates.application:main'
        ]}
      )

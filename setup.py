
""" python setup.py install or python setup.py develop """

from setuptools import setup, find_packages

setup(name='scrapeestimates',
      version='1.1.0',
      packages=find_packages(),
      entry_points={'console_scripts': [
        'scrapeestimates = scrapeestimates.application:main']}
      )

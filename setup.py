# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_pypi_stats import __version__

REQUIREMENTS = [
    'requests',
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-pypi-stats',
    version=__version__,
    description='Simple plugin to add dynamic stats from PyPI packages.',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://pypi.com/aldryn/aldryn-pypi-stats',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    # test_suite="test_settings.run",
)

#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from codecs import open

pkg_name = 'zwdocs'

here = os.path.abspath(os.path.dirname(__file__))
exclude_packages = ['tests']
packages = find_packages()
packages = [pkg for pkg in packages if all(p != pkg for p in exclude_packages)]

requires = [s.strip() for s in open('requirements.txt').readlines()]
test_requirements = [s.strip() for s in open('requirements_dev.txt').readlines()][4:]

about = {}
lines = []
pth = os.path.join(here, pkg_name, '__version__.py')
if not os.path.exists(pth):
    print('ERROR: __version__.py NOT FOUND in: %s'%pth)
    exit(1)
with open(pth, 'r', 'utf-8') as f:
    exec(f.read(), about)
    # auto update min version number for every dist upload
    verarr = about['__version__'].split('.') if '__version__' in about else '0.0.0'.split('.')
    verarr[2] = str(int(verarr[2])+1)
    about['__version__'] = '.'.join(verarr)
    f.seek(0)
    lines = list(f.readlines())
    print(lines)
    for i,s in enumerate(lines):
        if s.startswith('__version__'):
            lines[i] = "__version__ = '%s'\n"%about['__version__']
with open(pth, 'w', 'utf-8') as f:
    f.seek(0)
    f.writelines(lines)

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={pkg_name:pkg_name},
    include_package_data=True,
    install_requires=requires,
    tests_require=test_requirements,
    python_requires='>=3.6',
    platforms=["all"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)





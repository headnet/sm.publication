import os
import sys

reload(sys).setdefaultencoding("UTF-8")

from setuptools import setup, find_packages


def read(*pathnames):
    fh = open(os.path.join(os.path.dirname(__file__), *pathnames))
    return fh.read().decode('utf-8')

version = '1.1'

setup(
    name='sm.publication',
    version=version,
    description="Publication module for SM/AST.",
    long_description='\n'.join([
        read('README.rst'),
        read('CHANGES.rst'),
    ]),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
    ],
    keywords='plone sm ast publication',
    author='Bo Simonsen',
    author_email='bo@headnet.dk',
    license="GPLv2+",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['sm'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.dexterity'
    ],
    extras_require={
        'test': [
            'plone.testing',
            'plone.app.testing',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)

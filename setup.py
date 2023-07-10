""" setup """
# coding: utf-8

from setuptools import find_packages, setup

NAME = "swagger_server"
VERSION = "2.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="SDX LC",
    author_email="yxin@renci.org",
    url="",
    keywords=["Swagger", "SDX LC"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={"": ["swagger/swagger.yaml"]},
    include_package_data=True,
    entry_points={"console_scripts": ["swagger_server=swagger_server.__main__:main"]},
    long_description="""\
    You can find out more about Swagger at [http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/). 
    """,
    packages=find_packages(exclude=['tests']),
    install_requires='install_requires',
    extras_require={'dev': [
        'pip-tools >= 2.0',
        'pytest==7.2.1',
        'pytest-cov==4.0.0',
        'pytest-asyncio==0.20.3',
        'black==23.3.0',
        'isort==5.12.0',
        'pylint==2.15.0',
        'pycodestyle==2.10.0',
        'yala==3.2.0',
        'tox==3.28.0',
        'typing-extensions==4.5.0'
        ]},
    cmdclass={
        'clean': 'Cleaner',
        'coverage': 'TestCoverage',
        'doctest': 'DocTest',
        'egg_info': 'EggInfo',
        'lint': 'Linter',
        'test': 'Test'
        },
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Networking',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        ]
    )

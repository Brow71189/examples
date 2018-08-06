# -*- coding: utf-8 -*-

"""
To upload to PyPI, PyPI test, or a local server:
python setup.py bdist_wheel upload -r <server_identifier>
"""

import setuptools

setuptools.setup(
    name="swift-examples",
    version="0.0.1",
    author="Andreas Mittelberger",
    author_email="Brow7118@gmail.com",
    description="Examples package for Nion Swift.",
    packages=["nionswift_plugin.swift_examples"],
    install_requires=[],
    license='GPLv3',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True,
    python_requires='~=3.6',
    zip_safe=False
)

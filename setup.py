# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from setuptools import setup, find_packages

setup(
    name             = 'tlga',
    version          = '1.0.0',
    author           = 'Dorival M Pedroso',
    author_email     = 'dorival.pedroso@gmail.com',
    packages         = find_packages(),
    url              = 'http://github.com/cpmech/tlga/',
    license          = 'LICENSE',
    description      = 'Python Simple Genetic Algorithms',
    long_description = open('README').read(),
    install_requires=[
        "matplotlib >= 1.4.2",
        "numpy >= 1.8.2",
        "scipy >= 0.14.1",
    ],
)

#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'vaultutils-py',
  version = '0.0.0',
  license = 'MIT',
  description = open('README.md').read(),
  author = "Daniel Piet0",
  author_email = "daniel.piet@datadoghq.com",
  url = 'https://github.com/datadog/vaultutils-py',
  platforms = 'any',
  packages = setuptools.find_packages(),
  zip_safe = True,
  verbose = False,
)

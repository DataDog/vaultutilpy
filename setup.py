#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'vaultutilpy',
  version = '0.0.0',
  license = 'MIT',
  description = open('README.md').read(),
  author = "Daniel Piet",
  author_email = "daniel.piet@datadoghq.com",
  url = 'https://github.com/datadog/vaultutilpy',
  platforms = 'any',
  packages = setuptools.find_packages(),
  zip_safe = True,
  verbose = False,
)

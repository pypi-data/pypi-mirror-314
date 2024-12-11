#!/usr/bin/env python

import os
from setuptools import setup

release = "1.5.1"

root_package = "sardana.PoolController"
package_dir = {root_package: "python"}


provides = ['python']

source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python")
subpackages = [root_package + x[0][len(source_dir):].replace("/", ".")
               for x in os.walk(source_dir)]

packages = [root_package]
packages.extend(subpackages)

setup(name='PoolController',
      version=release,
      author="Sardana Controller Developers",
      author_email="fs-ec@desy.de",
      maintainer="DESY",
      maintainer_email="fs-ec@desy.de",
      url="https://github.com/desy-fsec/sardana-controllers/",
      packages=packages,
      package_dir=package_dir,
      include_package_data=True,
      provides=provides,
      )

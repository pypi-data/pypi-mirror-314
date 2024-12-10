#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
#############################################
# File Name: setup.py
# Author: cikuu
# Mail: info@cikuu.com
# Created Time: 2024-12-8
#############################################
 
from setuptools import setup, find_packages
 
setup(
  name = "xfunc",
  version = "2024.12.10.1",
  keywords = ("pip"),
  description = "cikuu tools",
  long_description = "add replace into soinit",
  license = "MIT Licence",
 
  url = "http://www.cikuu.com",
  author = "cikuu",
  author_email = "info@cikuu.com",
 
  packages = find_packages(),
  include_package_data = True,
  platforms = "any", 
  install_requires = ["redis","fire"]  
)

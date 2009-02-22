#!/usr/bin/env python

from __future__ import print_function

import _mysql
from jaraco.mysql import _mysql as jaraco_mysql

jaraco_dir = set(dir(jaraco_mysql))
ref_dir = set(dir(_mysql))

print("items in reference not in jaraco:")
print(str(ref_dir - jaraco_dir))
print("items in jaraco not in reference:")
print(str(jaraco_dir - ref_dir))
#!/usr/bin/env python

"""
This script should be run once on each target platform to generate the
Python API from the MySQL header files.

Prerequisites:
1) MySQL 5.1 with developer headers (libmysqlclient-dev on Unix)
2) gccxml
3) ctypeslib

For more information on this technique, visit

"""

import sys
import subprocess
from ctypeslib import h2xml, xml2py

print('Generating xml')

platform_map = dict(
	linux2 = 'unix',
	darwin = 'unix',
)

def gen_libs_win32():
	raise NotImplementedError

def gen_libs_unix():
	common_args = ['h2xml.py', '-I', '/usr/include/mysql']
	cmds = [
		'mysql.h -o mysql.xml'.split(),
		'-c errmsg.h -o errmsg.xml'.split(),
		'-c mysql_version.h -o mysql_version.xml'.split(),
		'-c mysqld_error.h -o mysqld_error.xml'.split(),
	]

	for cmd in cmds:
		assert h2xml.compile_to_xml(common_args + cmd) is None, cmd + ' failed'

	common_args = ['xml2py.py']

	cmds = [
		'mysql.xml -l libmysqlclient.so -o _mysql_api_unix.py'.split(),
		'errmsg.xml -o root/_mysql_errmsg.py'.split(),
		'mysql_version.xml -o root/_mysql_version.py'.split(),
		'mysqld_error.xml -o root/_mysql_errors.py'.split(),
		]
	for cmd in cmds:
		assert xml2py.main(common_args + cmd) is None, cmd + ' failed'


vars()['gen_libs_'+platform_map[sys.platform]]()

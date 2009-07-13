#!/usr/bin/env python

"""
This script should be run once on each target platform to generate the
Python API from the MySQL header files.

Prerequisites:
1) MySQL 5.1 with developer headers (libmysqlclient-dev on Unix)
2) gccxml
3) ctypeslib

For more information on this technique, visit
http://web.archive.org/web/20080115092643/starship.python.net/crew/theller/wiki/CodeGenerator

Also consider looking at the old docs:
http://starship.python.net/crew/theller/ctypes/old/codegen.html

"""

import sys
import os
import subprocess
from ctypeslib import h2xml, xml2py

print('Generating xml')

platform_map = dict(
	linux2 = 'unix',
	darwin = 'unix',
)

setup_root = os.path.dirname(__file__)

def merge_args(common_args, variable_args):
	for args in variable_args:
		yield common_args + args

def h2xml_cmd(args):
	assert h2xml.compile_to_xml(args) is None, cmd + ' failed'

def xml2py_cmd(args):
	assert xml2py.main(args) is None, cmd + ' failed'

def gen_libs_win32():
	sys.path.append(os.path.join(setup_root, 'root'))
	from _mysql_api_util import get_mysql_root
	mysql_include = os.path.join(get_mysql_root(), 'include')
	os.environ['PATH'] += ';%s\lib\opt' % get_mysql_root()
	common_args = ['h2xml.py', '-I', mysql_include]
	cmds = [
		# need WIN32_LEAN_AND_MEAN to exclude most windows stuff
		'-D WIN32_LEAN_AND_MEAN config-win.h mysql.h -o mysql.xml'.split(),
		'-c errmsg.h -o errmsg.xml'.split(),
		'-c mysql_version.h -o mysql_version.xml'.split(),
		'-c mysqld_error.h -o mysqld_error.xml'.split(),
	]
	cmds = merge_args(common_args, cmds)
	map(h2xml_cmd, cmds)

	common_args = ['xml2py.py']
	
	cmds = [
		'mysql.xml -l libmysql.dll -o _mysql_api_win32.py'.split(),
		# Use -s MYSQL to get the MYSQL structure and ancestral structures
		'errmsg.xml -o root/_mysql_errmsg.py'.split(),
		'mysql_version.xml -o root/_mysql_version.py'.split(),
		'mysqld_error.xml -o root/_mysql_errors.py'.split(),
		]
	cmds = merge_args(common_args, cmds)
	map(xml2py_cmd, cmds)
	patch_mysql_api()

def gen_libs_unix():
	mysql_include = '/usr/include/mysql'
	common_args = ['h2xml.py', '-I', mysql_include]
	cmds = [
		'mysql.h -o mysql.xml'.split(),
		'-c errmsg.h -o errmsg.xml'.split(),
		'-c mysql_version.h -o mysql_version.xml'.split(),
		'-c mysqld_error.h -o mysqld_error.xml'.split(),
	]
	cmds = merge_args(common_args, cmds)
	map(h2xml_cmd, cmds)

	common_args = ['xml2py.py']

	cmds = [
		'mysql.xml -l libmysqlclient.so -o _mysql_api_unix.py'.split(),
		'errmsg.xml -o root/_mysql_errmsg.py'.split(),
		'mysql_version.xml -o root/_mysql_version.py'.split(),
		'mysqld_error.xml -o root/_mysql_errors.py'.split(),
		]
	cmds = merge_args(common_args, cmds)
	map(xml2py_cmd, cmds)
	
	patch_mysql_api()

def patch_mysql_api():
	"""
	Todo:
	1) Change my_bool = c_char to my_bool = c_int8
	2) Change mysql_autocommit arg2 from c_char to my_bool
	3) Patch to support robust library location
	"""
	print patch_mysql_api.__doc__

def get_platform_name():
	return platform_map.get(sys.platform, sys.platform)

vars()['gen_libs_'+get_platform_name()]()

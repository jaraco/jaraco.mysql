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

setup_root = os.path.dirname(__file__)
sys.path.append(os.path.join(setup_root, 'root'))
from _mysql_api_util import get_mysql_root, get_platform_name

def merge_args(common_args, variable_args):
	for args in variable_args:
		yield common_args + args

class LibGenerator(object):
	h2xml_cmds = [
		# need WIN32_LEAN_AND_MEAN to exclude most windows stuff
		'mysql.h -o mysql.xml'.split(),
		'-c errmsg.h -o errmsg.xml'.split(),
		'-c mysql_version.h -o mysql_version.xml'.split(),
		'-c mysqld_error.h -o mysqld_error.xml'.split(),
	]
	xml2py_cmds = [
		'mysql.xml -l %(libname)s -o root/_mysql_api.py'.split(),
		# Use -s MYSQL to get the MYSQL structure and ancestral structures
		'errmsg.xml -o root/_mysql_errmsg.py'.split(),
		'mysql_version.xml -o root/_mysql_version.py'.split(),
		'mysqld_error.xml -o root/_mysql_errors.py'.split(),
		]
	
	def h2xml_cmd(self, args):
		assert h2xml.compile_to_xml(args) is None,  cmd + ' failed'

	def xml2py_cmd(self, args):
		assert xml2py.main(args) is None, cmd + ' failed'

	def run(self):
		print('Generating xml')
		h2xml_common = ['h2xml.py', '-I', self.mysql_include]
		cmds = merge_args(h2xml_common, self.h2xml_cmds)
		map(self.h2xml_cmd, cmds)
		
		print('Generating Python libs')
		xml2py_common = ['xml2py.py']
		xml2py_cmds = self.xml2py_cmds
		xml2py_cmds[0] = xml2py_cmds[0] % self.__dict__
		cmds = merge_args(xml2py_common, self.xml2py_cmds)
		map(self.xml2py_cmd, cmds)
		
		patch_mysql_api()

class Win32LibGenerator(LibGenerator):
	platform = 'win32'
	libname='libmysql.dll'
	mysql_include = os.path.join(get_mysql_root(), 'include')
	# need WIN32_LEAN_AND_MEAN to exclude most windows stuff
	h2xml_cmds = LibGenerator.h2xml_cmds
	h2xml_cmds[0][:0] = '-D WIN32_LEAN_AND_MEAN config-win.h'.split()

	def run(self):
		os.environ['PATH'] += ';%s\lib\opt' % get_mysql_root()
		super(Win32LibGenerator, self).run()

class UnixLibGenerator(LibGenerator):
	platform = 'unix'
	libname='libmysqlclient.so'
	mysql_include = '/usr/include/mysql'

def patch_mysql_api():
	"""
	Todo:
	1) Change my_bool = c_char to my_bool = c_int8
	2) Change mysql_autocommit arg2 from c_char to my_bool
	3) Patch to support robust library location
	"""
	print patch_mysql_api.__doc__

vars()[get_platform_name().capitalize()+'LibGenerator']().run()

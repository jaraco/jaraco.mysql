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
import copy
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
		'mysql.xml -l %(libname)s -o %(libroot)s/api.py'.split(),
		# Use -s MYSQL to get the MYSQL structure and ancestral structures
		'errmsg.xml -o %(libroot)s/errmsg.py'.split(),
		'mysql_version.xml -o %(libroot)s/version.py'.split(),
		'mysqld_error.xml -o %(libroot)s/errors.py'.split(),
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
		xml2py_cmds = map(self.patch_cmd, self.xml2py_cmds)
		cmds = merge_args(xml2py_common, xml2py_cmds)
		self.create_package()
		map(self.xml2py_cmd, cmds)
		
		self.patch_mysql_api()

	def patch_cmd(self, cmd):
		class ObjectDict(object):
			def __init__(self, object):
				self.object = object
			def __getitem__(self, name):
				return getattr(self.object, name)

		patch_part = lambda part: part % ObjectDict(self)
		return map(patch_part, cmd)

	@property
	def libroot(self):
		return 'root/_mysql_' + self.platform

	def create_package(self):
		if not os.path.exists(self.libroot):
			os.makedirs(self.libroot)
		open(os.path.join(self.libroot, '__init__.py')).close()

	def fix_my_bool(self):
		self.api_file = self.api_file.replace('my_bool = c_char\n', 'my_bool = c_int8\n')

	def fix_lib_path(self):
		pass

	def patch_mysql_api(self):
		"""
		Todo:
		1) Change mysql_autocommit arg2 from c_char to my_bool (may not be necessary under unix)
		"""
		self.api_file = open(os.path.join(self.libroot, 'api.py'), 'r').read()
		self.fix_my_bool()
		self.fix_lib_path()
		open(os.path.join(self.libroot, 'api.py',), 'w').write(self.api_file)
		print self.patch_mysql_api.__doc__


class WindowsLibGenerator(LibGenerator):
	platform = 'windows'
	libname='libmysql.dll'
	mysql_include = os.path.join(get_mysql_root(), 'include')
	# need WIN32_LEAN_AND_MEAN to exclude most windows stuff
	h2xml_cmds = copy.deepcopy(LibGenerator.h2xml_cmds)
	h2xml_cmds[0][:0] = '-D WIN32_LEAN_AND_MEAN config-win.h'.split()

	def run(self):
		os.environ['PATH'] += ';%s\lib\opt' % get_mysql_root()
		super(WindowsLibGenerator, self).run()

	def fix_lib_path(self):
		f = self.api_file
		f = f.replace("CDLL('libmysql.dll')", "CDLL(get_lib_path())")
		f = f.replace("WinDLL('libmysql.dll')", "WinDLL(get_lib_path())")
		i = f.index('_libraries = {}')
		before, after = f[:i], f[i:]
		new_code = 'from _mysql_api_util import get_lib_path\n'
		self.api_file = ''.join((before, new_code, after))


class UnixLibGenerator(LibGenerator):
	platform = 'unix'
	libname='libmysqlclient.so'
	mysql_include = '/usr/include/mysql'

vars()[get_platform_name().capitalize()+'LibGenerator']().run()

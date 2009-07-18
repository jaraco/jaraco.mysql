
"""
Support functions
"""

import sys
import os
from itertools import count

# try to import winreg.  It's needed for win32
try:
	try:
		import winreg
	except ImportError:
		import _winreg as winreg
except ImportError:
	pass

platform_map = dict(
	linux2 = 'unix',
	darwin = 'unix',
	win32 = 'windows',
)

def get_platform_name():
	return platform_map.get(sys.platform, sys.platform)

def registry_key_subkeys(key):
	def enumerated_subkeys(key):
		for index in count():
			try:
				yield winreg.EnumKey(key, index)
			except WindowsError:
				break
	return list(enumerated_subkeys(key))

def get_mysql_root_windows():
	mySQLKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\MySQL AB")
	installedVersions = registry_key_subkeys(mySQLKey)
	latestServerKeyName = sorted(installedVersions)[-1]
	serverKeyName = latestServerKeyName # todo, allow selection by version
	serverKey = winreg.OpenKey(mySQLKey, serverKeyName)
	mysql_root, dummy = winreg.QueryValueEx(serverKey,'Location')
	return mysql_root

def get_mysql_root_unix():
	return os.path.devnull

get_mysql_root = globals()['get_mysql_root_' + get_platform_name()]

def get_lib_path_windows():
	"Return the path to the MySQL DLL"
	return os.path.join(get_mysql_root(), 'bin', 'libmysql.dll')

def get_lib_path_unix():
	"Return the path to the MySQL library"
	return os.path.join(get_mysql_root(), 'libmysqlclient.so.15')

def get_lib_path():
	lib_path = globals()['get_lib_path_' + get_platform_name()]()
	assert os.path.exists(lib_path), "Could not locate MySQL library, install MySQL or set the environment variable MYSQL_LIB to the path to MySQL"
	return lib_path

def setup_platform_namespace(space):
	"""
	This function performs the equivalent of the following:
	
	import _mysql_api
	import _mysql_version
	import _mysql_errmsg
	import _mysql_errors
	
	but uses a platform-specific sub-module and imports the
	modules into the provided space.
	"""
	plat = get_platform_name()
	for mod_name in ('api', 'version', 'errmsg', 'errors'):
		mod = __import__('_mysql_%(plat)s.%(mod_name)s' % vars, space)
		mod_name = '_mysql_%s' % mod_name
		space[mod_name] = mod

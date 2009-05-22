
"""
Support functions
"""

import sys
import os
from itertools import count

# try to import winreg.  It's needed for win32
try:
	import _winreg
except ImportError:
	pass

def registry_key_subkeys(key):
	def enumerated_subkeys(key):
		for index in count():
			try:
				yield _winreg.EnumKey(key, index)
			except WindowsError:
				break
	return list(enumerated_subkeys(key))

def get_mysql_root_win32():
	mySQLKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\MySQL AB")
	installedVersions = registry_key_subkeys(mySQLKey)
	latestServerKeyName = sorted(installedVersions)[-1]
	serverKeyName = latestServerKeyName # todo, allow selection by version
	serverKey = _winreg.OpenKey(mySQLKey, serverKeyName)
	mysql_root, dummy = _winreg.QueryValueEx(serverKey,'Location')
	return mysql_root

def get_mysql_root_posix():
	raise NotImplementedError

get_mysql_root = globals()['get_mysql_root_' + sys.platform]

def get_lib_path_win32():
	"Return the path to the MySQL DLL"
	return os.path.join(get_mysql_root(), 'bin', 'libmysql.dll')

def get_lib_path_posix():
	"Todo, is this correct?"
	return os.path.join(get_mysql_root(), 'libmysql.so.15')

def get_lib_path():
	lib_path = globals()['get_lib_path_' + sys.platform]()
	assert os.path.exists(lib_path), "Could not locate MySQL library, install MySQL or set the environment variable MYSQL_LIB to the path to MySQL"
	return lib_path
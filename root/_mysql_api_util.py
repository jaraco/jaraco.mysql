
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

def __find_mysql_registered_installs():
	"""
	Find the mysql installs by inspecting the registry.
	
	When installing MySQL x64 on 64-bit Windows, MySQL doesn't
	store the registry information in the right place. See
	http://bugs.mysql.com/bug.php?id=42423 for details.
	This function works around that limitation, but gives priority
	to installs in the correct location.
	"""
	keys = [
		(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\MySQL AB'),
		(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\MySQL AB'),
		]
	for key in keys:
		try:
			key = winreg.OpenKey(*key)
		except WindowsError:
			continue
		for instance_name in registry_key_subkeys(key):
			# skip other MySQL products such as MySQL Workbench
			if not instance_name.startswith('MySQL Server'): continue
			instance_key = winreg.OpenKey(key, instance_name)
			mysql_root, dummy = winreg.QueryValueEx(instance_key, 'Location')
			yield instance_name, mysql_root

def get_mysql_root_windows():
	installs = __find_mysql_registered_installs()
	latest_install = next(iter(sorted(installs, reverse=True)))
	version, root = latest_install
	return root

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
		mod = __import__('_mysql_%(plat)s.%(mod_name)s' % vars(), space)
		target_mod_name = '_mysql_%s' % mod_name
		space[target_mod_name] = getattr(mod, mod_name)

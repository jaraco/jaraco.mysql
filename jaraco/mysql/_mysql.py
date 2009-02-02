
import operator
import ctypes
from jaraco.mysql import _mysql_api

server_init_done = False


def server_init(args=None, groups=None):
	"""
	Initialize embedded server. If this client is not linked against
	the embedded server library, this function does nothing.
	
	args -- sequence of command-line arguments
	groups -- sequence of groups to use in defaults files
	"""
	
	global server_init_done
	
	if server_init_done:
		raise ProgrammingError('already initialized')
	
	args_count = 0
	if args is not None:
		if not operator.isSequenceType(args):
			raise TypeError('args must be a sequence')
		
		try:
			args_count = len(args)
		except Exception:
			raise TypeError('args could not be sized')
		
		for arg in args:
			if not isinstance(arg, basestring):
				raise TypeError('args must contain strings')
		
		args_array = (ctypes.c_char_p * args_count)(*args)
		
		
	if groups is not None:
		if not operator.isSequenceType(groups):
			raise TypeError('groups must be a sequence')
		
		try:
			len(groups)
		except Exception:
			raise TypeError('groups could not be sized')
		
		for group in groups:
			if not isinstance(group, basestring):
				raise TypeError('groups must contain strings')
		
		# create a null-terminated list (one longer than we need)
		groups_array = (ctypes.c_char_p * (len(groups)+1))(*groups)
	
	res = _mysql_api.mysql_server_init(args_count, args_array, groups)
	if res:
		raise Exception(None)
	
	server_init_done = True

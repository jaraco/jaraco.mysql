
import operator
import ctypes
from jaraco.mysql import _mysql_api

server_init_done = False

def Exception(conn):
	global server_init_done
	if not server_init_done:
		raise InternalError(-1, 'server not initialized')
	
	#TODO: more to implement

def check_server_init(x):
	global server_init_done
	if not server_init_done:
		if(_mysql_api.mysql_server_init(0, None, None)):
			Exception(None)
			return x
	else:
		server_init_done = True

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
		return Exception(None)
	
	server_init_done = True

def server_end():
	"""
	Shut down embedded server. If not using an embedded server, this
	does nothing.
	"""
	global server_init_done
	if not server_init_done:
		return Exception(None)
		
	_mysql_api.mysql_server_end()
	server_init_done = False

def thread_safe():
	"Indicates whether the client is compiled as thread-safe."
	check_server_init(None)
	_mysql_api.mysql_thread_safe()

class result(object):
	"""
	result(connection, use=0, converter={})
	
	Creating instances of this class directly is an excellent way to
	shoot yourself in the foot. If using _mysql.connection directly,
	use connection.store_result() or connection.use_result() instead.
	If using MySQLdb.Connection, this is done by the cursor class.
	Just forget your ever saw this. Forget... FOR-GET...
	"""

	__slots__ = ('conn', 'use', 'result', 'converter')

	def __init__(self, connection, use=0, converter=None):
		if converter is None: converter = dict()
		self.conn = connection
		self.use = use
		method = [_mysql_api.mysql_store_result, _mysql_api.mysql_use_result][bool(use)]
		self.result = method(ctypes.byref(conn.connection))
		if not self.result:
			self.converter = ()
			return
		
		fields = tuple(self._get_fields())
		self.nfields = len(fields)
		for field in fields:
			tmp = field.type
			fun = converter.get(tmp)
			if operator.isSequenceType(fun):
				fun2 = None
				for t in fun:
					if not t: continue
					if not isinstance(t, tuple): continue
					if len(t) == 2:
						mask, fun2 = t
						if not isinstance(mask, int):
							break
						if mask & field.flags:
							break
						else:
							continue
				fun = fun2
			self.converter += (fun,)
	
	def __delattr__(self, name):
		raise AttributeError("can't delete %s attributes" % self.__class__.__name)
	
	def describe(self):
		"""
		Returns the sequence of 7-tuples required by the DB-API for
		the Cursor.description attribute.
		"""
		def get_field_description(field):
			return (
				field.name,
				field.type,
				field.max_length,
				field.length,
				field.length,
				field.decimals,
				field.flags is not None,
				)
		self.check_result_connection()
		return (get_field_description(field) for field in self._get_fields())
	
	def _get_fields(self):
		n = _mysql_api.mysql_num_fields(self.result)
		fields = _mysql_api.mysql_fetch_fields(self.result)
		for i in range(n):
			yield(fields[i])
	
	def field_flags(self):
		"Returns a tuple of field flags, one for each column in the result."
		self.check_result_connection()
		return (field.flags for field in self._get_fields())
	
	def _check_result_connection(self):
		pass #stubbed
	
	@staticmethod
	def _field_to_python(converter, rowitem, length):
		default_converter = lambda item, length: item[:length]
		converter = converter or default_converter
		
		if rowitem:
			return converter(rowitem, length)


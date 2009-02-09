#!/usr/bin/env python

"""
an adaptation of the MySQL C API (mostly)

You probably are better off using MySQLdb instead of using this
module directly.

In general, renaming goes from mysql_* to _mysql.*. _mysql.connect()
returns a connection object (MYSQL). Functions which expect MYSQL * as
an argument are now methods of the connection object. A number of things
return result objects (MYSQL_RES). Functions which expect MYSQL_RES * as
an argument are now methods of the result object. Deprecated functions
(as of 3.23) are NOT implemented.
"""

import operator
import ctypes
from jaraco.mysql import _mysql_api


server_init_done = False

def do_exception(conn):
	global server_init_done
	if not server_init_done:
		raise InternalError(-1, 'server not initialized')
	
	raise NotImplementedError()
	#TODO: more to implement

def check_server_init(x):
	global server_init_done
	if not server_init_done:
		if(_mysql_api.mysql_server_init(0, None, None)):
			do_exception(None)
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
		return do_exception(None)
	
	server_init_done = True

def server_end():
	"""
	Shut down embedded server. If not using an embedded server, this
	does nothing.
	"""
	global server_init_done
	if not server_init_done:
		return do_exception(None)
		
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

	# todo: make check_result_connection a decorator on the appropriate methods

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

	def row_to_tuple(self, row):
		"""
		@param row
		@type MYSQL_ROW
		"""
		lengths = _mysql_api.mysql_fetch_lengths(self.result)
		
		values = (
			self._field_to_python(conv_i, row_i, length)
			for conv_i, row_i, length in map(None, self.converter, row, lengths)
			)
		return tuple(values)

	def row_to_dict(self, row):
		lengths = _mysql_api.mysql_fetch_lengths(self.result)
		fields = _mysql_api.mysql_fetch_fields(self.result)
		unique_field_names = self._get_unique_field_names(fields)
		r = dict()
		for conv_i, row_i, length, field in map(None, self.converter, row, lengths, fields):
			v = self._field_to_python(conv_i, row_i, length)
			if field.name not in r:
				field_name = field.name
			else:
				field_name = '%s.%s' % (field.table, field.name)
				field_name = field_name[:256]
			r[field_name] = v
	
	def row_to_dict_old(self, row):
		raise NotImplementedError
		
	
	def _fetch_row(self, skiprows, maxrows, convert_row):
		# API variance - this function is similar to _mysql__fetch_row, but
		#  returns a sequence of rows, not the number.
		
		for i in range(skiprows, skiprows+maxrows+1):
			row = _mysql_api.mysql_fetch_row(self.result)
			if not row and _mysql_api.mysql_errno(self.conn.connection):
				_do_exception(self.conn)
			if not row:
				break
			v = self.convert_row(row)
			yield v
	
	def fetch_row(self, maxrows=1, how=0):
		"""
		fetch_row([maxrows, how]) -- Fetches up to maxrows as a tuple.
		The rows are formatted according to how:
		
		0 -- tuples (default)
		1 -- dictionaries, key=column or table.column if duplicated
		2 -- dictionaries, key=table.column
		"""
		row_converters = (
			self.row_to_tuple,
			self.row_to_dict,
			self.row_to_dict_old,
			)
		skiprows=0
		
		self.check_result_connection()
		try:
			convert_row = row_converters[how]
		except IndexError:
			raise ValueError('how out of range')
		
		if max_rows:
			result = tuple(self._fetch_row(skiprows, maxrows, convert_row))
		else:
			if self.use:
				maxrows = 1000
				result = ()
				while True:
					iter_result = tuple(self._fetch_row(skiprows, maxrows, convert_row))
					rowsadded = len(iter_result)
					skiprows += rowsadded
					if rows_added < maxrows: break
					result = result + iter_result
			else:
				maxrows = _mysql_api.mysql_num_rows(self.result)
				result = tuple(self._fetch_row(skiprows, maxrows, convert_row))
		return result
	
	def num_fields(self):
		"Return the number of fields (column) in the result."
		self.check_result_connection()
		return int(_mysql_api.mysql_num_fields(self.result))
	
	def num_rows(self):
		"""
		Returns the number of rows in the result set. Note that if
		use=1, this will not return a valid value until the entire result
		set has been read.
		"""
		self.check_result_connection()
		return int(_mysql_api.mysql_num_rows(self.result))
	
	def data_seek(self, row):
		"data_seek(n) -- seek to row n of result set"
		self.check_result_connection()
		_mysql_api.mysql_data_seek(self.result, row)
	
	def row_seek(self, offset):
		"row_seek(n) -- seek offset n rows of result set"
		self.check_result_connection()
		if self.use:
			raise ProgrammingError('cannot be used with connection.use_result()')
		r = _mysql_api.mysql_row_tell(self.result)
		_mysql_api.mysql_row_seek(self.result, r+offset)
	
	def row_tell(self):
		"row_tell() -- return the current row number of the result set."
		self.check_result_connection()
		if self.use:
			raise ProgrammingError('cannot be used with connection.use_result()')
		r = _mysql_api.mysql_row_tell(self.result)
		return int(r-self.result.data.data)
	
	def __del__(self):
		_mysql_api.mysql_free_result(self.result)
	

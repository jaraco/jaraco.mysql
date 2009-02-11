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
	
class connection(object):
	"""
	Returns a MYSQL connection object. Exclusive use of
	keyword parameters strongly recommended. Consult the
	MySQL C API documentation for more details.
	
	host
	  string, host to connect
	
	user
	  string, user to connect as
	
	passwd
	  string, password to use
	
	db
	  string, database to use
	
	port
	  integer, TCP/IP port to connect to
	
	unix_socket
	  string, location of unix_socket (UNIX-ish only)
	
	conv
	  mapping, maps MySQL FIELD_TYPE.* to Python functions which
	  convert a string to the appropriate Python type
	
	connect_timeout
	  number of seconds to wait before the connection
	  attempt fails.
	
	compress
	  if set, gzip compression is enabled
	
	named_pipe
	  if set, connect to server via named pipe (Windows only)
	
	init_command
	  command which is run once the connection is created
	
	read_default_file
	  see the MySQL documentation for mysql_options()
	
	read_default_group
	  see the MySQL documentation for mysql_options()
	
	client_flag
	  client flags from MySQLdb.constants.CLIENT
	
	load_infile
	  int, non-zero enables LOAD LOCAL INFILE, zero disables
	"""
	__slots__ = ('connection', 'open', 'converter')
	
	def __init__(self,
		host=None, user=None, passwd=None, db=None,
		unix_socket = None, conv=None, connect_timeout=0,
		compress = -1, named_pipe=-1, init_command=None,
		read_default_file=None, read_default_group=None,
		client_flag = 0, ssl=None, local_infile=-1):
		self.open = False
		check_server_init(-1)
		if conv is None: conv = dict()
		self.converter = conv
		
		conn = _mysql_api.mysql_init(self.connection)
		if connect_timeout:
			timeout = ctypes.c_uint(connect_timeout)
			_mysql_api.mysql_options(self.connection, _mysql_api.MYSQL_OPT_CONNECT_TIMEOUT, ctypes.byref(timeout))
		
		if compress != -1:
			_mysql_api.mysql_options(self.connection, _mysql_api.MYSQL_OPT_COMPRESS, 0)
			client_flag |= _mysql_api.CLIENT_COMPRESS
			
		if named_pipe != -1:
			_mysql_api.mysql_options(self.connection, _mysql_api.MYSQL_OPT_NAMED_PIPE, 0)
		
		if init_command is not None:
			_mysql_api.mysql_options(self.connection, _mysql_api.MYSQL_INIT_COMMAND, init_command)
		
		if read_default_file is not None:
			_mysql_api.mysql_options(self.connection, _mysql_api.MYSQL_READ_DEFAULT_FILE, read_default_file)

		if read_default_group is not None:
			_mysql_api.mysql_options(self.connection, _mysql_api.MYSQL_READ_DEFAULT_GROUP, read_default_group)
	
		if local_infile is not None:
			_mysql_api.mysql_options(self.connection, _mysql_api.MYSQL_OPT_LOCAL_INFILE, local_infile)
			
		if ssl:
			ssl_args = (ssl.get(key) for key in ('key', 'cert', 'ca', 'capath', 'cipher'))
			_mysql_api.mysql_ssl_set(self.connection, *ssl_args)
			
		conn = _mysql_api.mysql_real_connect(self.connection, 
			host, user, passwd, db,
			port, unix_socket, client_flag)
		
		if not conn:
			do_exception(self)
			
		self.open = True

	def close(self):
		"Close the connection No further activity possible."
		if not self.open:
			raise ProgrammingError("closing a closed connection")
		_mysql_api.mysql_close(self.connection)
		self.open = False

	def _check_connection(self):
		pass
		#stubbed

	def affected_rows(self):
		"""
		Return number of rows affected by the last query.
		Non-standard. Use Cursor.rowcount.
		"""
		self._check_connection()
		return long(_mysql_api.mysql_affected_rows(self.connection))
	
	def debug(self, debug):
		"""
		Does a DBUG_PUSH with the given string.
		mysql_debug() uses the Fred Fish debug library.
		To use this function, you must use a debug build
		of the client library..
		"""
		_mysql_api.mysql_debug(debug)

	def dump_debug_info(self):
		"""
		Instructs the server to write some debug information to the
		log. The connected user must have the process privilege for
		this to work. Non-standard.
		"""
		self._check_connection()
		err = _mysql_api.mysql_dump_debug_info(self.connection)
		if err:
			do_exception(self)
		
	def autocommit(self, flag):
		"Set the autocommit mode. True values enable; False value disable."
		# todo, mysql version < 4.01
		# err = _mysql_api.mysql_query(self.connection, "SET AUTOCOMMIT=%d" % flag)
		err = _mysql_api.mysql_autocommit(self.connection, flag)
		if err:
			do_exception(self)
	
	def commit(self):
		"Commits the current transaction"
		# todo: mysql version < 4.01
		err = _mysql_api.mysql_commit(self.connection)
		if err:
			do_exception(self)
		
	def rollback(self):
		"Rolls backs the current transaction"
		err = _mysql_api.mysql_rollback(self.connection)
		if err:
			do_exception(self)
	
	def next_result(self):
		"""
		If more query results exist, next_result() reads the next query
		results and returns the status back to application.
		
		After calling next_result() the state of the connection is as if
		you had called query() for the next query. This means that you can
		now call store_result(), warning_count(), affected_rows()
		, and so forth. 
		
		Returns 0 if there are more results; -1 if there are no more results
		
		Non-standard.
		"""
		err = _mysql_api.mysql_next_result(self.connection)
		if err > 0:
			do_exception(self)
		return 0

	def sqlstate(self):
		"""
		Returns a string containing the SQLSTATE error code
		for the last error. The error code consists of five characters.
		'00000' means \"no error.\" The values are specified by ANSI SQL
		and ODBC. For a list of possible values, see section 23
		Error Handling in MySQL in the MySQL Manual.
		
		Note that not all MySQL errors are yet mapped to SQLSTATE's.
		The value 'HY000' (general error) is used for unmapped errors.
		
		Non-standard.
		"""
		return str(mysql_api.mysql_sqlstate(self.connection))

	def warning_count(self):
		"""
		Returns the number of warnings generated during execution
		of the previous SQL statement.
		
		Non-standard.
		"""
		return int(_mysql_api.mysql_warning_count(self.connection))

	def error(self):
		"""
		Returns the error message for the most recently invoked API function
		that can succeed or fail. An empty string ("") is returned if no error
		occurred.
		"""
		return str(_mysql_api.mysql_error(self.connection))
	
	@staticmethod
	def _escape_string(conn, s):
		size = len(s)
		out = ctypes.create_string_buffer(size*2+1)
		check_server_init()
		args = (out, s, size)
		if conn and conn.open:
			result_len = _mysql_api.mysql_real_escape_string(conn.connection, *args)
		else:
			result_len = _mysql_api.mysql_escape_string(*args)
		return out[:result_len]
	
	def escape_string(self, s):
		"""
		escape_string(s)
		"""
		return connection._escape_string(self, s)

	@staticmethod
	def _string_literal(conn, o, d=None):
		s = str(o)
		size = len(s)
		out = ctypes.create_string_buffer(size*2+3)
		check_server_init()
		args = (out+1, s, size)
		if conn and conn.open:
			result_len = _mysql_api.mysql_real_escape_string(conn, *args)
		else:
			result_len = _mysql_api.mysql_escape_string(*args)
		out[0] = out[result_len+1] = "'"
		return out[:result_len+2]

	def string_literal(self, o, d=None):
		return connection._string_literal(self, o, d)
	
	def escape(self, obj):
		return escape(obj, self.converter)

	def change_user(self, user, passwd=None, db=None):
		"""
		Changes the user and causes the database specified by db to
		become the default (current) database on the connection
		specified by mysql. In subsequent queries, this database is
		the default for table references that do not include an
		explicit database specifier.
		
		This function was introduced in MySQL Version 3.23.3.
		
		Fails unless the connected user can be authenticated or if he
		doesn't have permission to use the database. In this case the
		user and database are not changed.
		
		The db parameter may be set to None if you don't want to have
		a default database.
		"""
		self.check_connection()
		r = _mysql_api.mysql_change_user(self.connection, user, passwd, db)
		if r:
			do_exception(self)
	
	def character_set_name(self):
		"""
		Returns the default character set for the current connection.\n\
		Non-standard.
		"""
		self.check_connection()
		return str(_mysql_api.mysql_character_set_name(self.connection))
	
	def set_character_set(self, name):
		"""
		Sets the default character set for the current connection.\n\
		Non-standard.
		"""
		self.check_connection()
		err = _mysql_api.mysql_set_character_set(self.connection, name)
		if err:
			do_exception(self)

def escape_string(s):
	"""
	escape_string(s) -- quote any SQL-interpreted characters in string s.
	
	Use connection.escape_string(s), if you use it at all.
	_mysql.escape_string(s) cannot handle character sets. You are
	probably better off using connection.escape(o) instead, since
	it will escape entire sequences as well as strings.
	"""
	return connection._escape_string(None, s)

def string_literal(s):
	"""
	string_literal(obj) -- converts object obj into a SQL string literal.
	This means, any special SQL characters are escaped, and it is enclosed
	within single quotes. In other words, it performs:
	
	\"'%s'\" % escape_string(str(obj))
	
	Use connection.string_literal(obj), if you use it at all.
	_mysql.string_literal(obj) cannot handle character sets.
	"""
	return connection._string_literal(None, s)

def __escape_item(item, d):
	itemtype = type(item)
	try:
		itemconv = d.get(itemtype) or d[str]
	except KeyError:
		raise TypeError('no default type converter defined')
	quoted = itemconv(item, d)
	return quoted

def escape(obj, conv=None):
	"""
	escape(obj, conv) -- escape any special characters in object obj
	using mapping conv to provide quoting functions for each type.
	Returns a SQL literal string.
	"""
	if not isinstance(conv, dict):
		raise TypeError("argument 2 must be a mapping")
	return __escape_item(obj, conv)

def escape_sequence(seq, conv):
	"""
	escape_sequence(seq, conv) -- escape any special characters in sequence
	seq using mapping conv to provide quoting functions for each type.
	Returns a tuple of escaped items.
	"""
	if not isinstance(conv, dict):
		raise TypeError("argument 2 must be a mapping")
	return tuple((__escape_item(item, conv) for item in seq))

def escape_dict(d, conv):
	"""
	escape_dict(d, conv) -- escape any special characters in
	dictionary d using mapping conv to provide quoting functions for each type.
	Returns a dictionary of escaped items.
	"""
	if not isinstance(d, dict):
		raise TypeError("argument 1 must be a mapping")
	if not isinstance(conv, dict):
		raise TypeError("argument 2 must be a mapping")
	items = ((key, __escape_item(value, conv)) for key, value in d.items())
	return dict(items)


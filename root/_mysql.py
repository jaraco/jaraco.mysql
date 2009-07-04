#!/usr/bin/env python

"""
an adaptation of _mysql.c from mysql-python (mostly)

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
import re
import itertools

# the following 4 lines are a quick hack to use the .dll in 
#  the same directory as this file
import os
dirname = os.path.dirname(__file__)
os.environ['PATH'] = ';'.join((os.environ['PATH'], dirname))
os.environ['PATH'] = ';'.join((os.environ['PATH'], r'c:\Program Files\MySQL\MySQL Server 5.1\bin'))
#print os.environ['PATH']

import _mysql_api
import _mysql_version
import _mysql_errmsg
import _mysql_errors
from _mysql_exceptions import *

__version__ = '1.2.3'
version_info = (1,2,3,'gamma',1)

server_init_done = False

def _build_error_exception_map():
	"""Build a mapping between error codes and exceptions
	to be thrown."""
	global _error_exceptions
	exceptions = (
		ProgrammingError,
		DataError,
		IntegrityError,
		NotSupportedError,
		)

	
	error_groups = (
	"""
	case CR_COMMANDS_OUT_OF_SYNC:
	case ER_DB_CREATE_EXISTS:
	case ER_SYNTAX_ERROR:
	case ER_PARSE_ERROR:
	case ER_NO_SUCH_TABLE:
	case ER_WRONG_DB_NAME:
	case ER_WRONG_TABLE_NAME:
	case ER_FIELD_SPECIFIED_TWICE:
	case ER_INVALID_GROUP_FUNC_USE:
	case ER_UNSUPPORTED_EXTENSION:
	case ER_TABLE_MUST_HAVE_COLUMNS:
#ifdef ER_CANT_DO_THIS_DURING_AN_TRANSACTION
	case ER_CANT_DO_THIS_DURING_AN_TRANSACTION:
#endif
	""",
	"""
#ifdef WARN_DATA_TRUNCATED
	case WARN_DATA_TRUNCATED:
#ifdef WARN_NULL_TO_NOTNULL
	case WARN_NULL_TO_NOTNULL:
#endif
#ifdef ER_WARN_DATA_OUT_OF_RANGE
	case ER_WARN_DATA_OUT_OF_RANGE:
#endif
#ifdef ER_NO_DEFAULT
	case ER_NO_DEFAULT:
#endif
#ifdef ER_PRIMARY_CANT_HAVE_NULL
	case ER_PRIMARY_CANT_HAVE_NULL:
#endif
#ifdef ER_DATA_TOO_LONG
	case ER_DATA_TOO_LONG:
#endif
#ifdef ER_DATETIME_FUNCTION_OVERFLOW
	case ER_DATETIME_FUNCTION_OVERFLOW:
#endif
	""",
	"""
#endif
	case ER_DUP_ENTRY:
#ifdef ER_DUP_UNIQUE
	case ER_DUP_UNIQUE:
#endif
#ifdef ER_NO_REFERENCED_ROW
	case ER_NO_REFERENCED_ROW:
#endif
#ifdef ER_NO_REFERENCED_ROW_2
	case ER_NO_REFERENCED_ROW_2:
#endif
#ifdef ER_ROW_IS_REFERENCED
	case ER_ROW_IS_REFERENCED:
#endif
#ifdef ER_ROW_IS_REFERENCED_2
	case ER_ROW_IS_REFERENCED_2:
#endif
#ifdef ER_CANNOT_ADD_FOREIGN
	case ER_CANNOT_ADD_FOREIGN:
#endif
	""",
	"""
	case ER_WARNING_NOT_COMPLETE_ROLLBACK:
	case ER_NOT_SUPPORTED_YET:
	case ER_FEATURE_DISABLED:
	case ER_UNKNOWN_STORAGE_ENGINE:
	""",
	)
	def parse(group):
		pattern = re.compile('case (.*):')
		err_ids = pattern.findall(group)
		values = [getattr(_mysql_errors, err_id) for err_id in err_ids if hasattr(_mysql_errors, err_id)]
		assert values, "No values parsed"
		assert None not in values
		return values
	parsed_error_groups = map(parse, error_groups)
	# parsed_error_groups now contains the error values from
	#  _mysql_api congruent to the list of exceptions
	_error_exceptions = {}
	for exception, err_group in zip(exceptions, parsed_error_groups):
		for err_val in err_group:
			_error_exceptions[err_val] = exception
	_error_exceptions[0] = InternalError

def do_exception(conn):
	global server_init_done
	if not '_error_exceptions' in globals(): _build_error_exception_map()
	if not server_init_done:
		raise InternalError(-1, 'server not initialized')
	
	merr = _mysql_api.mysql_errno(conn.connection)
	if merr > _mysql_errmsg.CR_MAX_ERROR:
		raise InterfaceError(-1, "error totally whack")
	else:
		default_exc = [OperationalError, InternalError][merr < 1000]
		exc = _error_exceptions.get(merr, default_exc)
	
	msg = _mysql_api.mysql_error(conn.connection)
	raise exc(merr, msg)

def check_server_init():
	global server_init_done
	if not server_init_done:
		if(_mysql_api.mysql_server_init(0, None, None)):
			do_exception(None)
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
	check_server_init()
	return _mysql_api.mysql_thread_safe()

def get_client_info():
	"""
	get_client_info() -- Returns a string that represents
	the client library version.
	"""
	check_server_init()
	return _mysql_api.mysql_get_client_info()

NULL = "NULL"

class result(object):
	"""
	result(connection, use=0, converter={})
	
	Creating instances of this class directly is an excellent way to
	shoot yourself in the foot. If using _mysql.connection directly,
	use connection.store_result() or connection.use_result() instead.
	If using MySQLdb.Connection, this is done by the cursor class.
	Just forget your ever saw this. Forget... FOR-GET...
	"""

	# todo: make check_connection a decorator on the appropriate methods

	__slots__ = ('conn', 'use', 'result', 'converter', 'nfields')

	def __init__(self, connection, use=0, converter=None):
		if converter is None: converter = dict()
		self.conn = connection
		self.use = use
		method = [_mysql_api.mysql_store_result, _mysql_api.mysql_use_result][bool(use)]
		self.result = method(self.conn.connection)
		self.converter = ()
		if not self.result:
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
		self._check_connection()
		return tuple(get_field_description(field) for field in self._get_fields())
	
	def _get_fields(self):
		n = _mysql_api.mysql_num_fields(self.result)
		fields = _mysql_api.mysql_fetch_fields(self.result)
		for i in range(n):
			yield(fields[i])
	
	def field_flags(self):
		"Returns a tuple of field flags, one for each column in the result."
		self._check_connection()
		return (field.flags for field in self._get_fields())
	
	def _check_connection(self):
		self.conn._check()
	
	@staticmethod
	def _byte_string_items(row, lengths, n_fields=None):
		r"""
		MySQL returns a **char for a row of data, but ctypes
		interprets this as list of strings and not a list of
		bytes.  This wrapper adapts the list of strings to a
		list of bytes.

		>>> row = (ctypes.c_char_p*3)('foo', '\000bar', 'baz')
		>>> _byte_string_items(row, [3,4], 2)
		['foo', '\x00bar']
		
		It should also preserve None
		>>> row = (ctypes.c_char_p*2)(None, 'foo')
		>>> _byte_string_items(row, [1,3])
		[None, 'foo']
		"""
		# first cast it to a pointer to void pointers
		row = ctypes.cast(row, ctypes.POINTER(ctypes.c_void_p))
		# limit the iterability of lengths to the number of fields
		lengths = itertools.islice(lengths, n_fields)

		def get_string_item(address, length):
			return ctypes.string_at(address, length) \
				if address is not None else None

		# then, use string_at to get the whole byte structure
		#  given the length
		return [
			get_string_item(address, length)
			for address, length in
			zip(row, lengths)
			]

	@staticmethod
	def _field_to_python(converter, rowitem):
		if rowitem is not None:
			if converter:
				rowitem = converter(rowitem)
		return rowitem
		
	def row_to_tuple(self, row):
		"""
		@param row
		@type MYSQL_ROW
		"""
		n_fields = _mysql_api.mysql_num_fields(self.result)
		lengths = _mysql_api.mysql_fetch_lengths(self.result)
		row = self._byte_string_items(row, lengths, n_fields)
		values = (
			self._field_to_python(conv_i, row_i)
			for conv_i, row_i
			in zip(self.converter, row)
			)
		return tuple(values)

	def row_to_dict(self, row):
		n_fields = _mysql_api.mysql_num_fields(self.result)
		lengths = _mysql_api.mysql_fetch_lengths(self.result)
		fields = _mysql_api.mysql_fetch_fields(self.result)
		unique_field_names = self._get_unique_field_names(fields)
		row = self._byte_string_items(row, lengths, n_fields)
		r = dict()
		field_specs = zip(range(n_fields), self.converter, row, lengths, fields)
		for n, conv_i, row_i, length, field in field_specs:
			v = self._field_to_python(conv_i, row_i, length)
			if field.name not in r:
				field_name = field.name
			else:
				field_name = '%s.%s' % (field.table, field.name)
				field_name = field_name[:256]
			r[field_name] = v
		return r
	
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
			v = convert_row(row)
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
		
		self._check_connection()
		try:
			convert_row = row_converters[how]
		except IndexError:
			raise ValueError('"how" out of range')

		if maxrows:
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
		self._check_connection()
		return int(_mysql_api.mysql_num_fields(self.result))
	
	def num_rows(self):
		"""
		Returns the number of rows in the result set. Note that if
		use=1, this will not return a valid value until the entire result
		set has been read.
		"""
		self._check_connection()
		return int(_mysql_api.mysql_num_rows(self.result))
	
	def data_seek(self, row):
		"data_seek(n) -- seek to row n of result set"
		self._check_connection()
		_mysql_api.mysql_data_seek(self.result, row)
	
	def row_seek(self, offset):
		"row_seek(n) -- seek offset n rows of result set"
		self._check_connection()
		if self.use:
			raise ProgrammingError('cannot be used with connection.use_result()')
		r = _mysql_api.mysql_row_tell(self.result)
		_mysql_api.mysql_row_seek(self.result, r+offset)
	
	def row_tell(self):
		"row_tell() -- return the current row number of the result set."
		self._check_connection()
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
		port=0,
		unix_socket = None, conv=None, connect_timeout=0,
		compress = -1, named_pipe=-1, init_command=None,
		read_default_file=None, read_default_group=None,
		client_flag = 0, ssl=None, local_infile=-1):
		self.open = False
		check_server_init()
		if conv is None: conv = dict()
		self.converter = conv
		self.connection = _mysql_api.MYSQL()
		
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
	
		if local_infile != -1:
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

	@property
	def server_capabilities(self):
		"Capabilities of server; consult MySQLdb.constants.CLIENT"
		return self.connection.server_capabilities

	def close(self):
		"Close the connection No further activity possible."
		if not self.open:
			raise ProgrammingError("closing a closed connection")
		_mysql_api.mysql_close(self.connection)
		self.open = False

	def _check(self):
		if not self.open:
			do_exception(self)

	def affected_rows(self):
		"""
		Return number of rows affected by the last query.
		Non-standard. Use Cursor.rowcount.
		"""
		self._check()
		return long(_mysql_api.mysql_affected_rows(self.connection))
	
	def dump_debug_info(self):
		"""
		Instructs the server to write some debug information to the
		log. The connected user must have the process privilege for
		this to work. Non-standard.
		"""
		self._check()
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
		return err

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
		# We want to pass in the buffer we just created, but reserve
		#  one character for ourselves.
		out_p = ctypes.cast(ctypes.byref(out, 1), ctypes.c_char_p)
		args = (out_p, s, size)
		if conn and conn.open:
			result_len = _mysql_api.mysql_real_escape_string(conn.connection, *args)
		else:
			result_len = _mysql_api.mysql_escape_string(*args)
		out[0] = out[result_len+1] = "'"
		return out[:result_len+2]

	def string_literal(self, o, d=None):
		return connection._string_literal(self, o, d)
	
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
		self._check()
		r = _mysql_api.mysql_change_user(self.connection, user, passwd, db)
		if r:
			do_exception(self)
	
	def character_set_name(self):
		"""
		Returns the default character set for the current connection.
		Non-standard.
		"""
		self._check()
		return str(_mysql_api.mysql_character_set_name(self.connection))
	
	def set_character_set(self, name):
		"""
		Sets the default character set for the current connection.
		Non-standard.
		"""
		self._check()
		err = _mysql_api.mysql_set_character_set(self.connection, name)
		if err:
			do_exception(self)

	def get_character_set_info(self):
		"""
		Returns a dict with information about the current character set:
		
		collation
			collation name
		name
			character set name
		comment
			comment or descriptive name
		dir
			character set directory
		mbminlen
			min. length for multibyte string
		mbmaxlen
			max. length for multibyte string
		
		Not all keys may be present, particularly dir.
		
		Non-standard.
		"""
		self._check()
		cs = _mysql_api.MY_CHARSET_INFO()
		_mysql_api.mysql_get_character_set_info(self.connection, cs)
		return dict(
			name = cs.csname,
			collation = cs.name,
			comment = cs.comment,
			dir = cs.dir,
			mbminlen = cs.mbminlen,
			mbmaxlen = cs.mbmaxlen,
			)

	def get_client_info(self):
		"""
		get_client_info() -- Returns a string that represents
		the client library version.
		"""
		self._check()
		return _mysql_api.mysql_get_client_info()
	
	def get_host_info(self):
		"""
		Returns a string that represents the MySQL client library
		version. Non-standard.
		"""
		self._check()
		return _mysql_api.mysql_get_host_info(self.connection)
	
	def get_proto_info(self):
		"""
		Returns an unsigned integer representing the protocol version
		used by the current connection. Non-standard.
		"""
		self._check()
		return _mysql_api.mysql_get_proto_info(self.connection)
		
	def get_server_info(self):
		"""
		Returns a string that represents the server version number.
		Non-standard.
		"""
		self._check()
		return _mysql_api.mysql_get_server_info(self.connection)
	
	def info(self):
		"""
		Retrieves a string providing information about the most
		recently executed query. Non-standard. Use messages or
		Cursor.messages.
		"""
		self._check()
		return _mysql_api.mysql_info(self.connection)
	
	def insert_id(self):
		"""
		Returns the ID generated for an AUTO_INCREMENT column by the previous
		query. Use this function after you have performed an INSERT query into a
		table that contains an AUTO_INCREMENT field.
		
		Note that this returns 0 if the previous query does not
		generate an AUTO_INCREMENT value. If you need to save the value for
		later, be sure to call this immediately after the query
		that generates the value.
		
		The ID is updated after INSERT and UPDATE statements that generate
		an AUTO_INCREMENT value or that set a column value to
		LAST_INSERT_ID(expr). See section 6.3.5.2 Miscellaneous Functions
		in the MySQL documentation.
		
		Also note that the value of the SQL LAST_INSERT_ID() function always
		contains the most recently generated AUTO_INCREMENT value, and is not
		reset between queries because the value of that function is maintained
		in the server.
		"""
		self._check()
		return _mysql_api.mysql_insert_id(self.connection)

	def kill(self, pid):
		"""
		Asks the server to kill the thread specified by pid.
		Non-standard.
		"""
		self._check()
		res = _mysql_api.mysql_kill(self.connection, pid)
		if res: do_exception(self)
	
	def field_count(self):
		"""
		Returns the number of columns for the most recent query on the
		connection. Non-standard. Will probably give you bogus results
		on most cursor classes. Use Cursor.rowcount.
		"""
		self._check()
		return _mysql_api.mysql_field_count(self.connection)
	
	def ping(self, reconnect=-1):
		"""
		Checks whether or not the connection to the server is
		working. If it has gone down, an automatic reconnection is
		attempted.
		
		This function can be used by clients that remain idle for a
		long while, to check whether or not the server has closed the
		connection and reconnect if necessary.
		
		New in 1.2.2: Accepts an optional reconnect parameter. If True,
		then the client will attempt reconnection. Note that this setting
		is persistent. By default, this is on in MySQL<5.0.3, and off
		thereafter.
		
		Non-standard. You should assume that ping() performs an
		implicit rollback; use only when starting a new transaction.
		You have been warned.
		"""
		self._check()
		if reconnect != -1:
			self.connection.reconnect = reconnect
		res = _mysql_api.mysql_ping(self.connection)
		if res: do_exception(self)

	def query(self, query):
		"""
		Execute a query. store_result() or use_result() will get the
		result set, if any. Non-standard. Use cursor() to create a cursor,
		then cursor.execute().
		"""
		self._check()
		res = _mysql_api.mysql_real_query(self.connection, query, len(query))
		if res: do_exception(self)

	def select_db(self, db):
		"""
		Causes the database specified by db to become the default
		(current) database on the connection specified by mysql. In subsequent
		queries, this database is the default for table references that do not
		include an explicit database specifier.
		
		Fails unless the connected user can be authenticated as having
		permission to use the database.
		
		Non-standard.
		"""
		self._check()
		res = _mysql_api.mysql_select_db(self.connection, db)
		if res: do_exception(self)
		
	def shutdown(self):
		"""
		Asks the database server to shut down. The connected user must
		have shutdown privileges. Non-standard.
		"""
		self._check()
		res = _mysql_api.mysql_shutdown(self.connection, _mysql_api.SHUTDOWN_DEFAULT)
		if res: do_exception(self)
	
	def stat(self):
		"""
		Returns a character string containing information similar to
		that provided by the mysqladmin status command. This includes
		uptime in seconds and the number of running threads,
		questions, reloads, and open tables. Non-standard.
		"""
		self._check()
		res = _mysql_api.mysql_stat(self.connection)
		if not res: do_exception(self)
		return res

	def store_result(self):
		"""
		Returns a result object acquired by mysql_store_result
		(results stored in the client). If no results are available,
		None is returned. Non-standard.
		"""
		self._check()
		res = result(self, 0, self.converter)
		if not res.result: res = None
		return res

	def thread_id(self):
		"""
		Returns the thread ID of the current connection. This value
		can be used as an argument to kill() to kill the thread.
		
		If the connection is lost and you reconnect with ping(), the
		thread ID will change. This means you should not get the
		thread ID and store it for later. You should get it when you
		need it.
		
		Non-standard.;
		"""
		self._check()
		return _mysql_api.mysql_thread_id(self.connection)

	def use_result(self):
		"""
		Returns a result object acquired by mysql_use_result
		(results stored in the server). If no results are available,
		None is returned. Non-standard.
		"""
		self._check()
		res = result(self, 1, self.converter)
		if not res.result: res = None
		return res

	def __del__(self):
		if self.open:
			self.close()

	def __repr__(self):
		if self.open:
			return "<%s open to '%.256s' at 0x%08X>" % (self.__class__.__name__, self.connection.host, id(self))
		else:
			return "<%s closed at 0x%08X>" % (self.__class__.__name__, id(self))

def connect(*args, **kwargs):
	return connection(*args, **kwargs)

connect.__doc__ = connection.__doc__

def debug(debug):
	"""
	Does a DBUG_PUSH with the given string.
	mysql_debug() uses the Fred Fish debug library.
	To use this function, you must use a debug version
	of the client library.
	"""
	return _mysql_api.mysql_debug(debug)

def escape_string(s):
	"""
	escape_string(s) -- quote any SQL-interpreted characters in string s.
	
	Use connection.escape_string(s), if you use it at all.
	_mysql.escape_string(s) cannot handle character sets. You are
	probably better off using connection.escape(o) instead, since
	it will escape entire sequences as well as strings.
	"""
	return connection._escape_string(None, s)

def string_literal(s, d=None):
	"""
	string_literal(obj) -- converts object obj into a SQL string literal.
	This means, any special SQL characters are escaped, and it is enclosed
	within single quotes. In other words, it performs:
	
	\"'%s'\" % escape_string(str(obj))
	
	Use connection.string_literal(obj), if you use it at all.
	_mysql.string_literal(obj) cannot handle character sets.
	"""
	return connection._string_literal(None, s, d)

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

connection.escape = staticmethod(escape)

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


from ctypes import *

STRING = c_char_p
_libraries = {}
_libraries['libmysqlclient.so'] = CDLL('libmysqlclient.so')


MYSQL_STMT_FETCH_DONE = 4
COM_TIME = 15
MYSQL_TYPE_LONG = 3
COM_SLEEP = 0
MYSQL_TIMESTAMP_DATETIME = 1
MYSQL_TYPE_BIT = 16
MYSQL_OPTION_MULTI_STATEMENTS_OFF = 1
MYSQL_RPL_ADMIN = 2
COM_PROCESS_INFO = 10
MYSQL_STATUS_USE_RESULT = 2
MYSQL_TYPE_BLOB = 252
COM_CHANGE_USER = 17
MYSQL_TYPE_DOUBLE = 5
COM_INIT_DB = 2
MYSQL_TIMESTAMP_NONE = -2
COM_TABLE_DUMP = 19
COM_REFRESH = 7
MYSQL_TYPE_TINY_BLOB = 249
MYSQL_TYPE_TIMESTAMP = 7
MYSQL_OPT_CONNECT_TIMEOUT = 0
COM_BINLOG_DUMP = 18
MYSQL_TYPE_NULL = 6
MYSQL_PROTOCOL_DEFAULT = 0
COM_DROP_DB = 6
COM_QUERY = 3
COM_DELAYED_INSERT = 16
MYSQL_OPT_COMPRESS = 1
MYSQL_TYPE_NEWDECIMAL = 246
MYSQL_PROTOCOL_TCP = 1
MYSQL_TYPE_FLOAT = 4
COM_FIELD_LIST = 4
MYSQL_STMT_INIT_DONE = 1
COM_CONNECT_OUT = 20
MYSQL_PROTOCOL_SOCKET = 2
MYSQL_REPORT_DATA_TRUNCATION = 19
MYSQL_SET_CHARSET_NAME = 7
STMT_ATTR_PREFETCH_ROWS = 2
COM_QUIT = 1
MYSQL_TYPE_NEWDATE = 14
MYSQL_STMT_PREPARE_DONE = 2
MYSQL_INIT_COMMAND = 3
COM_REGISTER_SLAVE = 21
MYSQL_TYPE_INT24 = 9
MYSQL_PROTOCOL_PIPE = 3
MYSQL_OPT_LOCAL_INFILE = 8
MYSQL_READ_DEFAULT_FILE = 4
MYSQL_STATUS_GET_RESULT = 1
COM_END = 29
MYSQL_STMT_EXECUTE_DONE = 3
MYSQL_TYPE_VAR_STRING = 253
MYSQL_TYPE_GEOMETRY = 255
COM_STMT_PREPARE = 22
MYSQL_TYPE_DATE = 10
MYSQL_PROTOCOL_MEMORY = 4
MYSQL_OPT_PROTOCOL = 9
MYSQL_READ_DEFAULT_GROUP = 5
COM_SET_OPTION = 27
MYSQL_OPT_NAMED_PIPE = 2
MYSQL_TIMESTAMP_ERROR = -1
MYSQL_RPL_MASTER = 0
MYSQL_TYPE_MEDIUM_BLOB = 250
MYSQL_TYPE_LONGLONG = 8
COM_STMT_RESET = 26
MYSQL_TIMESTAMP_TIME = 2
COM_STMT_EXECUTE = 23
MYSQL_TYPE_TIME = 11
MYSQL_SHARED_MEMORY_BASE_NAME = 10
MYSQL_OPT_RECONNECT = 20
MYSQL_SET_CHARSET_DIR = 6
MYSQL_TYPE_DATETIME = 12
COM_SHUTDOWN = 8
COM_STMT_SEND_LONG_DATA = 24
COM_CREATE_DB = 5
SHUTDOWN_DEFAULT = 0
STRING_RESULT = 0
CURSOR_TYPE_NO_CURSOR = 0
COM_STMT_CLOSE = 25
MYSQL_TYPE_YEAR = 13
MYSQL_OPT_WRITE_TIMEOUT = 12
STMT_ATTR_UPDATE_MAX_LENGTH = 0
REAL_RESULT = 1
MYSQL_STATUS_READY = 0
INT_RESULT = 2
SHUTDOWN_WAIT_TRANSACTIONS = 2
MYSQL_OPT_USE_RESULT = 13
MYSQL_TYPE_STRING = 254
CURSOR_TYPE_FOR_UPDATE = 2
SHUTDOWN_WAIT_CONNECTIONS = 1
MYSQL_TYPE_VARCHAR = 15
SHUTDOWN_WAIT_UPDATES = 8
MYSQL_OPT_USE_REMOTE_CONNECTION = 14
COM_CONNECT = 11
ROW_RESULT = 3
STMT_ATTR_CURSOR_TYPE = 1
COM_STATISTICS = 9
CURSOR_TYPE_SCROLLABLE = 4
MYSQL_TYPE_LONG_BLOB = 251
COM_STMT_FETCH = 28
SHUTDOWN_WAIT_ALL_BUFFERS = 16
MYSQL_OPT_USE_EMBEDDED_CONNECTION = 15
MYSQL_OPT_SSL_VERIFY_SERVER_CERT = 21
COM_PROCESS_KILL = 12
MYSQL_TYPE_DECIMAL = 0
MYSQL_OPT_READ_TIMEOUT = 11
DECIMAL_RESULT = 4
MYSQL_OPTION_MULTI_STATEMENTS_ON = 0
SHUTDOWN_WAIT_CRITICAL_BUFFERS = 17
MYSQL_OPT_GUESS_CONNECTION = 16
MYSQL_TYPE_TINY = 1
MYSQL_SECURE_AUTH = 18
COM_DEBUG = 13
MYSQL_TYPE_ENUM = 247
KILL_QUERY = 254
MYSQL_SET_CLIENT_IP = 17
COM_PING = 14
MYSQL_TYPE_SHORT = 2
MYSQL_TIMESTAMP_DATE = 0
MYSQL_RPL_SLAVE = 1
CURSOR_TYPE_READ_ONLY = 1
MYSQL_TYPE_SET = 248
KILL_CONNECTION = 255
pthread_t = c_ulong
class pthread_attr_t(Union):
    pass
pthread_attr_t._fields_ = [
    ('__size', c_char * 56),
    ('__align', c_long),
]
class __pthread_internal_list(Structure):
    pass
__pthread_internal_list._fields_ = [
    ('__prev', POINTER(__pthread_internal_list)),
    ('__next', POINTER(__pthread_internal_list)),
]
__pthread_list_t = __pthread_internal_list
class __pthread_mutex_s(Structure):
    pass
__pthread_mutex_s._fields_ = [
    ('__lock', c_int),
    ('__count', c_uint),
    ('__owner', c_int),
    ('__nusers', c_uint),
    ('__kind', c_int),
    ('__spins', c_int),
    ('__list', __pthread_list_t),
]
class pthread_mutex_t(Union):
    pass
pthread_mutex_t._fields_ = [
    ('__data', __pthread_mutex_s),
    ('__size', c_char * 40),
    ('__align', c_long),
]
class pthread_mutexattr_t(Union):
    pass
pthread_mutexattr_t._fields_ = [
    ('__size', c_char * 4),
    ('__align', c_int),
]
class N14pthread_cond_t3DOT_7E(Structure):
    pass
N14pthread_cond_t3DOT_7E._fields_ = [
    ('__lock', c_int),
    ('__futex', c_uint),
    ('__total_seq', c_ulonglong),
    ('__wakeup_seq', c_ulonglong),
    ('__woken_seq', c_ulonglong),
    ('__mutex', c_void_p),
    ('__nwaiters', c_uint),
    ('__broadcast_seq', c_uint),
]
class pthread_cond_t(Union):
    pass
pthread_cond_t._fields_ = [
    ('__data', N14pthread_cond_t3DOT_7E),
    ('__size', c_char * 48),
    ('__align', c_longlong),
]
class pthread_condattr_t(Union):
    pass
pthread_condattr_t._fields_ = [
    ('__size', c_char * 4),
    ('__align', c_int),
]
pthread_key_t = c_uint
pthread_once_t = c_int
class N16pthread_rwlock_t4DOT_10E(Structure):
    pass
N16pthread_rwlock_t4DOT_10E._fields_ = [
    ('__lock', c_int),
    ('__nr_readers', c_uint),
    ('__readers_wakeup', c_uint),
    ('__writer_wakeup', c_uint),
    ('__nr_readers_queued', c_uint),
    ('__nr_writers_queued', c_uint),
    ('__writer', c_int),
    ('__shared', c_int),
    ('__pad1', c_ulong),
    ('__pad2', c_ulong),
    ('__flags', c_uint),
]
class pthread_rwlock_t(Union):
    pass
pthread_rwlock_t._fields_ = [
    ('__data', N16pthread_rwlock_t4DOT_10E),
    ('__size', c_char * 56),
    ('__align', c_long),
]
class pthread_rwlockattr_t(Union):
    pass
pthread_rwlockattr_t._fields_ = [
    ('__size', c_char * 8),
    ('__align', c_long),
]
pthread_spinlock_t = c_int
class pthread_barrier_t(Union):
    pass
pthread_barrier_t._fields_ = [
    ('__size', c_char * 32),
    ('__align', c_long),
]
class pthread_barrierattr_t(Union):
    pass
pthread_barrierattr_t._fields_ = [
    ('__size', c_char * 4),
    ('__align', c_int),
]
__sig_atomic_t = c_int
class __sigset_t(Structure):
    pass
__sigset_t._fields_ = [
    ('__val', c_ulong * 16),
]
class timeval(Structure):
    pass
__time_t = c_long
__suseconds_t = c_long
timeval._fields_ = [
    ('tv_sec', __time_t),
    ('tv_usec', __suseconds_t),
]
__u_char = c_ubyte
__u_short = c_ushort
__u_int = c_uint
__u_long = c_ulong
__int8_t = c_byte
__uint8_t = c_ubyte
__int16_t = c_short
__uint16_t = c_ushort
__int32_t = c_int
__uint32_t = c_uint
__int64_t = c_long
__uint64_t = c_ulong
__quad_t = c_long
__u_quad_t = c_ulong
__dev_t = c_ulong
__uid_t = c_uint
__gid_t = c_uint
__ino_t = c_ulong
__ino64_t = c_ulong
__mode_t = c_uint
__nlink_t = c_ulong
__off_t = c_long
__off64_t = c_long
__pid_t = c_int
class __fsid_t(Structure):
    pass
__fsid_t._fields_ = [
    ('__val', c_int * 2),
]
__clock_t = c_long
__rlim_t = c_ulong
__rlim64_t = c_ulong
__id_t = c_uint
__useconds_t = c_uint
__daddr_t = c_int
__swblk_t = c_long
__key_t = c_int
__clockid_t = c_int
__timer_t = c_void_p
__blksize_t = c_long
__blkcnt_t = c_long
__blkcnt64_t = c_long
__fsblkcnt_t = c_ulong
__fsblkcnt64_t = c_ulong
__fsfilcnt_t = c_ulong
__fsfilcnt64_t = c_ulong
__ssize_t = c_long
__loff_t = __off64_t
__qaddr_t = POINTER(__quad_t)
__caddr_t = STRING
__intptr_t = c_long
__socklen_t = c_uint
class st_used_mem(Structure):
    pass
st_used_mem._fields_ = [
    ('next', POINTER(st_used_mem)),
    ('left', c_uint),
    ('size', c_uint),
]
USED_MEM = st_used_mem
class st_mem_root(Structure):
    pass
st_mem_root._fields_ = [
    ('free', POINTER(USED_MEM)),
    ('used', POINTER(USED_MEM)),
    ('pre_alloc', POINTER(USED_MEM)),
    ('min_malloc', c_uint),
    ('block_size', c_uint),
    ('block_num', c_uint),
    ('first_block_usage', c_uint),
    ('error_handler', CFUNCTYPE(None)),
]
MEM_ROOT = st_mem_root
class st_list(Structure):
    pass
st_list._fields_ = [
    ('prev', POINTER(st_list)),
    ('next', POINTER(st_list)),
    ('data', c_void_p),
]
LIST = st_list
list_walk_action = CFUNCTYPE(c_int, c_void_p, c_void_p)
list_add = _libraries['libmysqlclient.so'].list_add
list_add.restype = POINTER(LIST)
list_add.argtypes = [POINTER(LIST), POINTER(LIST)]
list_delete = _libraries['libmysqlclient.so'].list_delete
list_delete.restype = POINTER(LIST)
list_delete.argtypes = [POINTER(LIST), POINTER(LIST)]
list_cons = _libraries['libmysqlclient.so'].list_cons
list_cons.restype = POINTER(LIST)
list_cons.argtypes = [c_void_p, POINTER(LIST)]
list_reverse = _libraries['libmysqlclient.so'].list_reverse
list_reverse.restype = POINTER(LIST)
list_reverse.argtypes = [POINTER(LIST)]
list_free = _libraries['libmysqlclient.so'].list_free
list_free.restype = None
list_free.argtypes = [POINTER(LIST), c_uint]
list_length = _libraries['libmysqlclient.so'].list_length
list_length.restype = c_uint
list_length.argtypes = [POINTER(LIST)]
gptr = STRING
list_walk = _libraries['libmysqlclient.so'].list_walk
list_walk.restype = c_int
list_walk.argtypes = [POINTER(LIST), list_walk_action, gptr]
my_bool = c_int8
my_socket = c_int
mysql_port = (c_uint).in_dll(_libraries['libmysqlclient.so'], 'mysql_port')
mysql_unix_port = (STRING).in_dll(_libraries['libmysqlclient.so'], 'mysql_unix_port')
class st_mysql_field(Structure):
    pass

# values for enumeration 'enum_field_types'
enum_field_types = c_int # enum
st_mysql_field._fields_ = [
    ('name', STRING),
    ('org_name', STRING),
    ('table', STRING),
    ('org_table', STRING),
    ('db', STRING),
    ('catalog', STRING),
    ('def', STRING),
    ('length', c_ulong),
    ('max_length', c_ulong),
    ('name_length', c_uint),
    ('org_name_length', c_uint),
    ('table_length', c_uint),
    ('org_table_length', c_uint),
    ('db_length', c_uint),
    ('catalog_length', c_uint),
    ('def_length', c_uint),
    ('flags', c_uint),
    ('decimals', c_uint),
    ('charsetnr', c_uint),
    ('type', enum_field_types),
]
MYSQL_FIELD = st_mysql_field
MYSQL_ROW = POINTER(STRING)
MYSQL_FIELD_OFFSET = c_uint
my_ulonglong = c_ulonglong
class st_mysql_rows(Structure):
    pass
st_mysql_rows._fields_ = [
    ('next', POINTER(st_mysql_rows)),
    ('data', MYSQL_ROW),
    ('length', c_ulong),
]
MYSQL_ROWS = st_mysql_rows
MYSQL_ROW_OFFSET = POINTER(MYSQL_ROWS)
class embedded_query_result(Structure):
    pass
EMBEDDED_QUERY_RESULT = embedded_query_result
embedded_query_result._fields_ = [
]
class st_mysql_data(Structure):
    pass
st_mysql_data._fields_ = [
    ('rows', my_ulonglong),
    ('fields', c_uint),
    ('data', POINTER(MYSQL_ROWS)),
    ('alloc', MEM_ROOT),
    ('embedded_info', POINTER(embedded_query_result)),
]
MYSQL_DATA = st_mysql_data

# values for enumeration 'mysql_option'
mysql_option = c_int # enum
class st_mysql_options(Structure):
    pass
class st_dynamic_array(Structure):
    pass
st_mysql_options._fields_ = [
    ('connect_timeout', c_uint),
    ('read_timeout', c_uint),
    ('write_timeout', c_uint),
    ('port', c_uint),
    ('protocol', c_uint),
    ('client_flag', c_ulong),
    ('host', STRING),
    ('user', STRING),
    ('password', STRING),
    ('unix_socket', STRING),
    ('db', STRING),
    ('init_commands', POINTER(st_dynamic_array)),
    ('my_cnf_file', STRING),
    ('my_cnf_group', STRING),
    ('charset_dir', STRING),
    ('charset_name', STRING),
    ('ssl_key', STRING),
    ('ssl_cert', STRING),
    ('ssl_ca', STRING),
    ('ssl_capath', STRING),
    ('ssl_cipher', STRING),
    ('shared_memory_base_name', STRING),
    ('max_allowed_packet', c_ulong),
    ('use_ssl', my_bool),
    ('compress', my_bool),
    ('named_pipe', my_bool),
    ('rpl_probe', my_bool),
    ('rpl_parse', my_bool),
    ('no_master_reads', my_bool),
    ('separate_thread', my_bool),
    ('methods_to_use', mysql_option),
    ('client_ip', STRING),
    ('secure_auth', my_bool),
    ('report_data_truncation', my_bool),
    ('local_infile_init', CFUNCTYPE(c_int, POINTER(c_void_p), STRING, c_void_p)),
    ('local_infile_read', CFUNCTYPE(c_int, c_void_p, STRING, c_uint)),
    ('local_infile_end', CFUNCTYPE(None, c_void_p)),
    ('local_infile_error', CFUNCTYPE(c_int, c_void_p, STRING, c_uint)),
    ('local_infile_userdata', c_void_p),
]
st_dynamic_array._fields_ = [
]

# values for enumeration 'mysql_status'
mysql_status = c_int # enum

# values for enumeration 'mysql_protocol_type'
mysql_protocol_type = c_int # enum

# values for enumeration 'mysql_rpl_type'
mysql_rpl_type = c_int # enum
class character_set(Structure):
    pass
character_set._fields_ = [
    ('number', c_uint),
    ('state', c_uint),
    ('csname', STRING),
    ('name', STRING),
    ('comment', STRING),
    ('dir', STRING),
    ('mbminlen', c_uint),
    ('mbmaxlen', c_uint),
]
MY_CHARSET_INFO = character_set
class st_mysql(Structure):
    pass
class st_net(Structure):
    pass
class st_vio(Structure):
    pass
Vio = st_vio
st_net._fields_ = [
    ('vio', POINTER(Vio)),
    ('buff', POINTER(c_ubyte)),
    ('buff_end', POINTER(c_ubyte)),
    ('write_pos', POINTER(c_ubyte)),
    ('read_pos', POINTER(c_ubyte)),
    ('fd', my_socket),
    ('max_packet', c_ulong),
    ('max_packet_size', c_ulong),
    ('pkt_nr', c_uint),
    ('compress_pkt_nr', c_uint),
    ('write_timeout', c_uint),
    ('read_timeout', c_uint),
    ('retry_count', c_uint),
    ('fcntl', c_int),
    ('compress', my_bool),
    ('remain_in_buf', c_ulong),
    ('length', c_ulong),
    ('buf_length', c_ulong),
    ('where_b', c_ulong),
    ('return_status', POINTER(c_uint)),
    ('reading_or_writing', c_ubyte),
    ('save_char', c_char),
    ('no_send_ok', my_bool),
    ('no_send_eof', my_bool),
    ('no_send_error', my_bool),
    ('last_error', c_char * 512),
    ('sqlstate', c_char * 6),
    ('last_errno', c_uint),
    ('error', c_ubyte),
    ('query_cache_query', gptr),
    ('report_error', my_bool),
    ('return_errno', my_bool),
]
NET = st_net
class charset_info_st(Structure):
    pass
class st_mysql_methods(Structure):
    pass
MYSQL = st_mysql

# values for enumeration 'enum_server_command'
enum_server_command = c_int # enum
class st_mysql_stmt(Structure):
    pass
MYSQL_STMT = st_mysql_stmt
class st_mysql_res(Structure):
    pass
MYSQL_RES = st_mysql_res
st_mysql_methods._fields_ = [
    ('read_query_result', CFUNCTYPE(my_bool, POINTER(MYSQL))),
    ('advanced_command', CFUNCTYPE(my_bool, POINTER(MYSQL), enum_server_command, STRING, c_ulong, STRING, c_ulong, my_bool, POINTER(MYSQL_STMT))),
    ('read_rows', CFUNCTYPE(POINTER(MYSQL_DATA), POINTER(MYSQL), POINTER(MYSQL_FIELD), c_uint)),
    ('use_result', CFUNCTYPE(POINTER(MYSQL_RES), POINTER(MYSQL))),
    ('fetch_lengths', CFUNCTYPE(None, POINTER(c_ulong), MYSQL_ROW, c_uint)),
    ('flush_use_result', CFUNCTYPE(None, POINTER(MYSQL))),
    ('list_fields', CFUNCTYPE(POINTER(MYSQL_FIELD), POINTER(MYSQL))),
    ('read_prepare_result', CFUNCTYPE(my_bool, POINTER(MYSQL), POINTER(MYSQL_STMT))),
    ('stmt_execute', CFUNCTYPE(c_int, POINTER(MYSQL_STMT))),
    ('read_binary_rows', CFUNCTYPE(c_int, POINTER(MYSQL_STMT))),
    ('unbuffered_fetch', CFUNCTYPE(c_int, POINTER(MYSQL), POINTER(STRING))),
    ('free_embedded_thd', CFUNCTYPE(None, POINTER(MYSQL))),
    ('read_statistics', CFUNCTYPE(STRING, POINTER(MYSQL))),
    ('next_result', CFUNCTYPE(my_bool, POINTER(MYSQL))),
    ('read_change_user_result', CFUNCTYPE(c_int, POINTER(MYSQL), STRING, STRING)),
    ('read_rows_from_cursor', CFUNCTYPE(c_int, POINTER(MYSQL_STMT))),
]
st_mysql._fields_ = [
    ('net', NET),
    ('connector_fd', gptr),
    ('host', STRING),
    ('user', STRING),
    ('passwd', STRING),
    ('unix_socket', STRING),
    ('server_version', STRING),
    ('host_info', STRING),
    ('info', STRING),
    ('db', STRING),
    ('charset', POINTER(charset_info_st)),
    ('fields', POINTER(MYSQL_FIELD)),
    ('field_alloc', MEM_ROOT),
    ('affected_rows', my_ulonglong),
    ('insert_id', my_ulonglong),
    ('extra_info', my_ulonglong),
    ('thread_id', c_ulong),
    ('packet_length', c_ulong),
    ('port', c_uint),
    ('client_flag', c_ulong),
    ('server_capabilities', c_ulong),
    ('protocol_version', c_uint),
    ('field_count', c_uint),
    ('server_status', c_uint),
    ('server_language', c_uint),
    ('warning_count', c_uint),
    ('options', st_mysql_options),
    ('status', mysql_status),
    ('free_me', my_bool),
    ('reconnect', my_bool),
    ('scramble', c_char * 21),
    ('rpl_pivot', my_bool),
    ('master', POINTER(st_mysql)),
    ('next_slave', POINTER(st_mysql)),
    ('last_used_slave', POINTER(st_mysql)),
    ('last_used_con', POINTER(st_mysql)),
    ('stmts', POINTER(LIST)),
    ('methods', POINTER(st_mysql_methods)),
    ('thd', c_void_p),
    ('unbuffered_fetch_owner', STRING),
]
charset_info_st._fields_ = [
]
st_mysql_res._fields_ = [
    ('row_count', my_ulonglong),
    ('fields', POINTER(MYSQL_FIELD)),
    ('data', POINTER(MYSQL_DATA)),
    ('data_cursor', POINTER(MYSQL_ROWS)),
    ('lengths', POINTER(c_ulong)),
    ('handle', POINTER(MYSQL)),
    ('field_alloc', MEM_ROOT),
    ('field_count', c_uint),
    ('current_field', c_uint),
    ('row', MYSQL_ROW),
    ('current_row', MYSQL_ROW),
    ('eof', my_bool),
    ('unbuffered_fetch_cancelled', my_bool),
    ('methods', POINTER(st_mysql_methods)),
]
class st_mysql_manager(Structure):
    pass
st_mysql_manager._fields_ = [
    ('net', NET),
    ('host', STRING),
    ('user', STRING),
    ('passwd', STRING),
    ('port', c_uint),
    ('free_me', my_bool),
    ('eof', my_bool),
    ('cmd_status', c_int),
    ('last_errno', c_int),
    ('net_buf', STRING),
    ('net_buf_pos', STRING),
    ('net_data_end', STRING),
    ('net_buf_size', c_int),
    ('last_error', c_char * 256),
]
MYSQL_MANAGER = st_mysql_manager
class st_mysql_parameters(Structure):
    pass
st_mysql_parameters._fields_ = [
    ('p_max_allowed_packet', POINTER(c_ulong)),
    ('p_net_buffer_length', POINTER(c_ulong)),
]
MYSQL_PARAMETERS = st_mysql_parameters
mysql_server_init = _libraries['libmysqlclient.so'].mysql_server_init
mysql_server_init.restype = c_int
mysql_server_init.argtypes = [c_int, POINTER(STRING), POINTER(STRING)]
mysql_server_end = _libraries['libmysqlclient.so'].mysql_server_end
mysql_server_end.restype = None
mysql_server_end.argtypes = []
mysql_get_parameters = _libraries['libmysqlclient.so'].mysql_get_parameters
mysql_get_parameters.restype = POINTER(MYSQL_PARAMETERS)
mysql_get_parameters.argtypes = []
mysql_thread_init = _libraries['libmysqlclient.so'].mysql_thread_init
mysql_thread_init.restype = my_bool
mysql_thread_init.argtypes = []
mysql_thread_end = _libraries['libmysqlclient.so'].mysql_thread_end
mysql_thread_end.restype = None
mysql_thread_end.argtypes = []
mysql_num_rows = _libraries['libmysqlclient.so'].mysql_num_rows
mysql_num_rows.restype = my_ulonglong
mysql_num_rows.argtypes = [POINTER(MYSQL_RES)]
mysql_num_fields = _libraries['libmysqlclient.so'].mysql_num_fields
mysql_num_fields.restype = c_uint
mysql_num_fields.argtypes = [POINTER(MYSQL_RES)]
mysql_eof = _libraries['libmysqlclient.so'].mysql_eof
mysql_eof.restype = my_bool
mysql_eof.argtypes = [POINTER(MYSQL_RES)]
mysql_fetch_field_direct = _libraries['libmysqlclient.so'].mysql_fetch_field_direct
mysql_fetch_field_direct.restype = POINTER(MYSQL_FIELD)
mysql_fetch_field_direct.argtypes = [POINTER(MYSQL_RES), c_uint]
mysql_fetch_fields = _libraries['libmysqlclient.so'].mysql_fetch_fields
mysql_fetch_fields.restype = POINTER(MYSQL_FIELD)
mysql_fetch_fields.argtypes = [POINTER(MYSQL_RES)]
mysql_row_tell = _libraries['libmysqlclient.so'].mysql_row_tell
mysql_row_tell.restype = MYSQL_ROW_OFFSET
mysql_row_tell.argtypes = [POINTER(MYSQL_RES)]
mysql_field_tell = _libraries['libmysqlclient.so'].mysql_field_tell
mysql_field_tell.restype = MYSQL_FIELD_OFFSET
mysql_field_tell.argtypes = [POINTER(MYSQL_RES)]
mysql_field_count = _libraries['libmysqlclient.so'].mysql_field_count
mysql_field_count.restype = c_uint
mysql_field_count.argtypes = [POINTER(MYSQL)]
mysql_affected_rows = _libraries['libmysqlclient.so'].mysql_affected_rows
mysql_affected_rows.restype = my_ulonglong
mysql_affected_rows.argtypes = [POINTER(MYSQL)]
mysql_insert_id = _libraries['libmysqlclient.so'].mysql_insert_id
mysql_insert_id.restype = my_ulonglong
mysql_insert_id.argtypes = [POINTER(MYSQL)]
mysql_errno = _libraries['libmysqlclient.so'].mysql_errno
mysql_errno.restype = c_uint
mysql_errno.argtypes = [POINTER(MYSQL)]
mysql_error = _libraries['libmysqlclient.so'].mysql_error
mysql_error.restype = STRING
mysql_error.argtypes = [POINTER(MYSQL)]
mysql_sqlstate = _libraries['libmysqlclient.so'].mysql_sqlstate
mysql_sqlstate.restype = STRING
mysql_sqlstate.argtypes = [POINTER(MYSQL)]
mysql_warning_count = _libraries['libmysqlclient.so'].mysql_warning_count
mysql_warning_count.restype = c_uint
mysql_warning_count.argtypes = [POINTER(MYSQL)]
mysql_info = _libraries['libmysqlclient.so'].mysql_info
mysql_info.restype = STRING
mysql_info.argtypes = [POINTER(MYSQL)]
mysql_thread_id = _libraries['libmysqlclient.so'].mysql_thread_id
mysql_thread_id.restype = c_ulong
mysql_thread_id.argtypes = [POINTER(MYSQL)]
mysql_character_set_name = _libraries['libmysqlclient.so'].mysql_character_set_name
mysql_character_set_name.restype = STRING
mysql_character_set_name.argtypes = [POINTER(MYSQL)]
mysql_set_character_set = _libraries['libmysqlclient.so'].mysql_set_character_set
mysql_set_character_set.restype = c_int
mysql_set_character_set.argtypes = [POINTER(MYSQL), STRING]
mysql_init = _libraries['libmysqlclient.so'].mysql_init
mysql_init.restype = POINTER(MYSQL)
mysql_init.argtypes = [POINTER(MYSQL)]
mysql_ssl_set = _libraries['libmysqlclient.so'].mysql_ssl_set
mysql_ssl_set.restype = my_bool
mysql_ssl_set.argtypes = [POINTER(MYSQL), STRING, STRING, STRING, STRING, STRING]
mysql_get_ssl_cipher = _libraries['libmysqlclient.so'].mysql_get_ssl_cipher
mysql_get_ssl_cipher.restype = STRING
mysql_get_ssl_cipher.argtypes = [POINTER(MYSQL)]
mysql_change_user = _libraries['libmysqlclient.so'].mysql_change_user
mysql_change_user.restype = my_bool
mysql_change_user.argtypes = [POINTER(MYSQL), STRING, STRING, STRING]
mysql_real_connect = _libraries['libmysqlclient.so'].mysql_real_connect
mysql_real_connect.restype = POINTER(MYSQL)
mysql_real_connect.argtypes = [POINTER(MYSQL), STRING, STRING, STRING, STRING, c_uint, STRING, c_ulong]
mysql_select_db = _libraries['libmysqlclient.so'].mysql_select_db
mysql_select_db.restype = c_int
mysql_select_db.argtypes = [POINTER(MYSQL), STRING]
mysql_query = _libraries['libmysqlclient.so'].mysql_query
mysql_query.restype = c_int
mysql_query.argtypes = [POINTER(MYSQL), STRING]
mysql_send_query = _libraries['libmysqlclient.so'].mysql_send_query
mysql_send_query.restype = c_int
mysql_send_query.argtypes = [POINTER(MYSQL), STRING, c_ulong]
mysql_real_query = _libraries['libmysqlclient.so'].mysql_real_query
mysql_real_query.restype = c_int
mysql_real_query.argtypes = [POINTER(MYSQL), STRING, c_ulong]
mysql_store_result = _libraries['libmysqlclient.so'].mysql_store_result
mysql_store_result.restype = POINTER(MYSQL_RES)
mysql_store_result.argtypes = [POINTER(MYSQL)]
mysql_use_result = _libraries['libmysqlclient.so'].mysql_use_result
mysql_use_result.restype = POINTER(MYSQL_RES)
mysql_use_result.argtypes = [POINTER(MYSQL)]
mysql_master_query = _libraries['libmysqlclient.so'].mysql_master_query
mysql_master_query.restype = my_bool
mysql_master_query.argtypes = [POINTER(MYSQL), STRING, c_ulong]
mysql_master_send_query = _libraries['libmysqlclient.so'].mysql_master_send_query
mysql_master_send_query.restype = my_bool
mysql_master_send_query.argtypes = [POINTER(MYSQL), STRING, c_ulong]
mysql_slave_query = _libraries['libmysqlclient.so'].mysql_slave_query
mysql_slave_query.restype = my_bool
mysql_slave_query.argtypes = [POINTER(MYSQL), STRING, c_ulong]
mysql_slave_send_query = _libraries['libmysqlclient.so'].mysql_slave_send_query
mysql_slave_send_query.restype = my_bool
mysql_slave_send_query.argtypes = [POINTER(MYSQL), STRING, c_ulong]
mysql_get_character_set_info = _libraries['libmysqlclient.so'].mysql_get_character_set_info
mysql_get_character_set_info.restype = None
mysql_get_character_set_info.argtypes = [POINTER(MYSQL), POINTER(MY_CHARSET_INFO)]
mysql_set_local_infile_handler = _libraries['libmysqlclient.so'].mysql_set_local_infile_handler
mysql_set_local_infile_handler.restype = None
mysql_set_local_infile_handler.argtypes = [POINTER(MYSQL), CFUNCTYPE(c_int, POINTER(c_void_p), STRING, c_void_p), CFUNCTYPE(c_int, c_void_p, STRING, c_uint), CFUNCTYPE(None, c_void_p), CFUNCTYPE(c_int, c_void_p, STRING, c_uint), c_void_p]
mysql_set_local_infile_default = _libraries['libmysqlclient.so'].mysql_set_local_infile_default
mysql_set_local_infile_default.restype = None
mysql_set_local_infile_default.argtypes = [POINTER(MYSQL)]
mysql_enable_rpl_parse = _libraries['libmysqlclient.so'].mysql_enable_rpl_parse
mysql_enable_rpl_parse.restype = None
mysql_enable_rpl_parse.argtypes = [POINTER(MYSQL)]
mysql_disable_rpl_parse = _libraries['libmysqlclient.so'].mysql_disable_rpl_parse
mysql_disable_rpl_parse.restype = None
mysql_disable_rpl_parse.argtypes = [POINTER(MYSQL)]
mysql_rpl_parse_enabled = _libraries['libmysqlclient.so'].mysql_rpl_parse_enabled
mysql_rpl_parse_enabled.restype = c_int
mysql_rpl_parse_enabled.argtypes = [POINTER(MYSQL)]
mysql_enable_reads_from_master = _libraries['libmysqlclient.so'].mysql_enable_reads_from_master
mysql_enable_reads_from_master.restype = None
mysql_enable_reads_from_master.argtypes = [POINTER(MYSQL)]
mysql_disable_reads_from_master = _libraries['libmysqlclient.so'].mysql_disable_reads_from_master
mysql_disable_reads_from_master.restype = None
mysql_disable_reads_from_master.argtypes = [POINTER(MYSQL)]
mysql_reads_from_master_enabled = _libraries['libmysqlclient.so'].mysql_reads_from_master_enabled
mysql_reads_from_master_enabled.restype = my_bool
mysql_reads_from_master_enabled.argtypes = [POINTER(MYSQL)]
mysql_rpl_query_type = _libraries['libmysqlclient.so'].mysql_rpl_query_type
mysql_rpl_query_type.restype = mysql_rpl_type
mysql_rpl_query_type.argtypes = [STRING, c_int]
mysql_rpl_probe = _libraries['libmysqlclient.so'].mysql_rpl_probe
mysql_rpl_probe.restype = my_bool
mysql_rpl_probe.argtypes = [POINTER(MYSQL)]
mysql_set_master = _libraries['libmysqlclient.so'].mysql_set_master
mysql_set_master.restype = c_int
mysql_set_master.argtypes = [POINTER(MYSQL), STRING, c_uint, STRING, STRING]
mysql_add_slave = _libraries['libmysqlclient.so'].mysql_add_slave
mysql_add_slave.restype = c_int
mysql_add_slave.argtypes = [POINTER(MYSQL), STRING, c_uint, STRING, STRING]

# values for enumeration 'mysql_enum_shutdown_level'
mysql_enum_shutdown_level = c_int # enum
mysql_shutdown = _libraries['libmysqlclient.so'].mysql_shutdown
mysql_shutdown.restype = c_int
mysql_shutdown.argtypes = [POINTER(MYSQL), mysql_enum_shutdown_level]
mysql_dump_debug_info = _libraries['libmysqlclient.so'].mysql_dump_debug_info
mysql_dump_debug_info.restype = c_int
mysql_dump_debug_info.argtypes = [POINTER(MYSQL)]
mysql_refresh = _libraries['libmysqlclient.so'].mysql_refresh
mysql_refresh.restype = c_int
mysql_refresh.argtypes = [POINTER(MYSQL), c_uint]
mysql_kill = _libraries['libmysqlclient.so'].mysql_kill
mysql_kill.restype = c_int
mysql_kill.argtypes = [POINTER(MYSQL), c_ulong]

# values for enumeration 'enum_mysql_set_option'
enum_mysql_set_option = c_int # enum
mysql_set_server_option = _libraries['libmysqlclient.so'].mysql_set_server_option
mysql_set_server_option.restype = c_int
mysql_set_server_option.argtypes = [POINTER(MYSQL), enum_mysql_set_option]
mysql_ping = _libraries['libmysqlclient.so'].mysql_ping
mysql_ping.restype = c_int
mysql_ping.argtypes = [POINTER(MYSQL)]
mysql_stat = _libraries['libmysqlclient.so'].mysql_stat
mysql_stat.restype = STRING
mysql_stat.argtypes = [POINTER(MYSQL)]
mysql_get_server_info = _libraries['libmysqlclient.so'].mysql_get_server_info
mysql_get_server_info.restype = STRING
mysql_get_server_info.argtypes = [POINTER(MYSQL)]
mysql_get_client_info = _libraries['libmysqlclient.so'].mysql_get_client_info
mysql_get_client_info.restype = STRING
mysql_get_client_info.argtypes = []
mysql_get_client_version = _libraries['libmysqlclient.so'].mysql_get_client_version
mysql_get_client_version.restype = c_ulong
mysql_get_client_version.argtypes = []
mysql_get_host_info = _libraries['libmysqlclient.so'].mysql_get_host_info
mysql_get_host_info.restype = STRING
mysql_get_host_info.argtypes = [POINTER(MYSQL)]
mysql_get_server_version = _libraries['libmysqlclient.so'].mysql_get_server_version
mysql_get_server_version.restype = c_ulong
mysql_get_server_version.argtypes = [POINTER(MYSQL)]
mysql_get_proto_info = _libraries['libmysqlclient.so'].mysql_get_proto_info
mysql_get_proto_info.restype = c_uint
mysql_get_proto_info.argtypes = [POINTER(MYSQL)]
mysql_list_dbs = _libraries['libmysqlclient.so'].mysql_list_dbs
mysql_list_dbs.restype = POINTER(MYSQL_RES)
mysql_list_dbs.argtypes = [POINTER(MYSQL), STRING]
mysql_list_tables = _libraries['libmysqlclient.so'].mysql_list_tables
mysql_list_tables.restype = POINTER(MYSQL_RES)
mysql_list_tables.argtypes = [POINTER(MYSQL), STRING]
mysql_list_processes = _libraries['libmysqlclient.so'].mysql_list_processes
mysql_list_processes.restype = POINTER(MYSQL_RES)
mysql_list_processes.argtypes = [POINTER(MYSQL)]
mysql_options = _libraries['libmysqlclient.so'].mysql_options
mysql_options.restype = c_int
mysql_options.argtypes = [POINTER(MYSQL), mysql_option, STRING]
mysql_free_result = _libraries['libmysqlclient.so'].mysql_free_result
mysql_free_result.restype = None
mysql_free_result.argtypes = [POINTER(MYSQL_RES)]
mysql_data_seek = _libraries['libmysqlclient.so'].mysql_data_seek
mysql_data_seek.restype = None
mysql_data_seek.argtypes = [POINTER(MYSQL_RES), my_ulonglong]
mysql_row_seek = _libraries['libmysqlclient.so'].mysql_row_seek
mysql_row_seek.restype = MYSQL_ROW_OFFSET
mysql_row_seek.argtypes = [POINTER(MYSQL_RES), MYSQL_ROW_OFFSET]
mysql_field_seek = _libraries['libmysqlclient.so'].mysql_field_seek
mysql_field_seek.restype = MYSQL_FIELD_OFFSET
mysql_field_seek.argtypes = [POINTER(MYSQL_RES), MYSQL_FIELD_OFFSET]
mysql_fetch_row = _libraries['libmysqlclient.so'].mysql_fetch_row
mysql_fetch_row.restype = MYSQL_ROW
mysql_fetch_row.argtypes = [POINTER(MYSQL_RES)]
mysql_fetch_lengths = _libraries['libmysqlclient.so'].mysql_fetch_lengths
mysql_fetch_lengths.restype = POINTER(c_ulong)
mysql_fetch_lengths.argtypes = [POINTER(MYSQL_RES)]
mysql_fetch_field = _libraries['libmysqlclient.so'].mysql_fetch_field
mysql_fetch_field.restype = POINTER(MYSQL_FIELD)
mysql_fetch_field.argtypes = [POINTER(MYSQL_RES)]
mysql_list_fields = _libraries['libmysqlclient.so'].mysql_list_fields
mysql_list_fields.restype = POINTER(MYSQL_RES)
mysql_list_fields.argtypes = [POINTER(MYSQL), STRING, STRING]
mysql_escape_string = _libraries['libmysqlclient.so'].mysql_escape_string
mysql_escape_string.restype = c_ulong
mysql_escape_string.argtypes = [STRING, STRING, c_ulong]
mysql_hex_string = _libraries['libmysqlclient.so'].mysql_hex_string
mysql_hex_string.restype = c_ulong
mysql_hex_string.argtypes = [STRING, STRING, c_ulong]
mysql_real_escape_string = _libraries['libmysqlclient.so'].mysql_real_escape_string
mysql_real_escape_string.restype = c_ulong
mysql_real_escape_string.argtypes = [POINTER(MYSQL), STRING, STRING, c_ulong]
mysql_debug = _libraries['libmysqlclient.so'].mysql_debug
mysql_debug.restype = None
mysql_debug.argtypes = [STRING]
myodbc_remove_escape = _libraries['libmysqlclient.so'].myodbc_remove_escape
myodbc_remove_escape.restype = None
myodbc_remove_escape.argtypes = [POINTER(MYSQL), STRING]
mysql_thread_safe = _libraries['libmysqlclient.so'].mysql_thread_safe
mysql_thread_safe.restype = c_uint
mysql_thread_safe.argtypes = []
mysql_embedded = _libraries['libmysqlclient.so'].mysql_embedded
mysql_embedded.restype = my_bool
mysql_embedded.argtypes = []
mysql_manager_init = _libraries['libmysqlclient.so'].mysql_manager_init
mysql_manager_init.restype = POINTER(MYSQL_MANAGER)
mysql_manager_init.argtypes = [POINTER(MYSQL_MANAGER)]
mysql_manager_connect = _libraries['libmysqlclient.so'].mysql_manager_connect
mysql_manager_connect.restype = POINTER(MYSQL_MANAGER)
mysql_manager_connect.argtypes = [POINTER(MYSQL_MANAGER), STRING, STRING, STRING, c_uint]
mysql_manager_close = _libraries['libmysqlclient.so'].mysql_manager_close
mysql_manager_close.restype = None
mysql_manager_close.argtypes = [POINTER(MYSQL_MANAGER)]
mysql_manager_command = _libraries['libmysqlclient.so'].mysql_manager_command
mysql_manager_command.restype = c_int
mysql_manager_command.argtypes = [POINTER(MYSQL_MANAGER), STRING, c_int]
mysql_manager_fetch_line = _libraries['libmysqlclient.so'].mysql_manager_fetch_line
mysql_manager_fetch_line.restype = c_int
mysql_manager_fetch_line.argtypes = [POINTER(MYSQL_MANAGER), STRING, c_int]
mysql_read_query_result = _libraries['libmysqlclient.so'].mysql_read_query_result
mysql_read_query_result.restype = my_bool
mysql_read_query_result.argtypes = [POINTER(MYSQL)]

# values for enumeration 'enum_mysql_stmt_state'
enum_mysql_stmt_state = c_int # enum
class st_mysql_bind(Structure):
    pass
st_mysql_bind._fields_ = [
    ('length', POINTER(c_ulong)),
    ('is_null', STRING),
    ('buffer', c_void_p),
    ('error', STRING),
    ('buffer_type', enum_field_types),
    ('buffer_length', c_ulong),
    ('row_ptr', POINTER(c_ubyte)),
    ('offset', c_ulong),
    ('length_value', c_ulong),
    ('param_number', c_uint),
    ('pack_length', c_uint),
    ('error_value', my_bool),
    ('is_unsigned', my_bool),
    ('long_data_used', my_bool),
    ('is_null_value', my_bool),
    ('store_param_func', CFUNCTYPE(None, POINTER(NET), POINTER(st_mysql_bind))),
    ('fetch_result', CFUNCTYPE(None, POINTER(st_mysql_bind), POINTER(MYSQL_FIELD), POINTER(POINTER(c_ubyte)))),
    ('skip_result', CFUNCTYPE(None, POINTER(st_mysql_bind), POINTER(MYSQL_FIELD), POINTER(POINTER(c_ubyte)))),
]
MYSQL_BIND = st_mysql_bind
st_mysql_stmt._fields_ = [
    ('mem_root', MEM_ROOT),
    ('list', LIST),
    ('mysql', POINTER(MYSQL)),
    ('params', POINTER(MYSQL_BIND)),
    ('bind', POINTER(MYSQL_BIND)),
    ('fields', POINTER(MYSQL_FIELD)),
    ('result', MYSQL_DATA),
    ('data_cursor', POINTER(MYSQL_ROWS)),
    ('affected_rows', my_ulonglong),
    ('insert_id', my_ulonglong),
    ('read_row_func', CFUNCTYPE(c_int, POINTER(st_mysql_stmt), POINTER(POINTER(c_ubyte)))),
    ('stmt_id', c_ulong),
    ('flags', c_ulong),
    ('prefetch_rows', c_ulong),
    ('server_status', c_uint),
    ('last_errno', c_uint),
    ('param_count', c_uint),
    ('field_count', c_uint),
    ('state', enum_mysql_stmt_state),
    ('last_error', c_char * 512),
    ('sqlstate', c_char * 6),
    ('send_types_to_server', my_bool),
    ('bind_param_done', my_bool),
    ('bind_result_done', c_ubyte),
    ('unbuffered_fetch_cancelled', my_bool),
    ('update_max_length', my_bool),
]

# values for enumeration 'enum_stmt_attr_type'
enum_stmt_attr_type = c_int # enum
MYSQL_METHODS = st_mysql_methods
mysql_stmt_init = _libraries['libmysqlclient.so'].mysql_stmt_init
mysql_stmt_init.restype = POINTER(MYSQL_STMT)
mysql_stmt_init.argtypes = [POINTER(MYSQL)]
mysql_stmt_prepare = _libraries['libmysqlclient.so'].mysql_stmt_prepare
mysql_stmt_prepare.restype = c_int
mysql_stmt_prepare.argtypes = [POINTER(MYSQL_STMT), STRING, c_ulong]
mysql_stmt_execute = _libraries['libmysqlclient.so'].mysql_stmt_execute
mysql_stmt_execute.restype = c_int
mysql_stmt_execute.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_fetch = _libraries['libmysqlclient.so'].mysql_stmt_fetch
mysql_stmt_fetch.restype = c_int
mysql_stmt_fetch.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_fetch_column = _libraries['libmysqlclient.so'].mysql_stmt_fetch_column
mysql_stmt_fetch_column.restype = c_int
mysql_stmt_fetch_column.argtypes = [POINTER(MYSQL_STMT), POINTER(MYSQL_BIND), c_uint, c_ulong]
mysql_stmt_store_result = _libraries['libmysqlclient.so'].mysql_stmt_store_result
mysql_stmt_store_result.restype = c_int
mysql_stmt_store_result.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_param_count = _libraries['libmysqlclient.so'].mysql_stmt_param_count
mysql_stmt_param_count.restype = c_ulong
mysql_stmt_param_count.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_attr_set = _libraries['libmysqlclient.so'].mysql_stmt_attr_set
mysql_stmt_attr_set.restype = my_bool
mysql_stmt_attr_set.argtypes = [POINTER(MYSQL_STMT), enum_stmt_attr_type, c_void_p]
mysql_stmt_attr_get = _libraries['libmysqlclient.so'].mysql_stmt_attr_get
mysql_stmt_attr_get.restype = my_bool
mysql_stmt_attr_get.argtypes = [POINTER(MYSQL_STMT), enum_stmt_attr_type, c_void_p]
mysql_stmt_bind_param = _libraries['libmysqlclient.so'].mysql_stmt_bind_param
mysql_stmt_bind_param.restype = my_bool
mysql_stmt_bind_param.argtypes = [POINTER(MYSQL_STMT), POINTER(MYSQL_BIND)]
mysql_stmt_bind_result = _libraries['libmysqlclient.so'].mysql_stmt_bind_result
mysql_stmt_bind_result.restype = my_bool
mysql_stmt_bind_result.argtypes = [POINTER(MYSQL_STMT), POINTER(MYSQL_BIND)]
mysql_stmt_close = _libraries['libmysqlclient.so'].mysql_stmt_close
mysql_stmt_close.restype = my_bool
mysql_stmt_close.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_reset = _libraries['libmysqlclient.so'].mysql_stmt_reset
mysql_stmt_reset.restype = my_bool
mysql_stmt_reset.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_free_result = _libraries['libmysqlclient.so'].mysql_stmt_free_result
mysql_stmt_free_result.restype = my_bool
mysql_stmt_free_result.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_send_long_data = _libraries['libmysqlclient.so'].mysql_stmt_send_long_data
mysql_stmt_send_long_data.restype = my_bool
mysql_stmt_send_long_data.argtypes = [POINTER(MYSQL_STMT), c_uint, STRING, c_ulong]
mysql_stmt_result_metadata = _libraries['libmysqlclient.so'].mysql_stmt_result_metadata
mysql_stmt_result_metadata.restype = POINTER(MYSQL_RES)
mysql_stmt_result_metadata.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_param_metadata = _libraries['libmysqlclient.so'].mysql_stmt_param_metadata
mysql_stmt_param_metadata.restype = POINTER(MYSQL_RES)
mysql_stmt_param_metadata.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_errno = _libraries['libmysqlclient.so'].mysql_stmt_errno
mysql_stmt_errno.restype = c_uint
mysql_stmt_errno.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_error = _libraries['libmysqlclient.so'].mysql_stmt_error
mysql_stmt_error.restype = STRING
mysql_stmt_error.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_sqlstate = _libraries['libmysqlclient.so'].mysql_stmt_sqlstate
mysql_stmt_sqlstate.restype = STRING
mysql_stmt_sqlstate.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_row_seek = _libraries['libmysqlclient.so'].mysql_stmt_row_seek
mysql_stmt_row_seek.restype = MYSQL_ROW_OFFSET
mysql_stmt_row_seek.argtypes = [POINTER(MYSQL_STMT), MYSQL_ROW_OFFSET]
mysql_stmt_row_tell = _libraries['libmysqlclient.so'].mysql_stmt_row_tell
mysql_stmt_row_tell.restype = MYSQL_ROW_OFFSET
mysql_stmt_row_tell.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_data_seek = _libraries['libmysqlclient.so'].mysql_stmt_data_seek
mysql_stmt_data_seek.restype = None
mysql_stmt_data_seek.argtypes = [POINTER(MYSQL_STMT), my_ulonglong]
mysql_stmt_num_rows = _libraries['libmysqlclient.so'].mysql_stmt_num_rows
mysql_stmt_num_rows.restype = my_ulonglong
mysql_stmt_num_rows.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_affected_rows = _libraries['libmysqlclient.so'].mysql_stmt_affected_rows
mysql_stmt_affected_rows.restype = my_ulonglong
mysql_stmt_affected_rows.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_insert_id = _libraries['libmysqlclient.so'].mysql_stmt_insert_id
mysql_stmt_insert_id.restype = my_ulonglong
mysql_stmt_insert_id.argtypes = [POINTER(MYSQL_STMT)]
mysql_stmt_field_count = _libraries['libmysqlclient.so'].mysql_stmt_field_count
mysql_stmt_field_count.restype = c_uint
mysql_stmt_field_count.argtypes = [POINTER(MYSQL_STMT)]
mysql_commit = _libraries['libmysqlclient.so'].mysql_commit
mysql_commit.restype = my_bool
mysql_commit.argtypes = [POINTER(MYSQL)]
mysql_rollback = _libraries['libmysqlclient.so'].mysql_rollback
mysql_rollback.restype = my_bool
mysql_rollback.argtypes = [POINTER(MYSQL)]
mysql_autocommit = _libraries['libmysqlclient.so'].mysql_autocommit
mysql_autocommit.restype = my_bool
mysql_autocommit.argtypes = [POINTER(MYSQL), my_bool]
mysql_more_results = _libraries['libmysqlclient.so'].mysql_more_results
mysql_more_results.restype = my_bool
mysql_more_results.argtypes = [POINTER(MYSQL)]
mysql_next_result = _libraries['libmysqlclient.so'].mysql_next_result
mysql_next_result.restype = c_int
mysql_next_result.argtypes = [POINTER(MYSQL)]
mysql_close = _libraries['libmysqlclient.so'].mysql_close
mysql_close.restype = None
mysql_close.argtypes = [POINTER(MYSQL)]
st_vio._fields_ = [
]

# values for enumeration 'enum_cursor_type'
enum_cursor_type = c_int # enum
my_net_init = _libraries['libmysqlclient.so'].my_net_init
my_net_init.restype = my_bool
my_net_init.argtypes = [POINTER(NET), POINTER(Vio)]
my_net_local_init = _libraries['libmysqlclient.so'].my_net_local_init
my_net_local_init.restype = None
my_net_local_init.argtypes = [POINTER(NET)]
net_end = _libraries['libmysqlclient.so'].net_end
net_end.restype = None
net_end.argtypes = [POINTER(NET)]
net_clear = _libraries['libmysqlclient.so'].net_clear
net_clear.restype = None
net_clear.argtypes = [POINTER(NET)]
net_realloc = _libraries['libmysqlclient.so'].net_realloc
net_realloc.restype = my_bool
net_realloc.argtypes = [POINTER(NET), c_ulong]
net_flush = _libraries['libmysqlclient.so'].net_flush
net_flush.restype = my_bool
net_flush.argtypes = [POINTER(NET)]
my_net_write = _libraries['libmysqlclient.so'].my_net_write
my_net_write.restype = my_bool
my_net_write.argtypes = [POINTER(NET), STRING, c_ulong]
net_write_command = _libraries['libmysqlclient.so'].net_write_command
net_write_command.restype = my_bool
net_write_command.argtypes = [POINTER(NET), c_ubyte, STRING, c_ulong, STRING, c_ulong]
net_real_write = _libraries['libmysqlclient.so'].net_real_write
net_real_write.restype = c_int
net_real_write.argtypes = [POINTER(NET), STRING, c_ulong]
my_net_read = _libraries['libmysqlclient.so'].my_net_read
my_net_read.restype = c_ulong
my_net_read.argtypes = [POINTER(NET)]
class sockaddr(Structure):
    pass
sockaddr._fields_ = [
]
my_connect = _libraries['libmysqlclient.so'].my_connect
my_connect.restype = c_int
my_connect.argtypes = [my_socket, POINTER(sockaddr), c_uint, c_uint]
class rand_struct(Structure):
    pass
rand_struct._fields_ = [
    ('seed1', c_ulong),
    ('seed2', c_ulong),
    ('max_value', c_ulong),
    ('max_value_dbl', c_double),
]

# values for enumeration 'Item_result'
Item_result = c_int # enum
class st_udf_args(Structure):
    pass
st_udf_args._fields_ = [
    ('arg_count', c_uint),
    ('arg_type', POINTER(Item_result)),
    ('args', POINTER(STRING)),
    ('lengths', POINTER(c_ulong)),
    ('maybe_null', STRING),
    ('attributes', POINTER(STRING)),
    ('attribute_lengths', POINTER(c_ulong)),
]
UDF_ARGS = st_udf_args
class st_udf_init(Structure):
    pass
st_udf_init._fields_ = [
    ('maybe_null', my_bool),
    ('decimals', c_uint),
    ('max_length', c_ulong),
    ('ptr', STRING),
    ('const_item', my_bool),
]
UDF_INIT = st_udf_init
randominit = _libraries['libmysqlclient.so'].randominit
randominit.restype = None
randominit.argtypes = [POINTER(rand_struct), c_ulong, c_ulong]
my_rnd = _libraries['libmysqlclient.so'].my_rnd
my_rnd.restype = c_double
my_rnd.argtypes = [POINTER(rand_struct)]
create_random_string = _libraries['libmysqlclient.so'].create_random_string
create_random_string.restype = None
create_random_string.argtypes = [STRING, c_uint, POINTER(rand_struct)]
hash_password = _libraries['libmysqlclient.so'].hash_password
hash_password.restype = None
hash_password.argtypes = [POINTER(c_ulong), STRING, c_uint]
make_scrambled_password_323 = _libraries['libmysqlclient.so'].make_scrambled_password_323
make_scrambled_password_323.restype = None
make_scrambled_password_323.argtypes = [STRING, STRING]
scramble_323 = _libraries['libmysqlclient.so'].scramble_323
scramble_323.restype = None
scramble_323.argtypes = [STRING, STRING, STRING]
check_scramble_323 = _libraries['libmysqlclient.so'].check_scramble_323
check_scramble_323.restype = my_bool
check_scramble_323.argtypes = [STRING, STRING, POINTER(c_ulong)]
get_salt_from_password_323 = _libraries['libmysqlclient.so'].get_salt_from_password_323
get_salt_from_password_323.restype = None
get_salt_from_password_323.argtypes = [POINTER(c_ulong), STRING]
make_password_from_salt_323 = _libraries['libmysqlclient.so'].make_password_from_salt_323
make_password_from_salt_323.restype = None
make_password_from_salt_323.argtypes = [STRING, POINTER(c_ulong)]
make_scrambled_password = _libraries['libmysqlclient.so'].make_scrambled_password
make_scrambled_password.restype = None
make_scrambled_password.argtypes = [STRING, STRING]
scramble = _libraries['libmysqlclient.so'].scramble
scramble.restype = None
scramble.argtypes = [STRING, STRING, STRING]
check_scramble = _libraries['libmysqlclient.so'].check_scramble
check_scramble.restype = my_bool
check_scramble.argtypes = [STRING, STRING, POINTER(c_ubyte)]
get_salt_from_password = _libraries['libmysqlclient.so'].get_salt_from_password
get_salt_from_password.restype = None
get_salt_from_password.argtypes = [POINTER(c_ubyte), STRING]
make_password_from_salt = _libraries['libmysqlclient.so'].make_password_from_salt
make_password_from_salt.restype = None
make_password_from_salt.argtypes = [STRING, POINTER(c_ubyte)]
octet2hex = _libraries['libmysqlclient.so'].octet2hex
octet2hex.restype = STRING
octet2hex.argtypes = [STRING, STRING, c_uint]
get_tty_password = _libraries['libmysqlclient.so'].get_tty_password
get_tty_password.restype = STRING
get_tty_password.argtypes = [STRING]
my_init = _libraries['libmysqlclient.so'].my_init
my_init.restype = my_bool
my_init.argtypes = []
modify_defaults_file = _libraries['libmysqlclient.so'].modify_defaults_file
modify_defaults_file.restype = c_int
modify_defaults_file.argtypes = [STRING, STRING, STRING, STRING, c_int]
load_defaults = _libraries['libmysqlclient.so'].load_defaults
load_defaults.restype = c_int
load_defaults.argtypes = [STRING, POINTER(STRING), POINTER(c_int), POINTER(POINTER(STRING))]

# values for enumeration 'enum_mysql_timestamp_type'
enum_mysql_timestamp_type = c_int # enum
class st_mysql_time(Structure):
    pass
st_mysql_time._fields_ = [
    ('year', c_uint),
    ('month', c_uint),
    ('day', c_uint),
    ('hour', c_uint),
    ('minute', c_uint),
    ('second', c_uint),
    ('second_part', c_ulong),
    ('neg', my_bool),
    ('time_type', enum_mysql_timestamp_type),
]
MYSQL_TIME = st_mysql_time
class st_typelib(Structure):
    pass
st_typelib._fields_ = [
    ('count', c_uint),
    ('name', STRING),
    ('type_names', POINTER(STRING)),
    ('type_lengths', POINTER(c_uint)),
]
TYPELIB = st_typelib
find_type = _libraries['libmysqlclient.so'].find_type
find_type.restype = c_int
find_type.argtypes = [STRING, POINTER(TYPELIB), c_uint]
make_type = _libraries['libmysqlclient.so'].make_type
make_type.restype = None
make_type.argtypes = [STRING, c_uint, POINTER(TYPELIB)]
get_type = _libraries['libmysqlclient.so'].get_type
get_type.restype = STRING
get_type.argtypes = [POINTER(TYPELIB), c_uint]
copy_typelib = _libraries['libmysqlclient.so'].copy_typelib
copy_typelib.restype = POINTER(TYPELIB)
copy_typelib.argtypes = [POINTER(MEM_ROOT), POINTER(TYPELIB)]
sql_protocol_typelib = (TYPELIB).in_dll(_libraries['libmysqlclient.so'], 'sql_protocol_typelib')
sigset_t = __sigset_t
__fd_mask = c_long
class fd_set(Structure):
    pass
fd_set._fields_ = [
    ('fds_bits', __fd_mask * 16),
]
fd_mask = __fd_mask
select = _libraries['libmysqlclient.so'].select
select.restype = c_int
select.argtypes = [c_int, POINTER(fd_set), POINTER(fd_set), POINTER(fd_set), POINTER(timeval)]
class timespec(Structure):
    pass
timespec._fields_ = [
    ('tv_sec', __time_t),
    ('tv_nsec', c_long),
]
pselect = _libraries['libmysqlclient.so'].pselect
pselect.restype = c_int
pselect.argtypes = [c_int, POINTER(fd_set), POINTER(fd_set), POINTER(fd_set), POINTER(timespec), POINTER(__sigset_t)]
gnu_dev_major = _libraries['libmysqlclient.so'].gnu_dev_major
gnu_dev_major.restype = c_uint
gnu_dev_major.argtypes = [c_ulonglong]
gnu_dev_minor = _libraries['libmysqlclient.so'].gnu_dev_minor
gnu_dev_minor.restype = c_uint
gnu_dev_minor.argtypes = [c_ulonglong]
gnu_dev_makedev = _libraries['libmysqlclient.so'].gnu_dev_makedev
gnu_dev_makedev.restype = c_ulonglong
gnu_dev_makedev.argtypes = [c_uint, c_uint]
u_char = __u_char
u_short = __u_short
u_int = __u_int
u_long = __u_long
quad_t = __quad_t
u_quad_t = __u_quad_t
fsid_t = __fsid_t
loff_t = __loff_t
ino_t = __ino_t
ino64_t = __ino64_t
dev_t = __dev_t
gid_t = __gid_t
mode_t = __mode_t
nlink_t = __nlink_t
uid_t = __uid_t
off_t = __off_t
off64_t = __off64_t
pid_t = __pid_t
id_t = __id_t
ssize_t = __ssize_t
daddr_t = __daddr_t
caddr_t = __caddr_t
key_t = __key_t
useconds_t = __useconds_t
suseconds_t = __suseconds_t
ulong = c_ulong
ushort = c_ushort
uint = c_uint
int8_t = c_int8
int16_t = c_int16
int32_t = c_int32
int64_t = c_int64
u_int8_t = c_ubyte
u_int16_t = c_ushort
u_int32_t = c_uint
u_int64_t = c_ulong
register_t = c_long
blksize_t = __blksize_t
blkcnt_t = __blkcnt_t
fsblkcnt_t = __fsblkcnt_t
fsfilcnt_t = __fsfilcnt_t
blkcnt64_t = __blkcnt64_t
fsblkcnt64_t = __fsblkcnt64_t
fsfilcnt64_t = __fsfilcnt64_t
clock_t = __clock_t
time_t = __time_t
clockid_t = __clockid_t
timer_t = __timer_t
size_t = c_ulong
__all__ = ['MYSQL_TYPE_FLOAT', '__int16_t', 'MYSQL_STMT_PREPARE_DONE',
           'st_vio', '__off64_t', 'COM_STATISTICS',
           'MYSQL_SHARED_MEMORY_BASE_NAME', 'USED_MEM', 'COM_REFRESH',
           'st_net', 'mysql_fetch_lengths', 'mysql_stmt_store_result',
           'gnu_dev_major', 'enum_mysql_stmt_state',
           'mysql_stmt_insert_id', 'mysql_stmt_data_seek',
           'MYSQL_PROTOCOL_MEMORY', 'charset_info_st',
           'mysql_stmt_row_seek', '__time_t', 'mysql_stmt_prepare',
           'mysql_server_init', 'MYSQL_REPORT_DATA_TRUNCATION',
           'mysql_error', 'pid_t', 'enum_field_types',
           'mysql_get_client_version', 'gnu_dev_makedev',
           'scramble_323', 'MYSQL_TYPE_GEOMETRY', '__uint64_t',
           'STRING_RESULT', 'mode_t', 'timespec', 'my_rnd',
           'MYSQL_OPT_SSL_VERIFY_SERVER_CERT',
           'mysql_get_character_set_info', 'mysql_stmt_affected_rows',
           'KILL_CONNECTION', 'st_udf_args', 'MYSQL_OPT_PROTOCOL',
           'MYSQL_OPT_USE_EMBEDDED_CONNECTION', '__clockid_t', 'id_t',
           'COM_TABLE_DUMP', 'MYSQL_TYPE_DATE', 'MYSQL_TYPE_TINY',
           'mysql_stmt_init', 'mysql_reads_from_master_enabled',
           'mysql_master_send_query', 'mysql_kill',
           'MYSQL_OPT_LOCAL_INFILE', '__u_long', 'MYSQL_ROW',
           'mysql_query', 'pthread_t', 'COM_FIELD_LIST',
           'mysql_stmt_bind_param', 'MYSQL_TYPE_BLOB',
           'MYSQL_TYPE_INT24', '__mode_t', 'COM_STMT_PREPARE',
           'st_mysql_options', 'mysql_option', '__off_t',
           'enum_stmt_attr_type', 'CURSOR_TYPE_NO_CURSOR', 'u_quad_t',
           'net_real_write', 'fsfilcnt64_t', 'COM_INIT_DB',
           'MYSQL_ROW_OFFSET', 'mysql_num_rows', 'UDF_INIT',
           'sql_protocol_typelib', 'MYSQL_STMT_EXECUTE_DONE',
           'MYSQL_TIMESTAMP_DATE', '__int8_t', '__fsblkcnt64_t',
           'off_t', 'mysql_unix_port', 'pthread_barrierattr_t',
           'enum_mysql_timestamp_type', 'mysql_read_query_result',
           'timer_t', '__fsfilcnt64_t', 'COM_DELAYED_INSERT',
           'pthread_key_t', 'mysql_rollback', 'scramble', 'u_int8_t',
           'st_mysql', 'make_password_from_salt',
           'enum_mysql_set_option', 'st_typelib', 'COM_DROP_DB',
           '__fsblkcnt_t', 'mysql_fetch_row', 'copy_typelib',
           'st_mysql_methods', 'mysql_enum_shutdown_level',
           'MYSQL_TYPE_LONG_BLOB', 'loff_t', 'u_short', 'key_t',
           'mysql_real_query', 'MYSQL_TYPE_STRING',
           'pthread_rwlockattr_t', '__swblk_t', 'list_free',
           'mysql_slave_send_query', 'MYSQL_TIME', '__u_int',
           'ssize_t', '__clock_t', '__fsfilcnt_t',
           'mysql_free_result', 'MEM_ROOT', 'MYSQL_MANAGER',
           'make_type', 'mysql_get_parameters', 'pthread_mutexattr_t',
           'mysql_affected_rows', 'character_set', 'my_net_read',
           'MYSQL_TYPE_TINY_BLOB', 'mysql_rpl_probe',
           'mysql_rpl_type', 'blkcnt_t', 'st_mysql_data',
           'mysql_rpl_parse_enabled', '__qaddr_t',
           'mysql_fetch_fields', 'mysql_stmt_error',
           'COM_STMT_EXECUTE', 'my_connect', 'MYSQL_PROTOCOL_SOCKET',
           'MYSQL_TYPE_YEAR', 'check_scramble_323', 'u_char', 'uid_t',
           'u_int64_t', 'u_int16_t', 'mysql_get_host_info',
           'mysql_get_client_info', 'mysql_manager_fetch_line',
           'SHUTDOWN_WAIT_UPDATES', '__int32_t', 'MYSQL_TYPE_NULL',
           'off64_t', 'net_end', 'fsblkcnt64_t', '__fd_mask',
           'mysql_autocommit', 'MYSQL_TIMESTAMP_ERROR', 'clock_t',
           'COM_TIME', '__useconds_t', 'MYSQL_TYPE_TIME',
           'MYSQL_RPL_ADMIN', 'mysql_eof', 'COM_CONNECT',
           'EMBEDDED_QUERY_RESULT', 'load_defaults',
           'MYSQL_OPTION_MULTI_STATEMENTS_OFF',
           'CURSOR_TYPE_FOR_UPDATE', 'pthread_barrier_t',
           'enum_cursor_type', 'u_int32_t', 'pthread_rwlock_t',
           'mysql_refresh', '__pthread_internal_list',
           'MYSQL_TYPE_DECIMAL', 'enum_server_command',
           'MYSQL_TIMESTAMP_DATETIME', 'mysql_thread_end',
           'mysql_master_query', 'Vio', '__pthread_list_t',
           'pthread_attr_t', 'uint', '__rlim64_t', 'ino_t',
           'st_udf_init', 'MYSQL_STATUS_READY',
           'MYSQL_PROTOCOL_DEFAULT', 'mysql_next_result',
           'MYSQL_TIMESTAMP_NONE', 'mysql_change_user', '__blksize_t',
           'pthread_spinlock_t', 'MYSQL_OPT_RECONNECT',
           'mysql_get_server_info', 'mysql_field_count',
           'mysql_stmt_send_long_data', 'ino64_t',
           'MYSQL_TYPE_TIMESTAMP', 'MYSQL_TYPE_SET', 'list_cons',
           '__uint8_t', '__u_char', '__sig_atomic_t', '__blkcnt64_t',
           'get_salt_from_password', 'COM_BINLOG_DUMP',
           'mysql_rpl_query_type', 'mysql_stmt_attr_set',
           'mysql_data_seek', 'mysql_stmt_execute',
           'MYSQL_TYPE_NEWDECIMAL', 'list_walk', 'quad_t', 'LIST',
           'mysql_debug', 'SHUTDOWN_WAIT_ALL_BUFFERS', 'MYSQL',
           'Item_result', 'mysql_set_local_infile_handler',
           'pthread_cond_t', 'pselect', 'COM_DEBUG', 'ROW_RESULT',
           '__rlim_t', 'SHUTDOWN_WAIT_CONNECTIONS', 'nlink_t',
           'timeval', 'MYSQL_TYPE_LONG',
           'make_scrambled_password_323', 'mysql_set_master',
           'my_net_local_init', 'ulong', 'int8_t', 'MYSQL_ROWS',
           'my_init', 'MYSQL_TYPE_BIT', 'REAL_RESULT', 'list_add',
           'mysql_stat', 'fsblkcnt_t', '__quad_t',
           'MYSQL_SET_CHARSET_DIR', '__key_t', 'mysql_port', 'dev_t',
           '__uid_t', '__uint16_t', '__pthread_mutex_s',
           'my_net_write', 'mysql_list_fields', 'MYSQL_TYPE_DOUBLE',
           'fsfilcnt_t', 'mysql_shutdown', 'mysql_stmt_free_result',
           'embedded_query_result', 'mysql_stmt_errno', 'list_length',
           'st_dynamic_array', 'mysql_thread_init',
           'mysql_list_tables', 'gptr', 'COM_QUERY', '__loff_t',
           'MYSQL_READ_DEFAULT_FILE', 'daddr_t',
           'MYSQL_OPT_READ_TIMEOUT', 'mysql_warning_count',
           'MYSQL_BIND', 'mysql_slave_query', 'COM_STMT_FETCH',
           'mysql_commit', 'MYSQL_STMT_FETCH_DONE',
           'MYSQL_OPT_NAMED_PIPE', 'COM_SHUTDOWN', 'fd_mask',
           'MYSQL_OPTION_MULTI_STATEMENTS_ON', '__timer_t',
           'mysql_disable_rpl_parse', 'mysql_manager_connect',
           'MYSQL_OPT_COMPRESS', '__ssize_t', 'mysql_stmt_attr_get',
           'size_t', 'mysql_status', 'int16_t', 'mysql_thread_safe',
           'mysql_stmt_row_tell', 'mysql_server_end', '__sigset_t',
           'mysql_stmt_bind_result', 'COM_SET_OPTION',
           'MYSQL_TYPE_LONGLONG', 'COM_REGISTER_SLAVE', 'octet2hex',
           'mysql_real_escape_string',
           'mysql_disable_reads_from_master', 'mysql_use_result',
           'net_write_command', 'SHUTDOWN_DEFAULT',
           'mysql_stmt_num_rows', '__intptr_t', 'mysql_add_slave',
           'make_scrambled_password', 'get_salt_from_password_323',
           'TYPELIB', 'ushort', 'CURSOR_TYPE_READ_ONLY', '__blkcnt_t',
           'clockid_t', 'SHUTDOWN_WAIT_TRANSACTIONS',
           'mysql_set_character_set', 'caddr_t',
           'STMT_ATTR_UPDATE_MAX_LENGTH', 'blkcnt64_t', 'COM_PING',
           'int32_t', 'MYSQL_DATA', 'N16pthread_rwlock_t4DOT_10E',
           'MYSQL_TYPE_NEWDATE', 'mysql_more_results', 'st_mysql_res',
           'COM_CONNECT_OUT', 'MYSQL_FIELD_OFFSET',
           'mysql_dump_debug_info', 'mysql_enable_reads_from_master',
           'STMT_ATTR_PREFETCH_ROWS', 'COM_QUIT',
           'MYSQL_TYPE_DATETIME', '__dev_t', 'mysql_enable_rpl_parse',
           '__suseconds_t', 'u_long', 'MYSQL_SET_CHARSET_NAME',
           'MYSQL_RPL_SLAVE', 'MYSQL_OPT_GUESS_CONNECTION',
           'mysql_select_db', 'mysql_close', 'COM_STMT_CLOSE',
           'MYSQL_READ_DEFAULT_GROUP', 'time_t',
           'STMT_ATTR_CURSOR_TYPE', 'mysql_field_seek', 'blksize_t',
           'create_random_string', 'MYSQL_OPT_USE_RESULT',
           'mysql_errno', 'MYSQL_PROTOCOL_PIPE', 'get_tty_password',
           'my_ulonglong', 'mysql_store_result', 'list_delete',
           'st_mysql_manager', 'mysql_character_set_name',
           'MYSQL_SET_CLIENT_IP', 'mysql_embedded',
           'MYSQL_TYPE_VAR_STRING', '__ino_t',
           'MYSQL_OPT_CONNECT_TIMEOUT', 'st_mysql_field',
           'pthread_mutex_t', '__int64_t', 'mysql_set_server_option',
           'suseconds_t', 'COM_STMT_RESET', 'st_list',
           'mysql_get_ssl_cipher', 'pthread_condattr_t',
           'pthread_once_t', '__fsid_t', 'mysql_info', 'mysql_init',
           '__uint32_t', 'mysql_get_proto_info', 'fd_set',
           'list_reverse', 'st_mysql_time', 'MYSQL_METHODS',
           'st_mysql_rows', '__ino64_t', 'st_mysql_stmt',
           'gnu_dev_minor', 'MYSQL_FIELD', 'COM_PROCESS_INFO',
           'mysql_manager_command', 'MYSQL_STMT_INIT_DONE',
           'mysql_stmt_param_metadata', 'KILL_QUERY',
           'mysql_insert_id', 'register_t', 'net_flush',
           'COM_STMT_SEND_LONG_DATA', 'MYSQL_TYPE_SHORT', 'sigset_t',
           '__nlink_t', 'mysql_stmt_field_count',
           'MYSQL_TYPE_VARCHAR', 'mysql_manager_init',
           'mysql_list_processes', 'MYSQL_TYPE_ENUM', 'mysql_ssl_set',
           'st_mysql_parameters', 'MYSQL_OPT_USE_REMOTE_CONNECTION',
           'mysql_ping', 'net_clear', 'myodbc_remove_escape',
           'rand_struct', 'hash_password', '__id_t',
           'MYSQL_RPL_MASTER', 'CURSOR_TYPE_SCROLLABLE',
           'make_password_from_salt_323', 'select',
           'mysql_hex_string', 'mysql_sqlstate', 'mysql_row_tell',
           'randominit', 'N14pthread_cond_t3DOT_7E',
           'mysql_stmt_fetch', 'COM_CREATE_DB', 'MYSQL_INIT_COMMAND',
           'st_mem_root', 'mysql_protocol_type', 'mysql_thread_id',
           'MYSQL_RES', 'mysql_get_server_version', 'get_type',
           'COM_END', 'mysql_row_seek', 'NET',
           'mysql_stmt_param_count', '__gid_t', 'MYSQL_PROTOCOL_TCP',
           'MYSQL_OPT_WRITE_TIMEOUT', 'mysql_real_connect',
           'COM_SLEEP', 'my_socket', '__daddr_t', 'DECIMAL_RESULT',
           '__caddr_t', 'mysql_list_dbs', 'COM_PROCESS_KILL', 'u_int',
           'COM_CHANGE_USER', 'check_scramble',
           'SHUTDOWN_WAIT_CRITICAL_BUFFERS', 'gid_t',
           'MYSQL_STATUS_USE_RESULT', 'mysql_escape_string',
           'MYSQL_TYPE_MEDIUM_BLOB', 'mysql_stmt_fetch_column',
           'MYSQL_STATUS_GET_RESULT', 'find_type', 'sockaddr',
           'MYSQL_TIMESTAMP_TIME', 'my_bool', 'mysql_fetch_field',
           'net_realloc', 'mysql_set_local_infile_default', 'int64_t',
           'mysql_fetch_field_direct', 'modify_defaults_file',
           'MYSQL_PARAMETERS', 'list_walk_action', 'mysql_stmt_reset',
           '__u_quad_t', '__u_short', 'st_mysql_bind',
           'mysql_field_tell', 'fsid_t', 'MYSQL_SECURE_AUTH',
           '__pid_t', 'mysql_num_fields', 'mysql_stmt_close',
           'st_used_mem', 'INT_RESULT', 'mysql_stmt_result_metadata',
           'mysql_stmt_sqlstate', 'UDF_ARGS', 'useconds_t',
           'MY_CHARSET_INFO', 'mysql_send_query', 'my_net_init',
           'mysql_manager_close', 'MYSQL_STMT', '__socklen_t',
           'mysql_options']

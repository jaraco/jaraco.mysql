from ctypes import *

STRING = c_char_p


# LICENSE = GPL # alias
MYSQL_UNIX_ADDR = '/tmp/mysql.sock' # Variable STRING '"/tmp/mysql.sock"'
MYSQL_BASE_VERSION = 'mysqld-5.1' # Variable STRING '"mysqld-5.1"'
FRM_VER = 6 # Variable c_int '6'
MYSQL_SERVER_VERSION = '5.1.30' # Variable STRING '"5.1.30"'
MYSQL_COMPILATION_COMMENT = 'MySQL Community Server (GPL)' # Variable STRING '"MySQL Community Server (GPL)"'
MYSQL_VERSION_ID = 50130 # Variable c_int '50130'
MYSQL_CONFIG_NAME = 'my' # Variable STRING '"my"'
MYSQL_PORT_DEFAULT = 0 # Variable c_int '0'
MYSQL_PORT = 3306 # Variable c_int '3306'
MYSQL_SERVER_SUFFIX_DEF = '-community' # Variable STRING '"-community"'
PROTOCOL_VERSION = 10 # Variable c_int '10'
__all__ = ['MYSQL_UNIX_ADDR', 'MYSQL_BASE_VERSION', 'FRM_VER',
           'MYSQL_SERVER_VERSION', 'MYSQL_COMPILATION_COMMENT',
           'MYSQL_VERSION_ID', 'MYSQL_CONFIG_NAME',
           'MYSQL_PORT_DEFAULT', 'MYSQL_PORT',
           'MYSQL_SERVER_SUFFIX_DEF', 'PROTOCOL_VERSION']

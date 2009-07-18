from ctypes import *

STRING = c_char_p


# LICENSE = GPL # alias
MYSQL_UNIX_ADDR = '/var/run/mysqld/mysqld.sock' # Variable STRING '(const char*)"/var/run/mysqld/mysqld.sock"'
MYSQL_BASE_VERSION = 'mysqld-5.0' # Variable STRING '(const char*)"mysqld-5.0"'
FRM_VER = 6 # Variable c_int '6'
MYSQL_SERVER_VERSION = '5.0.75' # Variable STRING '(const char*)"5.0.75"'
MYSQL_COMPILATION_COMMENT = '(Ubuntu)' # Variable STRING '(const char*)"(Ubuntu)"'
MYSQL_VERSION_ID = 50075 # Variable c_int '50075'
MYSQL_CONFIG_NAME = 'my' # Variable STRING '(const char*)"my"'
MYSQL_PORT_DEFAULT = 0 # Variable c_int '0'
MYSQL_PORT = 3306 # Variable c_int '3306'
MYSQL_SERVER_SUFFIX_DEF = '-0ubuntu10.2' # Variable STRING '(const char*)"-0ubuntu10.2"'
PROTOCOL_VERSION = 10 # Variable c_int '10'
__all__ = ['MYSQL_UNIX_ADDR', 'MYSQL_BASE_VERSION', 'FRM_VER',
           'MYSQL_SERVER_VERSION', 'MYSQL_COMPILATION_COMMENT',
           'MYSQL_VERSION_ID', 'MYSQL_CONFIG_NAME',
           'MYSQL_PORT_DEFAULT', 'MYSQL_PORT',
           'MYSQL_SERVER_SUFFIX_DEF', 'PROTOCOL_VERSION']

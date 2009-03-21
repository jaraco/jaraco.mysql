import sys
sys.path.append('.')

from jaraco.mysql import _mysql

_mysql.server_init(['foo'])
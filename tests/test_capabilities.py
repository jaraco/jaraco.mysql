import re
import os

from jaraco.mysql import _mysql

uri_pattern = re.compile('mysql://(?P<user>.*):(?P<passwd>.*)@(?P<host>.*)/(?P<db>.*)')
uri_match = uri_pattern.match(os.environ['MYSQL_TEST_DB'])
db = _mysql.connect(**uri_match.groupdict())

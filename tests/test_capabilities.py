import re
import os

from jaraco.mysql import _mysql

# grab the parameters from a sqlalchemy-style URI out of the
#  environment.
uri_pattern = re.compile('mysql://(?P<user>.*):(?P<passwd>.*)@(?P<host>.*)/(?P<db>.*)')
uri_match = uri_pattern.match(os.environ['MYSQL_TEST_DB'])
params = uri_match.groupdict()

db = _mysql.connect(**params)
print db
#db.query("select * from role;")
#print db.field_count()
#res = db.use_result()

db.query("CREATE TABLE `jaracotest` (col1 INT, col2 BLOB) ENGINE=INNODB CHARACTER SET UTF8")
res = db.store_result()
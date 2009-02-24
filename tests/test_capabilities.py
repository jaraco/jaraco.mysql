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
db.query("select * from role;")
print db.field_count()
#db.use_result()
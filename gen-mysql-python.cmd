@echo off
REM first install Mysql 5.1 with developer options
REM also install gccxml (from CVS or ctypes site) and ctypeslib
REM also, note gccxml requires MSVC 6, 7, 7.1
REM for more info, visit http://starship.python.net/crew/theller/ctypes/old/codegen.html

SET MYSQL_HOME=c:\Program Files\MySQL\MySQL Server 5.1

SET PATH=%PATH%;%MYSQL_HOME%\lib\opt

echo Generating xml
REM Need WIN32_LEAN_AND_MEAN to exclude most windows stuff
h2xml -I "%MYSQL_HOME%\include" -D WIN32_LEAN_AND_MEAN config-win.h mysql.h -o mysql.xml 
h2xml -c -I "%MYSQL_HOME%\include" errmsg.h -o errmsg.xml
h2xml -c -I "%MYSQL_HOME%\include" mysql_version.h -o mysql_version.xml

echo generating python libs
xml2py mysql.xml -l libmysql.dll -o "jaraco\mysql\_mysql_api.py"
REM Use -s MYSQL to get the MYSQL structure and ancestral structures
xml2py errmsg.xml -o jaraco\mysql\_mysql_errmsg.py
xml2py mysql_version.xml -o jaraco\mysql\_mysql_version.py

: TODO: patch the _mysql_api.py as follows
: 1) Change my_bool = c_char to my_bool = c_int8
: 2) Change mysql_autocommit arg2 from c_char to my_bool
: 3) Patch to support robust library location

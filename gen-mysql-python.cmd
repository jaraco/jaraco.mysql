@echo off
REM first install Mysql 5.1 with developer options
REM also install gccxml (from CVS or ctypes site) and ctypeslib
REM also, note gccxml requires MSVC 6, 7, 7.1
REM for more info, visit http://starship.python.net/crew/theller/ctypes/old/codegen.html

SET MYSQL_HOME=c:\Program Files\MySQL\MySQL Server 5.1

SET PATH=%PATH%;%MYSQL_HOME%\lib\opt

echo Generating xml
REM Need WIN32_LEAN_AND_MEAN to exclude most windows stuff
h2xml -c -I "%MYSQL_HOME%\include" -D WIN32_LEAN_AND_MEAN config-win.h mysql.h -o mysql.xml 

echo generating python lib
xml2py mysql.xml -l libmysql.dll -o "jaraco\mysql\_mysql_api.py"

REM Use -s MYSQL to get the MYSQL structure and ancestral structures
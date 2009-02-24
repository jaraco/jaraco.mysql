from jaraco.mysql import _mysql

db = _mysql.connect(
	host='leviathan.imc.jaraco.com',
	user='jaraco',
	passwd='pa55word',
	db='rbb')
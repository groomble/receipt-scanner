import jaydebeapi 

def connection():
	connection=jaydebeapi.connect("org.h2.Driver","jdbc:h2:tcp://localhost/~/test",["sa","sa"],"../../../../h2-1.4.197.jar",)
	curs=connection.cursor()
	return curs,connection
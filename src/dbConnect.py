import sqlite3
from sqlite3 import Error


def databaseConnect(database_file):
	"""Create a connectiong to the database or create one if it doesn't exist"""
	try:
		conn=sqlite3.connect(database_file)
		conn.row_factory=sqlite3.Row
		return conn
	except Error as e:
		print(e)
	return None
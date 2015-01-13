import sqlite3
from db_head import db_file


def all_tables(cursor):	
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	return cursor.fetchall()
	
def show(table, cursor):
	cursor.execute("SELECT * FROM " + table + ";")
	print cursor.fetchall()

con = sqlite3.connect(db_file)
cursor = con.cursor()
for table in all_tables(cursor):
	print table[0]
	show(table[0],cursor)
con.close()
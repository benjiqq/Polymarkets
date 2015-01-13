import sqlite3
db_file = 'polymarkets.db'

def get_ticker():
	conn = sqlite3.connect(db_file)
	c = conn.cursor()
	c.execute('SELECT distinct ticker FROM stocks')
	ticker = [x[0] for x in c.fetchall()]
	return ticker

def get_closes(ticker):
	conn = sqlite3.connect(db_file)
	c = conn.cursor()

	c.execute('SELECT date,adjclose FROM stocks where ticker=? and dayindex>41000',(ticker,))
	data = [x for x in c.fetchall()]
	datadict = list()
	for row in data:
		datadict.append({'date':row[0],'close':row[1]})

	return datadict



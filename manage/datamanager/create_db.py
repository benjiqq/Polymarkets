import sqlite3
from db_head import db_file

conn = sqlite3.connect(db_file)

c = conn.cursor()

#Date,Open,High,Low,Close,Volume,Adj Close

c.execute('''CREATE TABLE stocks
             (ticker text, dayindex int, date text,  open real, high real, low real, close real, volume int, adjclose real)''')

c.execute('''CREATE TABLE failed_ticker
             (ticker text)''')

conn.commit()

conn.close()
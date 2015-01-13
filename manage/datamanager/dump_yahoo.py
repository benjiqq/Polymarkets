import sqlite3
import os
import time
from datetime import date
from os.path import dirname

from db_head import db_file


VOLUME = 5
ADJ_CLOSE = 6
full_path = os.path.realpath(__file__)
fpath, file = os.path.split(full_path)
datadir = os.path.join(dirname(dirname(fpath)),'data','csv')

def today_str():
   return time.strftime('%Y-%m-%d')

def check_line(line):
  arr = line.split(',')  
  try:
    for i in range(1,5):
      float(arr[i])
  except:
    return 'error with line ',line 

def process_file(fi):
  fp = os.path.join(datadir,fi)
  if os.path.exists(fp):
    f = open(fp,'r')
    lines = f.readlines()[1:]
    f.close()
    i = 0
    for line in lines:
      #print i,':',line
      r = check_line(line)
      if r:
        return r
         
      i+=1

def diff_days(dt):
  d0 = date(1900, 1, 1)
  #2013-08-06
  z = dt.split('-')
  y,m,d = int(z[0]), int(z[1]),int(z[2])
  d1 = date(y,m,d)
  delta = d1 - d0
  return delta.days

def insert_into_db(ticker,fp):
  if os.path.exists(fp):
    f = open(fp,'r')
    lines = f.readlines()[1:]
    f.close()
    i = 0
    rows = list()
    for line in lines:
      arr = line.split(',')
      td = arr[0]
      dd = diff_days(arr[0])
      rows.append([ticker] + [dd] + arr)

    conn = sqlite3.connect(db_file)
    c = conn.cursor()    
    c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?,?)', rows)
    conn.commit()

    conn.close()    


def check_ok():
  csvlist = os.listdir(datadir)
  failed = list()
  for x in csvlist[:]:    
    if x =='.DS_STORE': continue
    ticker = x.replace('.csv','')
    error = process_file(x,)
    ffp = os.path.join(datadir,x)
    print ffp
    if not error:
      insert_into_db(ticker,ffp)
    else:
      
      failed.append((ticker,))

      
      print 'removing ',ffp
      os.remove(ffp)


  if len(failed)>0:    
    conn = sqlite3.connect(db_file)

    c = conn.cursor()

    c.executemany('INSERT INTO failed_ticker VALUES (?)', failed)

    conn.commit()

    conn.close()

if __name__=='__main__':
  check_ok()

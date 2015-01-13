import os
import sys
from ORM import *


datadir = '/Users/blc/projects/finbrowser/fetch/pure/'

'''
INCOMESTATEMENT;SYM;DATE;SALES;EBIT;DEPR;TOTALNI;EPS;TAXRATE
BALANCESHEET;SYM;DATE;CURRENT ASSETS;CURRENT LIABIILITIES;LONG TERM DEBT;SHARES OUTSTANDING
INCOMESTATEMENT;A;10/02;6010000000.0;-1550000000.0;735000000.0;-1020000000.0;-2.2;0.0
BALANCESHEET;A;10/11;9060000000.0;4750000000.0;1930000000.0;347000000.0
'''

def dump_msn():
    ''' dump msn '''
    f = open(datadir + 'stockdata.txt','r')
    lines = f.readlines()
    f.close()

    income_cols = []
    for x in lines[0].split(';')[3:]:
        x = x.replace('\n','')
        income_cols.append(x)

    balancesheet_cols = []
    for x in lines[1].split(';')[3:]:
        x = x.replace('\n','')
        balancesheet_cols.append(x)


    #create stocks
    data_stock = {}
    stock_types = {}
    syms = list()
    for line in lines[2:]:
        line = line.replace('\n','')
        arr = line.split(';')
        sym = arr[1]
        data_stock[sym] = list()
        if sym not in syms:
            s = Stock(id=None,symbol = arr[1])
            s.save()
            stock_types[sym] = s
            syms.append(sym)


    for line in lines[2:]:
        line = line.replace('\n','')
        arr = line.split(';')
        typeStatement,symbol = arr[:2]
        data_stock[symbol].append(arr[0:])

    reports = list() # as string


    print sorted(data_stock.keys())

    #for each line itme
    for key in sorted(data_stock.keys())[:10]:
        values = data_stock[key]
        stocktype = stock_types[key]
        print 'insert stock line items ',key,len(values)
        for row in values[:]:
            #print stocktype.id
            rep = Report(date=row[2],reportType=row[0],stock=stocktype)
            #print 'rep: ',rep
            if str(rep) not in reports:
                reports.append(str(rep))
                rep.save()



            i = 0
            for lineitem in row[3:]:
                if row[0] == 'INCOMESTATEMENT':
                    cols = income_cols
                else:
                    cols = balancesheet_cols

                li = LineItem(report=rep,lineitemType=cols[i],value=lineitem)
                li.save()
                #print key,li
                i+=1

def convert_number_yahoo(number):
    floatvalue = 0
    if 'B' in number:
        number = number.replace('B','')
        f = float(number)
        floatvalue = f * 10**9

    if 'M' in number:
        number = number.replace('M','')
        f = float(number)
        floatvalue = f * 10**6

    return floatvalue

def dump_yahoo():
    ''' dump yahoo '''

    f = open(datadir + 'keystats.csv','r')
    lines = f.readlines()
    f.close()

    ydata = {}
    for li in lines:
        li = li.replace('\n','')
        stock,key,value = li.split(';')
        if stock not in ydata.keys():
            ydata[stock] = dict()
        ydata[stock][key] = value

    for sym,data in ydata.items():
        #print ydata['AAPL']
        #print len(Stock.objects.all())

        
        s = Stock(sym)
        print s
        #stock = Stock.objects.filter(symbol=sym)
        #mcapf = convert_number_yahoo(data['market_cap'])
        #stock.update(market_cap=mcapf)
        #print stock
        #s.save()
    

if __name__=='__main__':    
    #dump_msn()
    dump_yahoo()

import urllib2
from sp import *

turl = "http://investing.money.msn.com/investments/financial-statements?symbol="

for symbol in get_sp500():

    #symbol = 'rht'
    f = urllib2.urlopen(turl+symbol)
    s = f.read()

    fi = open('./raw/' + symbol + '.html','w')

    fi.write(s)
    fi.close()

    print symbol

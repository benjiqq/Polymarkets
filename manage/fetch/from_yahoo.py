import urllib2

from sp import *


#TODO
#run demon batch
#check data
# (industries=499)

def correctYahoo(sym):
    if '.' in sym: sym = sym.replace('.','-')
    return sym

def store_quotes(sym):
    turl = "http://finance.yahoo.com/q/is?s=%s"
    #...


def store_summary_raw(sym):
    turl = "http://finance.yahoo.com/q?s=%s&ql=1"
    u = urllib2.urlopen(turl%(sym))
    s = u.read()

    try:
        i1 = s.index('yfi_quote_summary_data')    
        i2 = s.index('Div &amp; Yield')+100
        s = s[i1:i2]
        f = open('./rawSummary/' + sym + '.html','w')
        f.write(s)
        f.close()

    except:
        print 'error ',symbol

def store_industry(sym):
    print 'sym ',sym
    turl = "http://finance.yahoo.com/q/in?s=%s"
    u = urllib2.urlopen(turl%(sym))
    s = u.read()

    x = 'Sector:</th><td nowrap class="yfnc_tabledata1"><a href="http://biz.yahoo.com/p/8conameu.html">'
    #Technology    
    y = 'Industry:</th><td nowrap class="yfnc_tabledata1"><a href="http://biz.yahoo.com/ic/811.html">'
    #Personal Computers</a></td></tr></table>
    try:        
        i1 = s.index('Sector:</th><td nowrap class="yfnc_tabledata1">')
        i2 = s.index('Industry:</th><td nowrap class="yfnc_tabledata1">')
    except:
        print 'error ',sym
        raise Exception
        
    i1+=len(x)
    i2+=len(y)
    indu =  s[i1:i1+50].split('<')[0]
    sector = s[i2:i2+50].split('<')[0]
    return [indu,sector]

def relace_yahoo_sym():
    d = {'BRK.B','BRK-B',
         'BF.B','BF-B'}
    

def get_industries():
    fi = open('industries.csv','w')
    i = 0
    for sym in get_sp500()[:]:
        sym = correctYahoo(sym)

        #store_summary_raw(symbol)
        print i,' : ',sym
        i+=1
        try:
            [indu,sector] = store_industry(sym)
            fi.write(sym + ';' + indu + ';' + sector + '\n')
        except:
            print 'error'
        #print sym,indu,sector


    fi.close()


def get_keystats():
    import ystockquote
    fi = open('keystats.csv','w')
    for sym in get_sp500()[:]:
        sym = correctYahoo(sym)
        stats = ystockquote.get_all(sym)

        for k,v in stats.items():
            s = ';'.join([sym,k,v])
            print s
            fi.write(s + '\n')
        
    fi.close()

    '''
    stock_exchange "NasdaqNM"
    market_cap 226.0B
    200day_moving_avg 643.045
    52_week_high 774.38
    price_earnings_growth_ratio 1.28
    price_sales_ratio 4.75
    price 687.918
    earnings_per_share 31.912
    50day_moving_avg 726.86
    avg_daily_volume 2850670
    volume 2324569
    52_week_low 556.52
    short_ratio 1.40
    price_earnings_ratio 21.55
    dividend_yield N/A
    dividend_per_share 0.00
    price_book_ratio 3.32
    ebitda 15.851B
    change +0.328
    book_value 207.054
    '''

def get_quote():
    import urllib
    template = "http://ichart.yahoo.com/table.csv?s=%s&a=00&b=2&c=2005&d=05&e=30&f=2012&g=d&ignore=.csv"
    symlist = ['AAPL','MSFT'] #file('whatever').read()
    wdir = '/Users/blc/projects/vcap/data/csv/'
    for sym in get_sp500()[:]:
        url = template % sym
        stuff = urllib.urlopen(url).read()
        with open(wdir + sym + '.csv','w') as f:
            f.write(stuff)

if __name__=='__main__':
    #get_industries()
    #get_keystats()
    #get_quote()

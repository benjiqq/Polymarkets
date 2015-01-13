import urllib
import urllib2
#from bs4 import BeautifulSoup
from xgoogle import *

gurl = "http://www.google.de"
from xgoogle.search import GoogleSearch
gs = GoogleSearch("a random web page")
gs.results_per_page = 50
results = gs.get_results()
print len(results)

for r in results:
    print r
'''
#data = urllib.urlencode({'site': 'adidas-group.com','q':'xls'})
headers = {'q':'xls'}
request = urllib2.Request(gurl, headers=headers)
response = urllib2.urlopen(request)

htmlstr = response.read()


gs = GoogleSearch("adidas")
gs.results_per_page = 50
results = gs.get_results()
for res in results:
  print res.title.encode('utf8')
  print res.desc.encode('utf8')
  print res.url.encode('utf8')


#for link in soup.find_all('a')[:]:
#    href = link['href']
#    #if 'google' in href: continue
#    print href
'''

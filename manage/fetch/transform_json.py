import json

inf = open('./pure/keystats.csv','r')
lines = inf.readlines()
inf.close()

stocks = dict()
for line in lines[:50]:
	line = line.replace('\n','')
	arr = line.split(';')
	stock,keystat,value = arr
	if stock not in stocks.keys(): stocks[stock]=dict()
	stocks[stock][keystat]=value

print stocks
s = json.dumps(stocks)
f = open('keystat.json', 'w')
f.write(s)
f.close()


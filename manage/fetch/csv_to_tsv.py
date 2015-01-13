import os

sym = 'AMZN'

csvdir = '/Users/blc/projects/vcap/data/csv/'
tsvdir = '/Users/blc/projects/vcap/data/tsv/'

def cp(sym):
    try:
        f = open(csvdir + sym + '.csv','r')
        lines = f.readlines()
        f.close()

        o = open(tsvdir + sym + '.tsv','w')

        o.write('date\tclose\n')
        for line in lines[1:]:
            arr = line.split(',')
            s = arr[0] + '\t' + arr[6]
            o.write(s)
        o.close()
    except:
        return

for x in os.listdir(csvdir):
    cp(x.split('.csv')[0])

import os 


wdir = './raw/'

cols_IS = ['DATE','SALES','EBIT','DEPR','TOTALNI','EPS','TAXRATE']
cols_BS = ['DATE','CURRENT ASSETS','CURRENT LIABIILITIES','LONG TERM DEBT', 'SHARES OUTSTANDING']

def getlines(filename):
    f = open(wdir + filename,'r')
    lines = f.readlines()
    f.close()
    return lines
    

def skip_head(lines):
    section = 0
    a,b,c,d = 0,0,0,0
    for i,line in enumerate(lines):
        if '<table' in line and section==0:
            a = i
        if '</table' in line and section==0:
            b = i        
            section = 1
        if '<table' in line and section==1:
            c = i
        if '</table' in line and section==1:
            d = i        
    return [lines[a:b],lines[c:d]]
            

def transform_html(lines):
    i = 0
    allrows = list()
    row = list()
    dates = list()
    for line in lines[:]:
            
            cc = '<' in line or '>' in line        
            line = line.replace(' ','')
            if len(line)>5 and not cc:
                #print i,line                
                if '/' in line:
                    line = line.replace('\r\n','')
                    allrows.append(row)
                    dates.append(line)
                    row = list()
                else:
                    line = line.replace('\r\n','')
                    row.append(line)
            i+=1
    allrows.append(row)
    allrows = allrows[1:]
    
    #print dates
    
    newrows = list()
    for i,row in enumerate(allrows):        
        newrow = list()
        newrow.append(dates[i])
        for r in row:
            newrow.append(reformat_num(r))
        #print newrow
        newrows.append(newrow)
    return newrows

def reformat_num(s):
    s = s.replace(',','')
    factor = 1
    if 'Bil' in s:
        factor = 10**9
        s = s.replace('Bil','')
    if 'Mil' in s:
        factor = 10**6
        s = s.replace('Mil','')
        
    s = float(s) * factor
    return s


def statementAsString(first,sym,isLines):
    alls = ""
    rows = transform_html(isLines)

    for r in rows:
        s = ';'.join([str(x) for x in r])
        alls +=first+';'+sym+';'+s+'\n'
    return alls

def tall():
    filelist = os.listdir(wdir)[1:]
    print filelist[:5]
    out = open('stockdata.txt','w')

    out.write(';'.join(cols_IS) + '\n')
    out.write(';'.join(cols_BS) + '\n')

    for f in filelist[:]:
        sym = f.split('.')[0]
        print sym,'*'*5
        lines = getlines(f)
        # income statement, balance sheet
        h = ';'.join(cols_IS)
        [isLines,bsLines] = skip_head(lines) 
        alls = statementAsString('INCOMESTATEMENT',sym,isLines)
        out.write(alls)
        alls = statementAsString('BALANCESHEET',sym,bsLines)
        out.write(alls)

    out.close()

tall()

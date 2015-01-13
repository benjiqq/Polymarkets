def get_sp500():
    f = open('sp500.txt','r')

    lines = f.readlines()

    f.close()

    syms = list()
    for line in lines[1:]:    
        line = line.replace('\t',' ')
        sym = line.split(' ')
        syms.append(sym[0])

    return syms

import numpy as np
from  inspect import getsource

def one_rrstr(x,n=0): # округление до n знаков после запятой
    if n == 0:
        return str(x)
    fmt = '{:.'+str(n)+'f}'
    return fmt.format(x).replace('.',',')

rrstr = np.vectorize(one_rrstr)
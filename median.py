from heapq import *

def load_ints():
    file = '/Users/vanessafelso/Documents/6.00x Files/Algorithm 6/Median.txt'
    #file = '/Users/vanessafelso/Documents/6.00x Files/Algorithm 6/test.txt'
    ints = []
    with open(file,'r') as f:
                for line in f:
                    x = int(line.strip())
                    ints.append(x)                    
    return ints
def median(A):
    first=A.pop(0)
    second=A.pop(0)
    k,med=3,0
    med=(med+first+second) % 10000
    heapl,heaph=[],[]
    if first<second:
        heappush(heapl,-first); heappush(heaph,second)
    else:
        heappush(heapl,-second); heappush(heaph,first)
    while A:
        x=A.pop(0)
        heapl,heaph=appropriate(x,heapl,heaph)
        m=choice(heapl,heaph)
        med=(med+m) % 10000
        k+=1
    return med
def appropriate(x,hl,hh):
    topbound=abs(hl[0])
    botbound=hh[0]
    if len(hl)==len(hh):
        if x<botbound:
            heappush(hl,-x)
        else:
            heappush(hh,x)
    elif len(hh)<len(hl):
        if hh[0]>x:
            if abs(hl[0])>x:
                heappush(hl,-x)
                heappush(hh,abs(heappop(hl)))
            else:
                heappush(hh,x)
        else:
            heappush(hh,x)
    else:
        if abs(hl[0])<x:
            if hh[0]<x:
                heappush(hh,x)
                heappush(hl,-heappop(hh))
            else:
                heappush(hl,-x)
        else:
            heappush(hl,-x)
    return hl,hh
def choice(hl,hh):
    if len(hh)>len(hl):
        return hh[0]
    else:
        return abs(hl[0])
                
A=load_ints()
print median(A)
#1213
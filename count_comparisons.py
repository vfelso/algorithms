def load_array(file):
    array = []
    with open(file,'r') as ints:
                for line in ints:
                    t = line.strip().split()
                    for x in t:
                        array.append(int(x))
    return array

def lazy_pivot(array,l,r):
    p = array[l]
    return p

def fucked_up_pivot(array,l,r):
    p = array[r]
    return p
    
def median_pivot(array,l,r):
    options=array[l:r+1]
    set = []
    n=len(options)
    set.append(options[0])
    if len(options)%2==0:set.append(options[(n/2)-1])
    else:set.append(options[(n-1)/2])
    set.append(options[n-1])
    set.sort()
    p=set[1]
    return p
    
def partition(array,l,r):
    p=lazy_pivot(array,l,r)
    n=r-l+1
    i=l+1
    for j in range(l,r+1):
        if array[j]<p:
            array[j],array[i] = array[i],array[j]
            i+=1
    array[l],array[i-1] = array[i-1],array[l]
    return n-1,i-1
    
def switch_partition(array,l,r):
    p=median_pivot(array,l,r)
    n=r-l+1
    ind=array.index(p)
    array[ind],array[l]=array[l],array[ind]
    i=l+1
    for j in range(l,r+1):
        if array[j]<p:
            array[j],array[i] = array[i],array[j]
            i+=1
    array[l],array[i-1] = array[i-1],array[l]
    return n-1,i-1

def quick_sort(array,l,r):
    n=r-l+1
    if n>1:
        num,i=switch_partition(array,l,r)
        if i!=0:
            a=quick_sort(array,l,i-1)
            num+=a
        if i!=len(array)-1:
            b=quick_sort(array,i+1,r)
            num+=b
        return num
    else:
        return 0
         
array = load_array()
num = quick_sort(array,0,len(array)-1)
print num

#162085,164123,138382



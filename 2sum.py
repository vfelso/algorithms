def load_a(file):
    ints,seen = [],set()
    with open(file,'r') as f:
                for line in f:
                    x = int(line.strip())
                    if x not in seen:
                        ints.append(x)
                        seen.add(x)                       
    return sorted(ints)
def twoSum(array,b,t):
    result=set()
    n=len(array)
    l,r,top=0,n-1,n-1
    while l<n/2:
        s=array[l]+array[r]
        if s==t:
            top=r
            result.add(s)
            r-=1
        elif s<t and s>=b:
            result.add(s)
            r-=1
        elif s>t:
            r-=1
        else:
            l+=1
            print l
            r=top                
    return len(result)
                
A=load_a()
print twoSum(A,-10000,10000)
#looks good with small test case, let's optimize running time
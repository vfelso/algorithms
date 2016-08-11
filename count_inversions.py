def load_array(file):
    array = []
    with open(file,'r') as ints:
                for line in ints:
                    t = line.strip().split()
                    for x in t:
                        array.append(int(x))
    return array
    
def merge_sort(array1,array2):
    i,j,D,Z = 0,0,[],0
    B,C = array1,array2
    n=len(B)+len(C)
    for k in range(n):
        if i<len(B) and j<len(C):
            if B[i]<C[j] or B[i]==C[j]:
                D.append(B[i])
                i+=1
            else:
                D.append(C[j])
                Z += len(B)-i
                j+=1  
        else:
            if i<len(B):
                D.append(B[i])
                i+=1
            else:
                D.append(C[j])
                j+=1        
    return D,Z

def sort_and_count(array):
    n = len(array)
    if n == 1:
        return array,0
    elif n == 2:
        if array[0] > array[1]:
            return [array[1],array[0]],1
        else: return array,0
    else:
        B,X = sort_and_count(array[:n/2])
        C,Y = sort_and_count(array[n/2:])
        D,Z = merge_sort(B,C)
    return D,X+Y+Z
        
print sort_and_count(load_array())[1]
    
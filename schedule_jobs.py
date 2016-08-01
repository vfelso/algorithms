import heapq
import operator

def load_jobs(function):
    file = '/Users/vanessafelso/Documents/6.00x Files/Algorithm pt 2 1/jobs.txt'
    jobs = {}
    heap = []
    i=1
    bool=True
    count =0
    with open(file,'r') as data:
        for line in data:
            if bool==True:bool=False
            else:
                x,y = line.strip().split()
                value = function(int(x)*1.0,int(y)*1.0)
                heap.append(value)
                if value not in jobs:jobs[value]=[(int(x)*1.0,i,int(y)*1.0)]
                else:jobs[value].append((int(x)*1.0,i,int(y)*1.0))
                i+=1
                count+=1
    heap.sort(reverse=True)
    return jobs, heap    
def difference(x,y):
    value = x-y
    return value    
def ratio(x,y):
    value = x/y
    return value
    
def scheduleByDifference():
    time = 0.0
    sum = 0.0
    schedule = []
    jobs,heap =load_jobs(difference)
    while len(heap)>0:
        pending=heap.pop(0)
        sorted_by_weight = sorted(jobs[pending],key=lambda x:x[0],reverse=True)
        temp = sorted_by_weight[0]
        jobs[pending].remove(temp)
        schedule.append(temp[1])
        time+=temp[2]
        sum += time*temp[0]
    return int(sum)
def scheduleByRatio():
    sum = 0.0
    time=0.0
    schedule = []
    jobs,heap=load_jobs(ratio)
    while len(heap)>0:
        pending=heap.pop(0)
        temp = jobs[pending][0]
        jobs[pending].remove(temp)
        schedule.append(temp[1])
        time+=temp[2]
        sum += time*temp[0]
    return int(sum)
   
print scheduleByDifference()
print scheduleByRatio()

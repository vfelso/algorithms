import matplotlib.pyplot as plt
import itertools
from math import *

def nodes(num,n):
    list=[1]
    node=2
    while node<n+1:
        if num^(2**(n-node))<num:
            num=num^(2**(n-node))
            list.append(node)
            node+=1
        else:
            node+=1
    return list
                
class Graph(object):
    def __init__(self):
        file = '/Users/vanessafelso/Documents/6.00x Files/Algorithm pt 2 5/tsp.txt'
        self.coordinates={}
        self.cost={}
        bool=True
        i=1
        with open(file,'r') as graph:
            for line in graph:
                if bool==True:bool=False
                else:
                    x,y = line.strip().split()
                    self.coordinates[i]=[float(x),float(y)]
                    i+=1
    def load_edges(self):
        seen=set()
        for i in range(1,26):
            for j in range(1,26):
                if i != j:
                    if (i,j) not in seen:
                        x,y=self.coordinates[i]
                        z,w=self.coordinates[j]
                        cost=self.euclid(x,y,z,w)
                        self.cost[i,j]=cost
                        seen.add((i,j))
                else:
                    self.cost[i,j]=float("inf")
    def plot_tour(self,tour):
        for i in range(len(tour)-1):
            x,y=self.coordinates[tour[i]]
            z,w=self.coordinates[tour[i+1]]
            plt.plot([x,z],[y,w])
        plt.scatter(*zip(*self.coordinates.values()))
        plt.show()
    def euclid(self,x,y,z,w):
        return sqrt(((x-z)**2)+((y-w)**2))
    def tour_len(self,list):
        cost=0
        for i in range(len(list)-1):
            cost+=self.cost[list[i],list[i+1]]
        return cost
    def perms(self,list):
        s,e=list[0],list[0]
        mid=list[1:]
        min,x=None,None
        for x in set(itertools.permutations(mid,24)):
            temp=[s]
            for y in x:
                temp.append(y)
            temp.append(e)
            cost=self.tour_len(temp)
            if min==None or cost<min:
                min=cost
                x=temp
        return min,x      
    def S(self,m,n):
        if m==1:
            return 0
        else:
            m=m-1
            bits=[]
            for combo in itertools.combinations(range(1,n),m):
                bit=0
                for i in combo:
                    bit=bit|2**(n-(i+1))
                bits.append(bit)
            return bits     
    def TSP(self,n):
        b=1
        A = {(0,b):0}
        for m in range(2,n+1):
            for s in self.S(m,n):
                l=nodes(s,n)
                for j in l:
                    if j==b:
                        pass
                    else:
                        min=None
                        for k in l:
                            if k==j:
                                pass
                            else:
                                if min==None or (A.get((s^2**(n-j),k),float("inf"))+self.cost[k,j])<min: 
                                    min=(A.get((s^2**(n-j),k),float("inf"))+self.cost[k,j])
                        A[s,j]=min 
        s=self.S(n,n).pop() 
        l=nodes(s,n)         
        min=None
        for j in l:
            if j==b:
                pass
            else:
                if min==None or (A.get((s,j),float("inf"))+self.cost[j,b])<min:
                     min=(A.get((s,j),float("inf"))+self.cost[j,b])  
        return min
        
graph=Graph()
graph.load_edges()
#print graph.TSP(20)

#[13, 14, 16, 24, 25, 20, 17, 21, 23, 22, 18, 19, 15, 12, 11, 10, 6, 2, 1, 5, 8, 4, 3, 7, 9, 13]
#26442   
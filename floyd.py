import numpy

class Graph(object):
    def __init__(self,file):
        self.G=[];self.weights={};b=True
        for x in range(1,1002):
            self.G.append([])
        with open(file,'r') as graph:
            for line in graph:
                if b==True: b=False
                else:
                    x,y,z = line.strip().split()
                    self.G[int(x)].append((int(z),int(y)))
                    self.weights[(int(x),int(y))]=int(z)
    def floyd(self):
        min=float("inf")
        dist = [[float("inf") for x in range(1002)] for y in range(1002)] 
        for u in range(1,1001):
            for v in range(1,1001):
                if u==v: dist[u][v]=0
                elif (u,v) in self.weights: 
                    dist[u][v]=self.weights[(u,v)]
                    if self.weights[(u,v)]<min:
                        min=self.weights[(u,v)]
        for k in range(1,1001):
            for i in range(1,1001):
                for j in range(1,1001):
                    if dist[i][j]>dist[i][k]+dist[k][j]:
                        dist[i][j]=dist[i][k]+dist[k][j] 
                        if dist[i][j]<min:
                            min=dist[i][j]
        print min 
        print self.check(dist) 
    def check(self,dist):
        for i in range(1,1002):
            if dist[i][i]<0:
                return 'Oh shit'
        return 'oh good'
                                  
#g1=Graph('/Users/vanessafelso/Documents/6.00x Files/Algorithm pt 2 4/g1.txt') #Nope, negative cycle found
#g2=Graph('/Users/vanessafelso/Documents/6.00x Files/Algorithm pt 2 4/g2.txt') #Nope, negative cycle found
g3=Graph('/Users/vanessafelso/Documents/6.00x Files/Algorithm pt 2 4/g3.txt')
#test=Graph('/Users/vanessafelso/Documents/6.00x Files/Algorithm pt 2 4/test.txt')
g3.floyd()

#-19
from heapq import *

class Graph(object):
    def __init__(self):
        file='/Users/vanessafelso/Documents/6.00x Files/Algorithm 5/dijkstraData.txt'
        self.G=[];self.weights={},
        for x in range(1,202):
            self.G.append([])
        with open(file,'r') as graph:
            for line in graph:
                l = line.strip().split()
                w=int(l[0])
                for x in l[1:]:
                    v,c=x.split(',')
                    v=int(v);c=int(c)
                    self.G[w].append((c,v))
    def Dijkstra(self,s):
        q,seen=[(0,s)],set()
        D={s:0}
        while q:
            (cost,v1)=heappop(q)
            if v1 not in seen:
                seen.add(v1)
                D[v1]=cost
                for c,v2 in self.G[v1]:
                    if v2 not in seen:
                        heappush(q,(cost+c,v2))
        return D[7],D[37],D[59],D[82],D[99],D[115],D[133],D[165],D[188],D[197]

graph=Graph()
print graph.Dijkstra(1)
#2599, 2610, 2947, 2052, 2367, 2399, 2029, 2442, 2505, 3068

import random

class Graph(object):
    def __init__(self):
        file = '/Users/vanessafelso/Documents/6.00x Files/Algorithm 3/kargerMinCut.txt'
        self.edges=[]
        self.vertices={}
        self.nodes=[str(x) for x in range(1,201)]
        with open(file,'r') as graph:
                for line in graph:
                    t = line.strip().split()
                    i=True
                    for x in t:
                        if i==True:
                            u=x
                            self.vertices[u]=[]
                            i=False
                        else:
                            if (x,u) not in self.edges:
                                self.edges.append((u,x))
                            self.vertices[u].append(x)
    def contract(self,v1,v2):
        self.edges.remove((v1,v2))
        self.nodes.remove(v1)
        self.nodes.remove(v2)
        while v2 in self.vertices[v1]:
            self.vertices[v1].remove(v2)
        while v1 in self.vertices[v2]:
            self.vertices[v2].remove(v1)
        new=v1+'&'+v2
        self.nodes.append(new)
        checks=[]
        for x in self.vertices[v1]:
            checks.append(x)
        for x in self.vertices[v2]:
            checks.append(x)
        self.vertices[new]=checks
        self.vertices.pop(v1, None)
        self.vertices.pop(v2, None)
        for x in checks:
            for y in self.vertices[x]:
                if y==v1 or y==v2:
                    self.vertices[x].remove(y)
                    self.vertices[x].append(new)
                else:
                    pass 
        self.update_edges()
    def update_edges(self):
        self.edges=[]
        for x in self.nodes:
            u=x
            for v in self.vertices[u]:
                if (v,u) not in self.edges:
                    self.edges.append((u,v))
    def random_contraction(self):
        while len(self.nodes)>2:
            u,v=random.choice(self.edges)
            self.contract(u,v)
        return len(self.edges)
  
num=200                    
while num>0:
    graph=Graph()
    print graph.random_contraction()
    num-=1

#17
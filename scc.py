class Graph(object):
    def __init__(self,file):
        self.G=[]
        self.GFinish=[]
        self.GRev=[]
        self.leader={}
        self.finished={}
        for x in range(1,875716):
            self.G.append([]);self.GRev.append([]);self.GFinish.append([]);self.leader[x]=0;
        self.n=len(self.G)-1
        self.s=None
        self.t=0
        self.f={}
        with open(file,'r') as graph:
            for line in graph:
                x,y = line.strip().split()
                self.G[int(x)].append(int(y))
                self.GRev[int(y)].append(int(x))
    def DFS_Loop(self,rev=False):
        self.s=None
        for x in range(1,875716):
            self.finished[x]=False
        for i in range(self.n,0,-1):
            if self.finished[i]==False:
                self.s=i
                self.DFS_Iterative(i,rev)
    def DFS_Recursive(self,start,rev=False):
        if rev==False: G=self.GFinish
        else: G=self.GRev
        if self.finished[start]==False:
            self.finished[start]=True
        if rev==False:
            self.leader[self.s]+=1
        for x in G[start]:
            if self.finished[x]==False:
                self.DFS_Recursive(x,rev)
        self.t+=1
        self.f[start]=self.t
    def DFS_Iterative(self,start,rev=False):
        if rev==False: G=self.GFinish
        else: G=self.GRev
        stack=[start]
        while stack != []:
            v=stack.pop() 
            if self.finished[v]==False:
                self.finished[v]=True
                if rev==False:
                    self.leader[self.s]+=1
                stack.append(v)
                stack_aux=[]
                for x in G[v]:
                    if self.finished[x]==False: stack_aux.append(x)
                while len(stack_aux)>0:
                    stack.append(stack_aux.pop())     
            else:
                if v not in self.f:
                    self.t+=1
                    self.f[v]=self.t
    def update(self):
        for x in range(1,self.n+1):
            newx=self.f[x]
            for y in self.G[x]:
                newy=self.f[y]
                self.GFinish[newx].append(newy)
    def kosaraju(self):
        self.DFS_Loop(True)
        self.update()
        self.DFS_Loop()
        print self.compute_SCC()
    def compute_SCC(self):
        sccs=self.leader.values()
        sccs=sorted(sccs,reverse=True)
        return sccs[0],sccs[1],sccs[2],sccs[3],sccs[4]
            
graph=Graph()
print graph.n
#graph.kosaraju()
#434821,968,459,313,211

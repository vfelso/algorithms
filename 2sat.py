def load_file():
    #1:100000,2:200000,3:400000,4:600000,5:800000,6:1000000
    file = '/Users/vanessafelso/Documents/6.00x Files/Algorithm pt 2 6/2sat2.txt'
    #file = '/Users/vanessafelso/Documents/6.00x Files/Algorithm pt 2 6/test.txt'
    bool=False
    G={}
    GRev={}
    with open(file,'r') as f:
                    for line in f:
                        if bool==False:
                            bool=True
                        else:
                            x,y = line.strip().split()
                            x,y=int(x),int(y)
                            if x<0:newx=abs(x)
                            else: newx=-x
                            if y<0:newy=abs(y)
                            else: newy=-y
                            try:
                                G[newx].append(y)
                            except:
                                G[newx]=[y]
                            try:
                                G[newy].append(x)
                            except:
                                G[newy]=[x]
                            try:
                                GRev[y].append(newx)
                            except:
                                GRev[y]=[newx]
                            try:
                                GRev[x].append(newy)
                            except:
                                GRev[x]=[newy]
    return G,GRev
def first_pass(d):
        global s
        global finished
        finished={}
        nodes=range(-n,n+1)
        for x in nodes:
            if x != 0:
                finished[x]=False
        for i in nodes:
            if i !=0:
                if finished[i]==False:
                    s=i
                    DFS_Iterative(i,d)
def DFS_Iterative(start,G):
        global f
        global t
        global finished
        stack=[start]
        while stack != []:
            v=stack.pop() 
            if finished[v]==False:
                finished[v]=True
                try:
                    leader[s].append(v)
                except:
                    leader[s]=[v]
                stack.append(v)
                stack_aux=[]
                for x in G.get(v,[]):
                    if finished[x]==False: stack_aux.append(x)
                while len(stack_aux)>0:
                    stack.append(stack_aux.pop())     
            else:
                if v not in f:
                    t+=1
                    f[v]=t
def update(G):
    graph={}
    switch={}
    for x in range(-n,n+1):
        if x !=0:
            newx=f[x]
            for y in G.get(x,[]):
                newy=f[y]
                try:
                    graph[newx].append(newy)
                except:
                    graph[newx]=[newy]
    for x in f.keys():
        switch[f[x]]=x
    return graph,switch
def second_pass(d):
        global s
        global finished
        global leader
        leader={}
        finished={}
        nodes=range(1,(2*n)+1)
        for x in nodes:
            finished[x]=False
        for i in nodes:
            if i !=0:
                if finished[i]==False:
                    s=i
                    DFS_Iterative(i,d)
def check(leader,switch):
        sccs={}
        for x in leader.keys():
            oldx=switch[x]
            for y in leader[x]:
                oldy=switch[y]
                sccs[oldy]=oldx
        for x in range(1,n):
            if sccs[x]==sccs[-x]:
                print x
        print 'Solvable!'
        
n=200000
s=None
finished={}
leader={}
f={}
t=0
d,r=load_file()
first_pass(r)
d,switch=update(d)
second_pass(d)
check(leader,switch)
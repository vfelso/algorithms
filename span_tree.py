class Graph(object):
    def __init__(self,numberNodes):
        self.nodes={}
        self.number=numberNodes
        for x in range(numberNodes+1):
            if x !=0:
                self.nodes[x]=[]
    def addEdge(self,i,j,w):
        self.nodes[i].append((j,w))
        self.nodes[j].append((i,w))
    
def load_graph():
    file = '/Users/vanessafelso/Documents/6.00x Files/Algorithm pt 2 1/edges.txt'
    number=0
    bool=True
    with open(file,'r') as data:
        for line in data:
            if bool==True:
                x,y = line.strip().split()
                number = int(x)
                graph = Graph(number)
                bool=False
            else:
                i,j,w = line.strip().split()
                graph.addEdge(int(i),int(j),int(w)*1.0)
    return graph  
    
def PrimMST(graph):
    X=[1]
    T=[]
    sum = 0
    for x in range(10):
        while len(X)<graph.number:
            templist=[]
            tempdict={}
            #run through each node in X collecting possibilities
            for node in X:
                for edge in graph.nodes[node]:
                    if edge[0] not in X:
                        tempdict[edge[1]]=(node,edge[0])
                        templist.append(edge[1])
                    else:
                        pass
            #choose the best
            templist.sort()
            next=templist[0]
            best = (tempdict[next],next)
            #go with it
            T.append(best)
            sum+=best[1]
            if best[0][0] not in X:X.append(best[0][0]) 
            if best[0][1] not in X:X.append(best[0][1])
    return int(sum)
        
#fuckThisGraph = Graph(5)
#fuckThisGraph.addEdge(1,3,80)
#fuckThisGraph.addEdge(1,2,60)
#fuckThisGraph.addEdge(1,5,-80)
#fuckThisGraph.addEdge(5,3,30)
#fuckThisGraph.addEdge(3,4,20)
#fuckThisGraph.addEdge(2,4,50)
#fuckThisGraph.addEdge(4,2,40)
graph = load_graph() 
#print PrimMST(fuckThisGraph)
print PrimMST(graph)

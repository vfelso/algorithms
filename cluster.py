class union_find():
    def __init__ (self):
        self.groups = {}
        self.leaders = {}
        self.k = 0
        for v in range(1,501):
            leader = v
            group_vertices = [v]
            size = 1
            self.groups[v] = (leader, group_vertices, size)
            self.leaders[v] = v
            self.k += 1
    def find (self, vertex):
        return self.leaders[vertex]
    def union (self, group1, group2):
        leader1, vertices1, size1 = self.groups[group1]
        leader2, vertices2, size2 = self.groups[group2]

        if size1 > size2:
            new_leader = leader1
            smaller_vertices = vertices2
            bigger_vertices = vertices1
            smaller_group = group2
            bigger_group = group1
        else:
            new_leader = leader2
            smaller_vertices = vertices1
            bigger_vertices = vertices2
            smaller_group = group1
            bigger_group = group2

        for vertex in smaller_vertices:
            # Add vertices of smaller group to bigger group
            bigger_vertices.append(vertex)
            # Update leader of moved vertices
            self.leaders[vertex] = new_leader
        # Discard smaller group
        self.groups.pop(smaller_group)
        # Update bigger group
        self.groups[bigger_group] = (new_leader, bigger_vertices, size1 + size2)
        # Lower cluster count
        self.k -= 1

class Graph(object):
    def __init__(self,file):
        self.G=[[]]*500
        self.edges=[]
        bool=True
        with open(file,'r') as graph:
            for line in graph:
                if bool==True:bool=False
                else:
                    x,y,z = line.strip().split()
                    self.edges.append([int(z),int(x),int(y)])
                    self.G[int(x)].append((int(z),int(y)))
    def kruskall(self):
        sorted_edges=sorted(self.edges)
        uf = union_find()
        for (z,u,v) in sorted_edges:
            group_u=uf.find(u)
            group_v=uf.find(v)
            if group_u!=group_v:
                if uf.k==4:
                    return z
                uf.union(group_u,group_v)
        return 'uh oh'

graph = Graph()
print graph.kruskall()
#106

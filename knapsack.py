import sys

sys.setrecursionlimit(150000)

class Knapsack(object):
    def __init__(self):
        self.values=[0]
        self.weights=[0]
        self.A={}
        file = '/Users/vanessafelso/Documents/6.00x Files/Algorithm pt 2 3/knapsack_big.txt'
        b=True
        with open(file,'r') as sack:
            for line in sack:
                if b==True:
                    x,y=line.strip().split()
                    self.W=int(x)
                    self.n=int(y)
                    b=False
                else:
                    x,y = line.strip().split()
                    self.values.append(int(x))
                    self.weights.append(int(y))     
    def clever_thief(self):
        A={}
        for x in range(self.W+1):
            A[0,x]=0
        for i in range(1,self.n+1):
            for x in range(self.W+1):
                if self.weights[i]>x:
                    A[i,x]=A[i-1,x]
                else:
                    A[i,x]=max((A[i-1,x]),(A[i-1,x-self.weights[i]]+self.values[i]))
        return A[self.n,self.W]
    def loop(self):
        self.A={}
        print self.recursive_thief(self.n,self.W)
    def recursive_thief(self,n, W):
        if n == 0:
            return 0
        if n not in self.A:
            self.A[n] = {}
        if W not in self.A[n]:
            if self.weights[n]>W:
                solution = self.recursive_thief(n - 1, W)
            else:
                solution = max(self.recursive_thief(n - 1, W),
                            self.recursive_thief(n - 1, W - self.weights[n]) + self.values[n])
            self.A[n][W] = solution
        else:
            solution = self.A[n][W]
        return solution
        
k=Knapsack()
print k.loop()

#4243395
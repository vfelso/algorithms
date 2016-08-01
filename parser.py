#parse input sentences
import csv
import math
import json

def load_text(fileName):
    file = '/Users/vanessafelso/Documents/6.00x Files/NLP 2/' + str(fileName)
    return file         
#First let's create our model with storage for nonterminal counts, binary rules and counts, unary rules and counts, and words
class PCFG(object):
    def __init__(self, file):
        self.nonterms = {}
        self.unaries = {}
        self.binaries = {}
        self.words = {}
        with open(file,'r') as counts:
            print 'Populating our model with counts...'
            for line in counts:
                t = line.strip().split()
                count = int(t[0])*1.0
                key = tuple(t[2:])
                if t[1] == 'NONTERMINAL':
                    self.nonterms[key] = count
                elif t[1] == 'UNARYRULE':
                    self.unaries[key] = count
                    word = t[3]
                    if word in self.words:
                        self.words[word] += count
                    else: self.words[word] = count
                elif t[1] == 'BINARYRULE':
                    self.binaries[key] = count
        self.vocab_count=len(self.words)
    def nontermCount(self,x):
        nonterm = (x,)
        if nonterm in self.nonterms: return self.nonterms[nonterm]
        else: return 0.0
    def unaryProb(self,x,y):
        unary = (x,y)
        nonterm = x
        if unary in self.unaries:
            unaryCount=self.unaries[unary]
            nontermCount=self.nontermCount(nonterm)
            return unaryCount / nontermCount
        else: return 0.0
    def binaryProb(self,x,y,z):
        binary = (x,y,z)
        if binary in self.binaries:
            binaryCount=self.binaries[binary]
            nontermCount=self.nontermCount(x)
            return binaryCount / nontermCount
        else: return 0.0
    def is_rare_word(self,word):
        if word in self.words:
            return self.words[word] <5
        else: return True

#time to implement the CKY algorithm
def argmax(ls):
    if not ls: return None, 0.0
    return max(ls, key = lambda x:x[1])
def cky_parse(sentence,pcfg):
    n = len(sentence)
    N = []
    for x in pcfg.nonterms.keys():
        N.append(x[0])
    x = [""] + sentence
    #return possibilities that could be under a given X 
    def R(X):
        possibilities = []
        for x in pcfg.binaries:
            if x[0] == X:
                possibilities.append((x[1],x[2]))
        return possibilities
    #small prob. calculations
    def q2(x,y,z): return pcfg.binaryProb(x,y,z)
    def q1(x,y): return pcfg.unaryProb(x,y)
    #create dynamic tables
    pi = {}
    bp = {}
    for i in range(n-1):
        for X in N:
            if (X,x[i]) in pcfg.unaries:
                pi[i,i,X] = q1(X,x[i])
                bp[i,i,X] = (X,x[i],i,i)
    for l in range(1,n):
        for i in range(1,n-l+1):
            j = i+l
            for X in N:
                back,score = argmax([((X,Y,Z,i,s,j),(q2(X,Y,Z)*pi[i,s,Y]*pi[s+1,j,Z])) for s in range(i,j) for (Y,Z) in R(X) if pi.get((i,s,Y),0.0)>0.0 if pi.get((s+1,j,Z),0.0)>0.0])
                if score != 0.0: 
                    bp[i,j,X], pi[i,j,X] = back,score
    print pi
    if (1,n,"SBARQ") in pi:
        tree = backtrace(bp[1,n,"SBARQ"],bp)
        score = pi.get((1,n,"SBARQ"))
        return tree, score
def backtrace(back,bp):
    if not back: return None
    if len(back) == 6:
        (X,Y,Z,i,s,j) = back
        return [X,backtrace(bp[i,s,Y],bp),backtrace(bp[s+1,j,Z],bp)]
    else:
        (X,Y,i,i) = back
        return[X,Y]
    
def replace_rare_words(sentence,pcfg):
    return [word if not pcfg.is_rare_word(word) else "_RARE_" for word in sentence]
def parse_text(fileName,pcfg):
    file = '/Users/vanessafelso/Documents/6.00x Files/NLP 2/' + str(fileName)
    final = []
    for i,l in enumerate(open(file)):
        line = l.strip().split()
        sentence = replace_rare_words(line,pcfg)
    #    tree,score = cky_parse(sentence,pcfg)
    #    final.append(json.dumps(tree))                
    #with open("parsed_dev.dat", "wb") as parsed:
    #    for x in final:
    #        print>>parsed, x

#create a new file of training trees with _RARE_ replacing rare words
def replace_trees(pcfg):
    file = '/Users/vanessafelso/Documents/6.00x Files/NLP 2/parse_train.dat'
    final = []
    with open(file,'r') as train:
        for line in train:
            tree = json.loads(line.strip())
            replace_rare(pcfg,tree)
            line = json.dumps(tree)
            final.append(line)
    with open("newparse_train.dat", "wb") as newtrain:
        for x in final:
            print>>newtrain, x 
def replace_rare(pcfg,tree):
    if len(tree) == 3:
        replace_rare(pcfg, tree[1])
        replace_rare(pcfg,tree[2])
    elif len(tree) == 2:
        if pcfg.is_rare_word(tree[1]): tree[1] = "_RARE_"
                        
text = load_text('cfg.counts')
model = PCFG(text)
cky_parse(['What', 'was', 'the', '_RARE_', '?'],model)
#parse_text('parse_dev.dat',model)
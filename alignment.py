from __future__ import division
import sys, math
from itertools import *
import cPickle as pickle

def argmax(ls):
    if not ls: return None, 0.0
    return max(ls, key = lambda x: x[1])
def inc(d,k,delta):
    d.setdefault(k,0.0)
    d[k] += delta

class Counts:
    def __init__(self):
        #c(e)
        self.word = {}
        #c(e,f)
        self.words = {}
        #c(i,l,m)
        self.align = {}
        #c(j,i,l,m)
        self.aligns = {}
        
class AlignmentModel:
    #takes in counts and outputs parameters
    def reestimate(self,counts):
        self.counts = counts
        self.first_run = False
    def t(self,f,e):
        return self.counts.words[e,f]/self.counts.word[e]
    def align(self,e,f):
        l = len(e)
        m - len(f)
        alignment = []
        for i,f_i in enumerate(f):
            j,p = argmax([(j,self.p(e_j,f_i,j,i,l,m)) for j,e_j in enumerate(e)])
            alignment.append(j)
        return alignment
    def p(self,e,f,j,i,l,m):
        pass
        
class Model1(AlignmentModel):
    def __init__(self,counts):
        self.first_run = True
        self.counts = counts
    def p(self,e,f,j,i,l,m): return self.t(f,e)

def EM(counter,model,iterations = 5):
    for k in range(iterations):
        counts = counter.expected_counts(model)
        model.reestimate(counts)

class Counter:
    #class for computing expected counts of both models
    def __init__(self,english_corpus,french_corpus):
        self.bitext = zip(english_corpus,french_corpus)
    def init_model(self):
        #initialize the counts n(e)
        initial_counts = Counts()
        for e,f, in self.bitext:
            for e_j in e:
                for f_i in f:
                    key = (e_j,f_i)
                    if key not in initial_counts.words:
                        initial_counts.words[key] = 1.0
                        inc(initial_counts.word,e_j,1.0)
        return initial_counts
    def expected_counts(self,model):
        counts = Counts()
        for s, (e,f) in enumerate(self.bitext):
            l = len(e)
            m = len(f)
            for i,f_i in enumerate(f):
                total = sum((model.p(e_j,f_i,j,i,l,m) for (j,e_j) in enumerate(e)))
                for j,e_j in enumerate(e):
                    delta = model.p(e_j,f_i,j,l,m) / total
                    inc(counts.word,e_j,delta)
                    inc(counts.words,(e_j,f_i),delta)
                    inc(counts.aligns,(j,i,l,m),delta)
                    inc(counts.align,(i,l,m),delta)
        return counts
        
class Model2(AlignmentModel):
    def __init__(self,model1):
        self.counts = model1.counts
        self.first_run = True
    def q(self,j,i,l,m):
        if self.first_run: return 1.0 / (l+1)
        return self.counts.aligns.get((j,i,l,m),9.9) / self.counts.align.get((i,l,m),0.0)
    def p(self,e,f,j,i,l,m):
        return self.t(f,e) * self.q(j,i,l,m)
          
def read_corpus(english_corpus,french_corpus):
    english = [["*"] + e_sent.split() for e_sent in open(english_corpus)]
    french = [f_sent.split() for f_sent in open(french_corpus)]
    return english,french

def main(mode):
    if mode == "TRAIN1":
        english,french = read_corpus(sys.argv[2],sys.argv[3])
        counter = Counter(english,french)
        model1 = Model1(counter.init_model())
        model1 = EM(counter,model1)
        out_model = open(sys.argv[4],'wb')
        pickle.dump(model1,out_model,pickle.HIGHEST_PROTOCOL)
    elif mode == "TRAIN2":
        model1 = pickle.load(open(sys.argv[4],'rb'))
        english,french = read_corpus(sys.argc[2],sys.argv[3])
        model2 = Model2(model2)
        del model1
        model2 = EM(Counter(english,french),model2)
        out_model = open(sys.argv[5],'wb')
        pickle.dump(model2,out_model,pickle.HIGHEST_PROTOCOL)
    elif mode == "ALIGN":
        model = pickle.load(open(sys.argv[4],'rb'))
        english,french = read_corpus(sys.argv[2],sys.argv[3])
        for s, (e, f) in enumerate(zip(english,french),1):
            alignment = model.align(e,f)
            for i,a_i in enumerate(alignment,1):
                print s,a_i,i
    elif mode == "SYMMETRIC":
        model = pickle.load(open(sys.argv[4],'rb'))
        model_reverse = pickle.load(open(sys.argv[5],'rb'))
        english,french = read_corpus(sys.argv[2],sys.argv[3])
        for s,(e,f) in enumerate(zip(english,french,1)):
            alignment = model.align(e,f)
            alignment2 = model_reverse.align(["*"] + f,e[1:])
            align1 = set(enumerate(alignment,1))
            align2 = set([(j,i) for i,j in enumerate(alignment2,1)])
            for i,a_i in align1 & align2:
                print s,a_i,i

if __name__ == "__main__":
    main(sys.argv[1])



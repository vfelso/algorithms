import csv
import math

def load_text(fileName,directory):
    file = str(directory) + str(fileName)
    return file         
def vocab_count(input):
    count = 0
    for x in input:
        count +=1
    return count*1.0  
def sort(word):
    if any([c.isdigit() for c in word]): 
        word = '_DIGITS_'
    elif all([c.isupper() for c in word]): 
        word = '_ALLCAP_'
    elif word[-1].isupper(): 
        word = '_LASTCAP_'
    else:
        word = '_RARE_'
    return word
    
#First let's create our model with all values for emissions, trigrams, bigrams, unigrams
class HMM(object):
    def __init__(self, file):
        self.emissions = {}
        self.trigrams = {}
        self.bigrams = {}
        self.unigrams = {}
        with open(file,'r') as counts:
            print 'Creating our model with gene counts...'
            for line in counts:
                t = line.strip().split()
                count = int(t[0])
                key = tuple(t[2:])
                if t[1] == 'WORDTAG':
                    self.emissions[key] = count
                elif t[1] == '3-GRAM':
                    self.trigrams[key] = count
                elif t[1] == '2-GRAM':
                    self.bigrams[key] = count
                elif t[1] == '1-GRAM':
                    self.unigrams[key[0]] = count
    def unigramCount(self,y):
        return self.unigrams[y]
    def trigramProb(self,w,w1,w2):
        trigram = (w,w1,w2)
        bigram = (w,w1)
        trigramCount=self.trigrams[trigram]*1.0
        bigramCount=self.bigrams[bigram]*1.0
        return trigramCount / bigramCount
    def emissionProb(self,x,y):
        num = 0
        if y in ["*","STOP"]: return 1.0
        if ('O',x) not in self.emissions and ('I-GENE',x) not in self.emissions:
            x = sort(x)
        try:
            num = self.emissions[(y,x)]
        except:
            num = 0
        ycount = self.unigramCount(y)
        return num*1.0 / ycount*1.0
def argmax(ls):
    return max(ls, key = lambda x:x[1])                                              
#tag a file using various algorithms, creating an output file with the tagged version
def tag(word,taggingModel):
    probYes = taggingModel.emissionProb(word,'I-GENE')
    probNo = taggingModel.emissionProb(word,'O')
    newline = [word]
    if probYes > probNo:
        tagging = 'I-GENE'
    else:
        tagging = 'O'
    return tagging 
def viterbi_tag(sentence,taggingModel):
    n = len(sentence)
    #return tag options for each position called k
    def K(k):
        if k in (-1,0): return ["*"]
        else: return ['O','I-GENE'] 
    #x is our new variable for sentence. It is has a position 0 that is empty. Y is our new variable for tags. It has the same length as x.
    x = [""] + sentence
    y = [""] * (n+1)
    #does small prob. calculations
    def q(w,u,v): return taggingModel.trigramProb(u,v,w)
    def e(x,u): return taggingModel.emissionProb(x,u)
    #create dynamic tables for pi(max) and bp(arg max)
    pi = {}
    pi[0,"*","*"] = 1.0
    bp = {}
    for k in range(1,n+1):
        for u in K(k-1):
            for v in K(k):
                bp[k,u,v],pi[k,u,v] = argmax([(w,pi[k-1,w,u]*q(v,w,u)*e(x[k],v)) for w in K(k-2)])
    (y[n-1],y[n]), score = argmax([((u,v), pi[n,u,v]*q("STOP",u,v)) for u in K(n-1) for v in K(n)])
    #traversing through all ks asserting that its tag is the best tag according to bp
    for k in range(n-2,0,-1):
        y[k] = bp[k+2,y[k+1],y[k+2]]
    y[0] = "*"
    scores = [pi[i,y[i-1],y[i]] for i in range(1,n)]
    return y[1:n+1]
            
def tag_text(fileName,taggingModel):
    file = '/Users/vanessafelso/Documents/6.00x Files/NLP 1/' + str(fileName)
    final = []
    with open(file,'r') as input:
            sentence = []
            for line in input:
                if line.strip():
                    sentence.append(line.strip())   
                else:
                    tagging = viterbi_tag(sentence,taggingModel)
                    zipped = zip(sentence,tagging)
                    for x in zipped:
                        final.append(x)
                    final.append([]) 
                    sentence = []                 
    with open("gene.tagged", "wb") as tagged:
        for x in final:
            if x!= []:
                tagged.write(str(x[0])+" "+str(x[1]) + "\n")
            else:
                tagged.write("\n")

text = load_text('newgene.counts')
model = HMM(text)
vocabCount = vocab_count(model.emissions)
tag_text('gene.dev',model)
import nltk
from nltk.corpus import wordnet
import inflect
import operator

inflect = inflect.engine()


class Aspect:
    #Aspect_list=list()

    def __init__(self, reviews):
        self.reviews = reviews

    def findMax(self,dic):
        maxSoFar = 0
        word = ""
        for i in dic.keys():
            if(dic[i] > maxSoFar):
                maxSoFar = dic[i]
                word = i

        del dic[word]
        return word


    def filter_nouns(self,all_nouns):
        d=dict()
        numberAspects = 10
        Aspect_list_Filterd=[]
        for i in range(len(all_nouns)):
            d[all_nouns[i]]=0

        for j in range(len(all_nouns)):
           #if all_nouns[j] in d:
            d[all_nouns[j]] += 1

        for i in range(numberAspects):
            word = self.findMax(d)
            while inflect.plural(word) in Aspect_list_Filterd:
                word = self.findMax(d)
            Aspect_list_Filterd.append(word)

        return Aspect_list_Filterd

    def extract_aspects(self):
        #d=dict()
        #t=tuple()
        all_nouns=[]
        for w in self.reviews:
           tokens=nltk.word_tokenize(w)
           tokens_Filterd=nltk.pos_tag(tokens)
           for i in range(len(tokens_Filterd)):
               t=tokens_Filterd[i]
               if (t[1]=="NN" or t[1]=="NNS") and t[0]!="i":
                   all_nouns.append(t[0])
        Aspect_list_Filterd = self.filter_nouns(all_nouns)
        return Aspect_list_Filterd

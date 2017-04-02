from nltk.corpus import stopwords
import  nltk

from aspectExtractor import Aspect
from nltk.corpus import wordnet
class biword:

    def __init__(self,all_rev):
      self.all_rev=all_rev
      self.aspectphrase=[]
      self.newaspects=[]
      self.aspectsphrase=[]
      self.aspect_list=[]

    def num_aspect_phrase(self,phrase,listAspect_phrase):
        num = 0
        for aspect in listAspect_phrase:
            if aspect == phrase:
                num = num + 1
        return num


    def CheckAspect(self, str):
        check = 0
        for i in self.aspect_list:
            if i == str[0] or i == str[1]:
                check += 1
            if check == 2:
                break
        if check == 2:
            return True


    def leaves(self,tree):
      for subtree in tree.subtrees(filter=lambda t: t.label() == 'biWord'):
        yield subtree.leaves()


    def get_terms(self,tree):
       terms =self.leaves(tree)
       for term in terms:
          self.aspectphrase.append(term)

    def checkSimilarity(self,AspectName, word):
        for syn in wordnet.synsets(AspectName):
            for syn2 in wordnet.synsets(word):
                result = syn.wup_similarity(syn2)
                if result is None:
                    result = 0
                if (result >= 0.7):
                    return True
        return False
    def Extract(self):
       for rev in self.all_rev:
          rev_text=nltk.word_tokenize(rev)
          pos_tagged=nltk.tag.pos_tag(rev_text)
          grammer="biWord:{<NN><NN>}"
          chunker=nltk.RegexpParser(grammer)
          tree=chunker.parse(pos_tagged)
          self.get_terms(tree)

       for ap in self.aspectphrase:
          sentence = ""
          for wordtaged in ap:
            sentence+=wordtaged[0]+" "
          self.aspectsphrase.append(sentence)
       self.aspect = Aspect(self.all_rev)

       aspect_list_tmp = self.aspect.extract_aspects()

       aspect_list_tmp_2=[]
       for aspect_f in aspect_list_tmp:
           aspect_list_tmp_2.append(aspect_f)

      

       for asp in aspect_list_tmp_2:
           mainaspect=self.aspect.findMax(aspect_list_tmp)
           if self.checkSimilarity(mainaspect,asp):
               self.aspect_list.append(asp)

       print(self.aspect_list)

       for aspectp in self.aspectsphrase:
          for aspect in self.aspect_list:
             if aspect in aspectp:
                 self.newaspects.append(aspectp)

       for a in self.newaspects:
        aspect = a.split(" ")
        if (self.CheckAspect(aspect) == True):
             freq = float(self.num_aspect_phrase(a,self.newaspects))
             num_1 =float(aspect_list_tmp[aspect[0]])
             num_2 =float(aspect_list_tmp[aspect[1]])
             total = num_1 + num_2
             result=float(freq/(total))
             if result >= 0.3:
              self.aspect_list.remove(aspect[0])
              self.aspect_list.remove(aspect[1])
              self. aspect_list.append(a)

       return self.aspect_list

from nltk.corpus import stopwords
from textblob import TextBlob
import nltk

from senti_words import pos_words,neg_words


class Analyser:
    def __init__(self, reviews_list,aspects_list):
        self.reviews = reviews_list
        self.aspects=aspects_list
        self.pos=pos_words
        self.neg=neg_words
        self.dict = {}
        self.nounphrases = []
        self.newlisttagged=[]
        self.stopwords = stopwords.words('english')

    def leaves(self, tree):
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
            yield subtree.leaves()

    def get_terms(self, tree):
        terms = self.leaves(tree)
        for term in terms:
            self.nounphrases.append(term)


    def analyse_reviews(self):
        for i in self.aspects:
            self.dict[i] = {"pos": 0, "neg": 0}
        self.stopwords.remove('very')
        self.stopwords.remove('but')
        self.stopwords.remove('and')
        self.stopwords.remove('not')
        self.stopwords.append(')')
        self.stopwords.append('(')
        self.stopwords.append('.')
        self.stopwords.append(':')
        self.stopwords.append('-')
        stopwordstagged = nltk.tag.pos_tag(self.stopwords)




        for rev in  self.reviews:
            text = nltk.word_tokenize(rev)
            tagged = nltk.tag.pos_tag(text)
            for taggedstopword in stopwordstagged:
                for textword in tagged:
                    if taggedstopword[0] == textword[0]:
                        tagged.remove(textword)
            self.newlisttagged.append(tagged)


        for newtagged in self.newlisttagged:

                self.nounphrases = []


                grammer = """NP:
                                  {<IN>*<VB.*>+<NN.*>+<CC>+<NN.*>+}
                                  {<NN.*>+<JJ.*>+<CC>*<JJ.*>+}
                                  {<IN>*<NN.*>*<CC>*<VB.*>*<RBR>*<JJ.*>*<NN.*>*<RB>*<JJ.*>*<CD>*<NN.*>*<VB.*>*<RB>*<NN.*>*}
                """
                chunker = nltk.RegexpParser(grammer)
                tree = chunker.parse(newtagged)
                self.get_terms(tree)


                for nounphrase in self.nounphrases:
                    ArrOfAspects = []
                    s=sentence=noun=""
                    for taggedword in nounphrase:

                        sentence+=taggedword[0]+" "

                    for aspect in self.aspects:
                        aspect_split=aspect.split()
                        if len(aspect_split)<2:
                          if aspect in sentence:
                            ArrOfAspects.append(aspect)
                        else:
                            for a in aspect_split:
                                if a in sentence:
                                    ArrOfAspects.append(aspect)
                                    break



                    if len(ArrOfAspects)!=0:

                        textblob = TextBlob(sentence)

                        if textblob.sentiment.polarity > 0.1 and "n't" in sentence:
                            for aspect in ArrOfAspects:
                                self.dict[aspect]['neg'] += 1
                        elif textblob.sentiment.polarity < -0.1 and "n't" in sentence:
                            for aspect in ArrOfAspects:
                                self.dict[aspect]['pos'] += 1

                        elif textblob.sentiment.polarity > 0.1:
                           for aspect in ArrOfAspects:
                             self.dict[aspect]['pos'] += 1

                        elif textblob.sentiment.polarity < 0.0:
                            for aspect in ArrOfAspects:
                                self.dict[aspect]['neg'] += 1


                        elif textblob.sentiment.polarity == 0.0:
                              if "n't" not in sentence:
                                sentence=sentence.split(' ')
                                for word in sentence:
                                     if word in self.pos:
                                         for aspect in ArrOfAspects:
                                           self.dict[aspect]['pos'] += 1
                                     elif word in self.neg:
                                         for aspect in ArrOfAspects:
                                            self.dict[aspect]['neg'] += 1

                              elif  "n't" in sentence:
                                  sentence = sentence.split(' ')
                                  for word in sentence:
                                      if word in self.pos:
                                          for aspect in ArrOfAspects:
                                              self.dict[aspect]['neg'] += 1
                                      elif word in self.neg:
                                          for aspect in ArrOfAspects:
                                              self.dict[aspect]['pos'] += 1
        return self.dict

from nltk.corpus import stopwords
from textblob import TextBlob
import nltk
import inflect
from senti_words import pos_words,neg_words

inflect = inflect.engine()
class Analyser:
    def __init__(self, reviews_list,aspects_list):
        self.reviews = reviews_list
        self.aspects=aspects_list
        self.pos=pos_words
        self.neg=neg_words
        #self.aspects_list_dictionary=aspect_list_dictionary
        self.dict = {}
        self.p=0
        self.n=0
        self.newlisttagged=[]
        self.nounphrases = []
        self.stopwords = stopwords.words('english')
    def leaves(self,tree):
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
            yield subtree.leaves()

    def get_terms(self,tree):
        terms = self.leaves(tree)
        for term in terms:
             self.nounphrases.append(term)


    def analyse_reviews(self):
        for i in self.aspects:
            self.dict[i] = {"pos": 0, "neg": 0}

        self.stopwords.remove('very')
        self.stopwords.remove('but')
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
                                  {<NN.*>+<JJ.*>+<CC>+<JJ.*>+}
                                  {<IN>*<NN.*>*<VB.*>*<JJ.*>*<NN.*>*<RB>*<JJ.*>*<CD>*<NN.*>*<VB.*>*<RB>*<NN.*>*}
                """
                chunker = nltk.RegexpParser(grammer)
                tree = chunker.parse(newtagged)
                self.get_terms(tree)
                for nounphrase in self.nounphrases:
                    sentence = ""
                    sentence_word = []
                    noun = ""
                    adj = ""
                    verp = ""
                    for taggedword in nounphrase:
                        if 'NN' in taggedword[1]:
                            for aspect in self.aspects:
                                if taggedword[0] == aspect:
                                    noun += aspect + '$'
                        elif 'JJ' in taggedword[1] or 'JJS' in taggedword[1] or 'JJR' in taggedword[1]:
                            adj += taggedword[0] + '%'
                        elif 'VBP' in taggedword[1] or 'VBD' in taggedword[1] or 'IN' in taggedword[1]:
                            verp = taggedword[0]
                        sentence += taggedword[0] + " "
                        sentence_word.append(taggedword[0])
                    nounss = noun.split('$')
                    enter = False
                    for nound in nounss:
                        for aspect in self.aspects:

                            if nound == aspect:
                                textblob = TextBlob(sentence)
                                if textblob.sentiment.polarity > 0.1:
                                    self.dict[nound]['pos'] += 1
                                elif textblob.sentiment.polarity < 0.0:
                                    self.dict[nound]['neg'] += 1
                                elif textblob.sentiment.polarity == 0.0:
                                    for pos_word in self.pos:
                                        for word in sentence_word:
                                            if (pos_word == word):
                                                self.dict[nound]['pos'] += 1
                                                enter=True
                                                break
                                    if enter==False:
                                     for neg_word in self.neg:
                                        for word in sentence_word:
                                            if (neg_word == word):
                                                self.dict[nound]['neg'] += 1
                                                break


        for j in self.aspects:
            total = self.dict[j]["pos"] + self.dict[j]["neg"]
            if (total != 0):
                pos_per = round((self.dict[j]["pos"] / total) * 100, 2)
                neg_per =  round((self.dict[j]["neg"] / total) * 100, 2)
        return self.dict

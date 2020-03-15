from nltk.corpus import words

class Spelling_Bee():
    
    def __init__(self, characters, center):
        
        self.characters = characters
        self.center = center
        self.load_corpus()
        self.losers = []
        print(f'Current size of corpus: {len(self.word_list)}')
        
        
    def load_corpus(self):
        f = open('words_alpha.txt', 'r')
        x = f.readlines()
        f.close()
        
        corpus = []
        for word in x:
            corpus.append(word.strip('\n'))
            
        self.word_list = corpus     
        
    def remove_short_words(self):
        for i,word in enumerate(self.word_list):
            if len(word) < 4:
                self.losers.append(i)
                
        print(len(self.word_list))
    def remove_non_center_words(self):
        for i,word in enumerate(self.word_list):
            if self.center not in word:
                self.losers.append(i)
        #print(len(self.word_list))
              
    def check_corpus(self):       

 

        for i, word in enumerate(self.word_list):
            #print(word)
            for letter in list(word):
                if letter not in self.characters:
                    self.losers.append(i)

                    break
                else:
                    continue
        winners = []

        for i in range(len(self.word_list)):
            if i not in self.losers:
                winners.append(self.word_list[i])
        
        return winners

        
    def word_possible(self, word):
        for letter in list(word):
            if letter not in self.characters:
                #print(letter)
                return False
        return True


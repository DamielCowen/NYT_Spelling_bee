"""
Created on Thu Jun 11 15:43:20 2020

@author: drahcir1
"""

# imports for getting gameData
from lxml import html
import requests, time, json 

#import nltk
#nltk.download('words')

# list of complete english language words
from nltk.corpus import words

#import Trie.py
from trie import Trie, TrieNode


class Spelling_Bee():
    
    def __init__(self):
        start = time.time()
        self._getGameData()
        self._loadCorpus()
        self._processCorpus()
        end = time.time()
        print(end-start, self.corpus_size)
        
    def _loadCorpus(self):
 
        self.corpus = words.words()
        self.corpus_size = len(self.corpus)
        self._shortWordsRemoved = False
        self._capitalsRemoved = False
        self._corpusSearched = False
        self._includesCenter = False
    
        
        
    def _processCorpus(self):
        #lowers case
        self._removeCapitals()
        #remove short words
        self._removeShortWords()
        self._searchCorpus()
        self._checkForCenter()
       
        #remove words that do not contain center letter
        #remove words that are not made up of valid letters
    
    def _removeShortWords(self):        
        self.corpus[:] = [word for word in self.corpus if len(word) >3 ]
        self.corpus_size = len(self.corpus)
        #print('Removed short words. corpus size now {} words'.format(self.corpus_size))
        self._shortWordsRemoved = True
        
    def _removeCapitals(self):
        self.corpus[:] = [word for word in self.corpus if word.islower()]
        self._capitalsRemoved = True
        '''
        Mutate exsisitng corpus to remove words that contain capitals. Words with 
        capitals are assumed to be proper nouns and are not considered solutions.
        
        Exerpt Detaling Big(O) for Slicing into a list 
        
        Slice operations require more thought. To access the slice [a:b] of a list, we 
        must iterate over every element between indices a and b. So, slice access is 
        O(k)O(k), where kk is the size of the slice. Deleting a slice is O(n)O(n) for 
        the same reason that deleting a single element is O(n)O(n): nn subsequent 
        elements must be shifted toward the list's beginning.[1]
        
        [1] https://bradfieldcs.com/algos/analysis/performance-of-python-types/
        
        '''
                   
    def _searchCorpus(self):

        self.corpus[:] = [word for word in self.corpus 
                   if set(list(word)).issubset(self.validLetters)] 
        #^^ https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating
        self.corpus_size =  len(self.corpus)
       # print('Removed words that include characters not in the puzzel, {} words remain in corpus'
       #       .format(self.corpus_size))
        self._corpusSearched = True
        
    def _checkForCenter(self):
        self.corpus[:] = [word for word in self.corpus if self.centerLetter in set(list(word))]
        self.corpus_size =  len(self.corpus)
        #print('Removed words that do not include center letter, {} words remain in corpus'
        #      .format(self.corpus_size))
        self._includesCenter = True
        
    def getWinners(self):
        if not self._shortWordsRemoved:
            self._removeShortWords()
        if not self._capitalsRemoved:
            self._removeCapitals()
        if not self._corpusSearched:
            self._searchCorpus()
        if not self._checkForCenter:
            self._checkForCenter()
            
        return self.corpus
              
    def _getGameData(self):
        url ='https://www.nytimes.com/puzzles/spelling-bee'
        xpath ='/html/body/div[2]/div[2]/div[2]/script/text()'
        
        page = requests.get(url)
        
        tree = html.fromstring(page.content)
        gameDataRaw = tree.xpath(xpath)
        self.gameDataDict = json.loads(gameDataRaw[0][18:])
        
        
        self.centerLetter = self.gameDataDict['today']['centerLetter']
        self.validLetters = self.gameDataDict['today']['validLetters']
        

    
class method1(Spelling_Bee):
    
    '''
    loads nltk.brown corpus into a list. Iterates through the list 4 times 
    checking for each soultion critera. Removes words when they fail a criteria.
    Assume remaining words are solutions.

    '''
    
    def __init__(self):
        start = time.time()
        self._getGameData()
        self._loadCorpus()
        self._processCorpus()
        end = time.time()
        print(end-start, len(self.corpus))
        
    def _loadCorpus(self):
 
        self.corpus = words.words()
        self.corpus_size = len(self.corpus)
        self._shortWordsRemoved = False
        self._capitalsRemoved = False
        self._corpusSearched = False
        self._includesCenter = False
    
        
        
    def _processCorpus(self):
        #lowers case
        self._removeCapitals()
        #remove short words
        self._removeShortWords()
        #remove words that are not made up of valid letters
        self._searchCorpus()
        #remove words that do not contain center letter
        self._checkForCenter()

      
    def _removeShortWords(self):
         for word in self.corpus[::-1]: # iterate through list backwards to avoid messing up index
             if len(word) < 4:
                 self.corpus.remove(word)
         self._shortWordsRemoved = True
        
    def _removeCapitals(self):
        for word in self.corpus[::-1]:
            if not word.islower():
                self.corpus.remove(word)
        self._capitalsRemoved = True
        
    def _searchCorpus(self):
        for word in self.corpus[::-1]:
             if not set(list(word)).issubset(self.validLetters):
                 self.corpus.remove(word)
        self._corpusSearced = True
        
    def _checkForCenter(self):
        for word in self.corpus[::-1]:
            if not self.centerLetter in set(list(word)):
                self.corpus.remove(word)
        self._includesCenter = True
                                   
    
    
class method2(Spelling_Bee):
    
    '''
    iterates through nltk words corpus and only loads valid words to list
    '''
            
    def __init__(self):
        start = time.time()
        self._getGameData()
        self._loadProccessCorpus()
        #self._trie()
        end = time.time()
        print(end-start, len(self.corpus))
        
    def _valid_word(self, word):
        length = len(word) > 3
        capital = word.islower()
        characters = set(list(word)).issubset(self.validLetters)
        center = self.centerLetter in set(list(word))
        
        return length and capital and characters and center
        
    def _loadProccessCorpus(self):
        self.corpus = []
        for word in words.words():
            if self._valid_word(word):
                self.corpus.append(word)
       


class method3(Spelling_Bee):
    '''
    nltk.brown corpus filtered on saving to trie data type
    '''
        
    def __init__(self):
        start = time.time()
        self._getGameData()
        self._make_trie()
        self._loadCorpus()
        #self._trie()
        end = time.time()
        print(end-start)
    
        
        
    def _make_trie(self):
        self.trie = Trie()
    
    def _loadCorpus(self):
        for word in words.words():
            if len(word) > 3 and set(list(word)).issubset(self.validLetters):
                self.trie.insert(word)
                


        
class Pro(Spelling_Bee):    
        
    def __init__(self):
        self._getGameData()
      
    
    
    def _getGameData(self):
        start = time.time()
        url ='https://www.nytimes.com/puzzles/spelling-bee'
        xpath ='/html/body/div[2]/div[2]/div[2]/script/text()'
        
        page = requests.get(url) #get request from url
        
        tree = html.fromstring(page.content)  #parse
        gameDataRaw = tree.xpath(xpath) #xpath extract, game data a json
        self.gameDataDict = json.loads(gameDataRaw[0][18:]) #extracts as dict
        
        
        self.answers = self.gameDataDict['today']['answers']
        self.centerLetter = self.gameDataDict['today']['centerLetter']
        self.validLetters = self.gameDataDict['today']['validLetters']
        self.pangrams = self.gameDataDict['today']['pangrams']
        end = time.time()
        print(end-start, len(self.answers))
        
        
    def getWinners(self):
        return self.answers
    
    
if __name__ == "__main__":
    print('BASE')
    base = Spelling_Bee()
    print()
    print('Method 1')
    m1 = method1()
    print()
    print('Method 2')
    m2 = method2()
    print()
    print('Method 3')
    m3 = method3()
    print()
    print('Pro')
    p = Pro()

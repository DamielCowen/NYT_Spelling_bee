class TrieNode:

    def __init__(self, character):
        '''
        Trie Node class. Keeps children as a list of TrieNode objects
        '''
        self.character = character
        self.children = []
        self.isEndOfWord = False
   


class Trie:

    def __init__ (self):
        '''
        Trie data structure. 
        '''
        self.root = TrieNode("")
        self.root.isEndOfWord = True
        self.number_nodes = 1

    def insert(self, word):
        '''
        adds a word from the dictonary to the trie. Starts from the first character in the word. Creates a new nodes as needed. 
        '''      
        node = self.root #starts with ''
        print(word)
        for letter in word: 
            for child in node.children:
                
                if child.character == letter:
                    node = child
                    break
            else:
                child = TrieNode(letter)
                node.children.append(child)
                self.number_nodes += 1
                node = child


        node.isEndOfWord = True



    def search(self, word):
        '''
        iterates through each character in the word. If the following character is a child, that becomes the new node. 
        if you get to the end of the word then and the isEndOfWord == True returns true, else returns false
        '''
        node = self.root #starts with ''
        for letter in word: 
            for child in node.children:
                if child.character == letter:
                    if node.isEndOfWord == True:
                        node = child
                    break
            else:
                return False

        return node.isEndOfWord



    def depthFirstSearch(self, node, word, includesKey, charstring, wordlist = []):
        if node.character not in charstring:
            return
        word += node.character
        includesKey = includesKey or node.character == charstring[0]
        if includesKey and node.isEndOfWord:
            wordlist.append(word)
        for child in node.children:
            self.depthFirstSearch(child, word, includesKey, charstring, wordlist)
        return wordlist

    # def getValidWords(self, charstring):
    #     return self.depthFirstSearch(self.root, '', False, charstring)

    def getValidWords(self, charstring):
        """
        Returns list of all words in trie containing *only* letters in
        charstring. Letters can occur 0 or more times. All words must
        contains charstring[0] (key).
        """
        def dfs(node, word, includesKey, charstring, wordlist=[]):
            if node.character not in charstring:
                # Invalid character, so stop building the word
                return
            word += node.character
            includesKey = includesKey or node.character == charstring[0]
            if includesKey and node.isEndOfWord and len(word) >= 4:
                # completed word includes the key
                wordlist.append(word)
                # print(word)
            for child in node.children:
                dfs(child, word, includesKey, charstring, wordlist)
            return sorted(wordlist,key=len, reverse=True)

        return dfs(self.root, "", False, charstring)







    
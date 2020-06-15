class TrieNode:
    def __init__(self, c):
        self.char = c
        self.children = []
        self.isCompleteWord = False


class Trie2:
    def __init__(self):
        self.root = TrieNode("")
        self.root.isCompleteWord = True

    def add(self, word):
        n = self.root
        for c in word:
            for child in n.children:
                if child.char == c:
                    n = child
                    break
            else:
                child = TrieNode(c)
                n.children.append(child)
                n = child
        n.isCompleteWord = True

    def search(self, word):
        n = self.root
        for c in word:
            for child in n.children:
                if child.char == c:
                    n = child
                    break
            else:
                return False
        return n.isCompleteWord

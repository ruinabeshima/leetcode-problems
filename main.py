class TrieNode: 
    def __init__(self): 
        self.children = {}
        self.is_word = False 

class Trie: 
    def __init__(self):
        self.root = TrieNode() 

    def insert(self, word): 
        node = self.root 

        for ch in word:
            if ch not in node.children: 
                node.children[ch] = TrieNode() 
            node = node.children[ch]

        # Mark the last node
        node.is_word = True 

    def walk(self, s): 
        node = self.root 

        for ch in s: 
            if ch not in node.children: 
                return None 
            node = node.children[ch]

        return node 

    def search(self, word): 
        node = self.walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix): 
        return self.walk(prefix) is not None
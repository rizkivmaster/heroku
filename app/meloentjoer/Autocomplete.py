__author__ = 'traveloka'


class TrieNode:
    def __init__(self):
        self.childNodes = dict()
        self.words = set()
        self.prefixCount = 0

    def add_word(self, node, word, rest):
        self.words.add(word)
        if len(rest) == 0:
            return node
        next_char = rest[0]
        if next_char in self.childNodes:
            child_node = self.childNodes[next_char]
            child_node.add_word(word, rest[1:])
        else:
            new_node = TrieNode()
            new_node.prefixCount = self.prefixCount+1
            self.childNodes[next_char] = new_node.add_word(word, rest[1:])
        return self

    def dfs(self, rest):
        if len(rest) == 0:
            return self
        else:
            if rest[0] in self.childNodes:
                return self.dfs(rest[1:])
            else:
                return None


class AutoComplete:

    def __init__(self):
        self.trie = TrieNode()

    def add_keyword(self, word, key):
        self.trie.add_word(word, key)

    def get_word(self, key):
        return self.trie.dfs(key)
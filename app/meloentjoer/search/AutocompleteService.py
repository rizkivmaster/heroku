from app.meloentjoer.common.util.TrieNode import TrieNode

__author__ = 'traveloka'


class AutocompleteService:
    def __init__(self):
        self.trie = TrieNode()

    def add_keyword(self, word, key):
        self.trie.add_word(word, key)

    def get_words(self, key):
        node = self.trie.dfs(key)
        if node is None:
            return []
        else:
            return list(node.words)

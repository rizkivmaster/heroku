class TrieNode:
    def __init__(self):
        self.childNodes = dict()
        self.words = set()
        self.prefixCount = 0

    def reset(self):
        self.childNodes = dict()
        self.words = set()
        self.prefixCount = 0

    def add_word(self, word, rest):
        self.words.add(word)
        if len(rest) > 0:
            self.prefixCount += 1
            next_char = rest[0]
            if next_char in self.childNodes:
                child_node = self.childNodes[next_char]
                child_node.add_word(word, rest[1:])
            else:
                new_node = TrieNode()
                new_node.prefixCount = self.prefixCount + 1
                new_node.add_word(word, rest[1:])
                self.childNodes[next_char] = new_node

    def dfs(self, rest):
        """
        :param rest:
        :return:
        """
        if len(rest) == 0:
            return self.words
        else:
            if rest[0] in self.childNodes:
                child_node = self.childNodes[rest[0]]
                return child_node.dfs(rest[1:])
            else:
                return []

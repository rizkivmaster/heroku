import unittest
from app.meloentjoer.common.util.TrieNode import TrieNode


class Test(unittest.TestCase):
    def test_TrieNode(self):
        node = TrieNode()
        node.add_word('test', 'test')
        node.add_word('testing', 'testing')
        new_list = node.dfs('testi')
        assert (len(new_list) > 0)


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def put(self, key: str, value=None):
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def keys_with_prefix(self, prefix: str):
        result = []
        node = self.root
        for char in prefix:
            if char not in node.children:
                return result
            node = node.children[char]

        def dfs(current_node, path):
            if current_node.is_end_of_word:
                result.append("".join(path))
            for char, next_node in current_node.children.items():
                dfs(next_node, path + [char])

        dfs(node, list(prefix))
        return result

from Trie._base.node import FSANode
from Trie._base.automata import FSA

__all__ = ['Trie']


class Trie(FSA):
    """ To create a Trie instance, create an object of this class.

    Attributes
    ----------
    root: _TrieNode
        The Top level node which is created every time you create a Trie instance
    """

    __slots__ = 'root'

    def __init__(self):
        """ This method initializes the Trie instance by creating the root node.

        By default, the id of the root node is 1 and number of words in the Trie is also 1.
        The label of the root node is an empty string ''.
        """

        root = FSANode(0, '')
        super(Trie, self).__init__(root)

    def __len__(self):
        """ Returns the number of nodes in the Trie Data Structure

        Returns
        -------
        int
            Number of Nodes in the trie data structure
        """

        return self._id

    def add(self, word, count=1):
        """ Adds a word in the trie data structure.

        Parameters
        ----------
        word: str
            The word that you want to insert in the trie.

        Raises
        ------
        AssertionError
            If the word is None
        """

        assert word is not None, "Input word cannot be None"

        node = self.root
        for i, letter in enumerate(word):
            if letter not in node.children:
                self._id += 1
                node.add_child(letter, _id=self._id)
            node = node[letter]
            if i == len(word)-1:
                node.eow = True
                node.count += count
                self._num_of_words += count

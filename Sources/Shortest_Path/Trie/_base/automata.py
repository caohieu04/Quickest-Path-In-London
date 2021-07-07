import os
from types import GeneratorType

from Trie._utils.utils import gen_source, validate_expression
from Trie.exceptions import InvalidWildCardExpressionError


class FSA:
    """
    Base Class which defines the common methods for Trie.
    """

    __slots__ = '_id', '_num_of_words', 'root'

    def __init__(self, root):
        self._id = 1
        self._num_of_words = 1
        self.root = root

    def __contains__(self, word):
        """ Returns true if the word is present else false

        Parameters
        ----------
        word: str
            The word to be searched

        Returns
        -------
        boolean
            Whether the word is present
        """
        if word == '':
            return True  # The root is an empty string. So it is always present
        if word is None:
            return False
        node = self.root
        for i, letter in enumerate(word):
            if letter in node.children:
                node = node[letter]
                if node.eow and i == len(word) - 1:
                    return True
            else:
                return False
        return False

    def __contains_prefix(self, prefix):
        """ Checks whether the prefix is present. If yes, returns (True, node) where the prefix ends else returns (False, None)

        Parameters
        ----------
        prefix: str
            The Prefix string

        Returns
        -------
        tuple: (exists, node)
            If yes, returns (True, node) where the prefix ends else returns (False, None)
        """
        if prefix == '':
            return True, self.root
        if prefix is None:
            return False, None
        node = self.root
        for _, letter in enumerate(prefix):
            if letter in node.children:
                node = node[letter]
            else:
                return False, None
        return True, node

    def contains_prefix(self, prefix):
        """ Returns a boolean indicating the presence of prefix

        Parameters
        ----------
        prefix: str
            The Prefix string

        Returns
        -------
        boolean
            True, if present, else False.
        """
        contains, _ = self.__contains_prefix(prefix)
        return contains

    @staticmethod
    def __words_with_wildcard(node,
                              wildcard,
                              index,
                              current_word="",
                              with_count=False):
        """ Returns all the words where the wildcard pattern matches.

        Parameters
        ----------
        node: inc_search._base.node.FSANode
            Current Node in the Finite State Automaton
        wildcard: str
            The wildcard pattern as input
        index: int
            The current index in the wildcard pattern
        current_word: str
            Word formed till now

        Returns
        -------
        list
            The list of words where the wildcard pattern matches.
        """
        if not node or not wildcard or index < 0:
            return []

        if node.eow and index >= len(wildcard) and current_word:
            return [(current_word,
                     node.count)] if with_count else [current_word]

        if index >= len(wildcard):
            return []

        words = []
        letter = wildcard[index]

        if letter == '?':
            for child in node.children:
                child_node = node[child]

                child_words = FSA.__words_with_wildcard(child_node,
                                                        wildcard,
                                                        index + 1,
                                                        current_word + child,
                                                        with_count=with_count)
                words.extend(child_words)

        elif letter == '*':
            words_at_current_level = FSA.__words_with_wildcard(
                node, wildcard, index + 1, current_word, with_count=with_count)
            words.extend(words_at_current_level)

            if node.children:
                for child in node.children:
                    child_node = node[child]
                    child_words = FSA.__words_with_wildcard(
                        child_node,
                        wildcard,
                        index,
                        current_word + child,
                        with_count=with_count)
                    words.extend(child_words)
            elif node.eow and index == len(wildcard) - 1:
                return [(current_word,
                         node.count)] if with_count else [current_word]

        else:
            if letter in node.children:
                child_node = node[letter]
                child_words = FSA.__words_with_wildcard(child_node,
                                                        wildcard,
                                                        index + 1,
                                                        current_word +
                                                        child_node.val,
                                                        with_count=with_count)
                words.extend(child_words)

        return words

    def search_with_wildcard(self, wildcard, with_count=False):
        """ Returns all the words where the wildcard pattern matches.

        Parameters
        ----------
        wildcard: str
            The wildcard pattern as input

        Returns
        -------
        list
            A list of words where the wildcard pattern matches.
        """
        words = []
        if wildcard is None:
            raise ValueError("Search pattern cannot be None")

        if wildcard == '':
            return words
        try:
            wildcard = validate_expression(wildcard)
        except InvalidWildCardExpressionError:
            raise

        if wildcard.isalpha():
            present, node = self.__contains_prefix(wildcard)
            if present and node.eow:
                words.append(
                    (wildcard,
                     node.count)) if with_count else words.append(wildcard)
            return words

        return FSA.__words_with_wildcard(self.root,
                                         wildcard,
                                         0,
                                         self.root.val,
                                         with_count=with_count)

    def search_with_prefix(self, prefix, with_count=False):
        """ Returns a list of words which share the same prefix as passed in input. The words are by default sorted in the increasing order of length.

        Parameters
        ----------
        prefix: str
            The Prefix string

        Returns
        -------
        list
            A list of words which share the same prefix as passed in input
        """
        if not prefix:
            return []
        _, node = self.__contains_prefix(prefix)
        if node is None:
            return []
        return FSA.__words_with_wildcard(node,
                                         '*',
                                         0,
                                         prefix,
                                         with_count=with_count)

    def add(self, word, count=1):
        """ To be overridden """
        pass

    def add_all(self, source):
        """ Add a collection of words from any of the following passed in input

        Words which are not of type string are not inserted in the Trie

        Parameters
        ----------
        source: list, set, tuple, generator, file
            Words to be added
        """
        if isinstance(source, (GeneratorType, str, list, tuple, set)):
            pass
        elif hasattr(source, 'read'):
            pass
        else:
            raise ValueError("Source type {0} not supported ".format(
                type(source)))

        if isinstance(source, str) and not os.path.exists(source):
            raise IOError("File does not exists")

        if isinstance(source, str) or hasattr(source, 'read'):
            source = gen_source(source)

        for word in source:
            if type(word) == str:
                self.add(word)

    def get_word_count(self):
        """ Returns the number of words in Trie data structure

        Returns
        -------
        int
            Number of words in Trie data structure
        """
        return max(0, self._num_of_words - 1)

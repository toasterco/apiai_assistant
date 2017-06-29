""" Corpus

This module provides the Corpus class that can be used to manage
and access a json file that holds the outputs of an API.ai agent """


import json
import random


class Corpus(object):
    """
    Args:
        filepath (str): path to the json file
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.corpus = None
        self.init_corpus()

    def __contains__(self, x):
        """
        Returns:
            bool: True if the element is in the corpus. False otherwise
        """

        if self.corpus is None:
            self.init_corpus()
        return x in self.corpus

    def init_corpus(self):
        """ Initialize the corpus by reading the json file and loading
        it in memory """

        with open(self.filepath, 'r') as fd:
            self.corpus = json.load(fd)

    def __getitem__(self, key):
        """
        Returns:
            str: A randomly selected element of the key item in the corpus.
                 None if not found.
        """

        return self.get(key)

    def get(self, key):
        """
        Returns:
            str: A randomly selected element of the key item in the corpus.
                 None if not found.
        """

        if self.corpus is None:
            self.init_corpus()

        if key not in self.corpus:
            return None

        return random.choice(self.corpus[key])

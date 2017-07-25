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

    DEFAULT_CONFIRMATIONS = [['Yes', 'No']]
    """ :list: used if no confirmations object is found in the corpus JSON object """

    def __init__(self, filepath):
        self.filepath = filepath
        self.corpus = None
        self.suggestions = None
        self.confirmations = None
        self.init_corpus()

    def __contains__(self, x):
        """
        Returns:
            bool: True if the element is in the corpus. False otherwise
        """

        if self.corpus is None:
            self.init_corpus()
        return x in self.corpus

    def validate(self, data):
        """
        Args:
            data (:obj:`dict`): JSON data to validate
        Returns:
            bool: True if data is valid/ False otherwise
        """

        return 'corpus' in data

    def init_corpus(self):
        """ Initialize the corpus by reading the json file and loading
        it in memory """

        with open(self.filepath, 'r') as fd:
            data = json.load(fd)
            if not self.validate(data):
                raise ValueError('{} not a corpus'.format(self.filepath))

            self.corpus = data['corpus']
            self.suggestions = data.get('suggestions')
            self.condirmations = data.get(
                'confirmations', self.DEFAULT_CONFIRMATIONS)

    def __getitem__(self, key):
        """
        Returns:
            str: A randomly selected element of the key item in the corpus.
                 None if not found.
        """

        return self.get(key)

    def get_confirmation(self):
        """ Returns a random confirmation """

        if self.corpus is None:
            self.init_corpus()

        return random.choice(self.confirmations)

    def get(self, key, source=None):
        """
        Returns:
            str: A randomly selected element of the key item in the corpus.
                 None if not found.
        """

        if self.corpus is None:
            self.init_corpus()

        if source is None:
            source = self.corpus

        if key not in source:
            return None

        return random.choice(source[key])

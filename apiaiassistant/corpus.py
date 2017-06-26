import json
import random


class Corpus(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.corpus = None
        self.init_corpus()

    def __contains__(self, x):
        if self.corpus is None:
            self.init_corpus()
        return x in self.corpus

    def init_corpus(self):
        with open(self.filepath, 'r') as fd:
            self.corpus = json.load(fd)

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key):
        if self.corpus is None:
            self.init_corpus()

        if key not in self.corpus:
            return None

        return random.choice(self.corpus[key])

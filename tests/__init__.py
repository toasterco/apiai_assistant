def mocked_init_corpus(faked_corpus=None):
    def mocked_init_corpus_closure(self):
        self.corpus = faked_corpus or {}
    return mocked_init_corpus_closure

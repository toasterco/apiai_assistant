import mock
import unittest

from tests import mocked_init_corpus
from apiaiassistant.corpus import Corpus


class CorpusTestCase(unittest.TestCase):
    @mock.patch('apiaiassistant.corpus.Corpus.init_corpus',
                mocked_init_corpus({'corpus': {'foo': ['bar']}}))
    def test_basic(self):
        c = Corpus('dummystring')
        self.assertEqual(c.corpus, {'foo': ['bar']})

    @mock.patch('apiaiassistant.corpus.Corpus.init_corpus',
                mocked_init_corpus({'corpus': {'foo': ['bar']}}))
    def test_contains(self):
        c = Corpus('dummystring')
        self.assertTrue('foo' in c)
        self.assertFalse('abc' in c)

    @mock.patch('apiaiassistant.corpus.Corpus.init_corpus',
                mocked_init_corpus({'corpus': {'foo': ['bar']}}))
    def test_getitem(self):
        c = Corpus('dummystring')
        self.assertEqual(c['foo'], 'bar')
        self.assertEqual(c['abc'], None)

    @mock.patch('apiaiassistant.corpus.Corpus.init_corpus',
                mocked_init_corpus({'corpus': {'foo': ['bar']}}))
    def test_init_corpus(self):
        c = Corpus('dummystring')
        c.corpus = None
        c.confirmations = None
        self.assertTrue('foo' in c)
        self.assertTrue(c.confirmations, Corpus.DEFAULT_CONFIRMATIONS)

        c.corpus = None
        self.assertEqual(c['foo'], 'bar')

if __name__ == '__main__':
    unittest.main()

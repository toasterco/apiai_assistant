import mock
import unittest

from tests import mocked_init_corpus
from apiaiassistant.corpus import Corpus


class CorpusTestCase(unittest.TestCase):
    @mock.patch('apiaiassistant.corpus.Corpus.init_corpus',
                mocked_init_corpus(
                    {
                        'foo': ['bar']
                    }))
    def test_basic(self):
        c = Corpus('abd.json')
        self.assertEqual(c.corpus, {'foo': ['bar']})

    @mock.patch('apiaiassistant.corpus.Corpus.init_corpus',
                mocked_init_corpus(
                    {
                        'foo': ['bar']
                    }))
    def test_contains(self):
        c = Corpus('abd.json')
        self.assertTrue('foo' in c)
        self.assertFalse('abc' in c)

    @mock.patch('apiaiassistant.corpus.Corpus.init_corpus',
                mocked_init_corpus(
                    {
                        'foo': ['bar']
                    }))
    def test_getitem(self):
        c = Corpus('abd.json')
        self.assertEqual(c['foo'], 'bar')
        self.assertEqual(c['abc'], None)


if __name__ == '__main__':
    unittest.main()

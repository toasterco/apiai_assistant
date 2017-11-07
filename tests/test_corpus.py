import json
import mock
import unittest

from tests import mocked_init_corpus
from apiai_assistant.corpus import Corpus


class CorpusTestCase(unittest.TestCase):
    @mock.patch('apiai_assistant.corpus.Corpus.init_corpus',
                mocked_init_corpus({'corpus': {'foo': ['bar']}}))
    def test_basic(self):
        c = Corpus('dummystring')
        self.assertEqual(c.corpus, {'foo': ['bar']})

    @mock.patch('apiai_assistant.corpus.Corpus.init_corpus',
                mocked_init_corpus({'corpus': {'foo': ['bar']}}))
    def test_contains(self):
        c = Corpus('dummystring')
        self.assertTrue('foo' in c)
        self.assertFalse('abc' in c)

    @mock.patch('apiai_assistant.corpus.Corpus.init_corpus',
                mocked_init_corpus({'corpus': {'foo': ['bar']}}))
    def test_getitem(self):
        c = Corpus('dummystring')
        self.assertEqual(c['foo'], 'bar')
        self.assertEqual(c['abc'], None)

    def test_init_corpus(self):
        data = {'corpus': {'foo': ['bar']}}
        with mock.patch("__builtin__.open", mock.mock_open(read_data=json.dumps(data))) as m:
            c = Corpus('dummystring')
            self.assertTrue('foo' in c)
            self.assertEqual(c.confirmations, Corpus.DEFAULT_CONFIRMATIONS)
            self.assertEqual(c.suggestions, None)

            c.corpus = None
            self.assertEqual(c['foo'], 'bar')

    def test_corpus_invalid(self):
        data = {'foo': ['bar']}
        with mock.patch("__builtin__.open", mock.mock_open(read_data=json.dumps(data))) as m:
            with self.assertRaises(ValueError):
                c = Corpus('dummystring')

    def test_confirmation(self):
        data = {'corpus': {'foo': ['bar']}}
        with mock.patch("__builtin__.open", mock.mock_open(read_data=json.dumps(data))) as m:
            c = Corpus('dummystring')
            c.corpus = None
            confirmation = c.get_confirmation()
            self.assertTrue(confirmation in Corpus.DEFAULT_CONFIRMATIONS)


if __name__ == '__main__':
    unittest.main()

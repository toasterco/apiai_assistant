import unittest

from apiai_assistant.widgets import InvalidGoogleAssistantWidget
from apiai_assistant.widgets import OptionInfo


class OptionInfoTestCase(unittest.TestCase):
    def test_basic(self):
        key = "foobar"
        w = OptionInfo(key)
        self.assertEqual(
            w.render(),
            {
                "key": key,
                "synonyms": []
            }
        )

    def test_missing_key(self):
        with self.assertRaises(InvalidGoogleAssistantWidget):
            OptionInfo(None)

    def test_missing_key_but_synonyms(self):
        synonyms = ['foo', 'bar']
        w = OptionInfo(None, synonyms)
        self.assertEqual(
            w.render(),
            {
                "key": None,
                "synonyms": synonyms
            }
        )


if __name__ == '__main__':
    unittest.main()

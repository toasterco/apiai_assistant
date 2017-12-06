import unittest

from apiai_assistant import Platforms
from apiai_assistant.widgets import InvalidGoogleAssistantWidget
from apiai_assistant.widgets import GoogleAssistantOptionInfo


class GoogleAssistantOptionInfoTestCase(unittest.TestCase):
    def test_basic(self):
        key = "foobar"
        w = GoogleAssistantOptionInfo(key)
        self.assertEqual(
            w.render(Platforms.GOOGLE_ASSISTANT),
            {
                "key": key,
                "synonyms": []
            }
        )

    def test_missing_key(self):
        with self.assertRaises(InvalidGoogleAssistantWidget):
            GoogleAssistantOptionInfo(None)

    def test_missing_key_but_synonyms(self):
        synonyms = ['foo', 'bar']
        w = GoogleAssistantOptionInfo(None, synonyms)
        self.assertEqual(
            w.render(Platforms.GOOGLE_ASSISTANT),
            {
                "key": None,
                "synonyms": synonyms
            }
        )


if __name__ == '__main__':
    unittest.main()

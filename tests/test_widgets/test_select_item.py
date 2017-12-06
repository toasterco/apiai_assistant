import unittest

from apiai_assistant import Platforms
from apiai_assistant.widgets import GoogleAssistantSelectItem
from apiai_assistant.widgets import GoogleAssistantOptionInfo


class GoogleAssistantSelectItemTestCase(unittest.TestCase):
    def test_basic(self):
        key = "foobar"
        title = "bario"
        w_slct_item = GoogleAssistantSelectItem(
            title=title,
            option_info=GoogleAssistantOptionInfo(key)
        )
        self.assertEqual(
            w_slct_item.render(Platforms.GOOGLE_ASSISTANT),
            {
                "title": title,
                "description": None,
                "optionInfo": {
                    "key": key,
                    "synonyms": []
                },
                "image": None
            }
        )

if __name__ == '__main__':
    unittest.main()

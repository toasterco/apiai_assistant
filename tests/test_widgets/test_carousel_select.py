import unittest

from apiai_assistant import Platforms
from apiai_assistant.widgets import GoogleAssistantOptionInfo
from apiai_assistant.widgets import GoogleAssistantSelectItem
from apiai_assistant.widgets import GoogleAssistantCarouselSelectWidget


class GoogleAssistantCarouselSelectWidgetTestCase(unittest.TestCase):
    def test_basic(self):
        item_keys = ['a', 'b', 'c']
        items = [
            GoogleAssistantSelectItem(
                title=key,
                option_info=GoogleAssistantOptionInfo(key))
            for key in item_keys
        ]
        w = GoogleAssistantCarouselSelectWidget(items)
        self.assertEqual(
            w.render(Platforms.GOOGLE_ASSISTANT),
            {
                "type": "carousel_card",
                "platform": "google",
                "items": [
                    {
                        "title": "a",
                        "description": None,
                        "optionInfo": {
                            "key": "a",
                            "synonyms": []
                        },
                        "image": None
                    },
                    {
                        "title": "b",
                        "description": None,
                        "optionInfo": {
                            "key": "b",
                            "synonyms": []
                        },
                        "image": None
                    },
                    {
                        "title": "c",
                        "description": None,
                        "optionInfo": {
                            "key": "c",
                            "synonyms": []
                        },
                        "image": None
                    }
                ]
            }
        )


if __name__ == '__main__':
    unittest.main()

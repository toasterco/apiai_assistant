import unittest

from apiai_assistant import Platforms
from apiai_assistant.widgets import GoogleAssistantOptionInfo
from apiai_assistant.widgets import GoogleAssistantSelectItem
from apiai_assistant.widgets import GoogleAssistantListSelectWidget


class ListSelectWidgetTestCase(unittest.TestCase):
    def test_basic(self):
        item_keys = ['a', 'b', 'c']
        items = [
            GoogleAssistantSelectItem(
                title=key,
                option_info=GoogleAssistantOptionInfo(key))
            for key in item_keys
        ]
        w = GoogleAssistantListSelectWidget(items)
        origin = Platforms.GOOGLE_ASSISTANT
        self.assertEqual(
            w.render(origin),
            {
                "type": "list_card",
                "platform": origin,
                "title": None,
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

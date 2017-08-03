import unittest

from apiai_assistant.widgets import OptionInfo
from apiai_assistant.widgets import SelectItem
from apiai_assistant.widgets import ListSelectWidget


class ListSelectWidgetTestCase(unittest.TestCase):
    def test_basic(self):
        item_keys = ['a', 'b', 'c']
        items = [
            SelectItem(title=key, option_info=OptionInfo(key))
            for key in item_keys
        ]
        w = ListSelectWidget(items)
        self.assertEqual(
            w.render(),
            {
                "type": "list_card",
                "platform": "google",
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

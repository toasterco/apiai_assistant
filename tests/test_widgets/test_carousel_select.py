import unittest

from apiai_assistant.widgets import OptionInfo
from apiai_assistant.widgets import SelectItem
from apiai_assistant.widgets import CarouselSelectWidget


class CarouselSelectWidgetTestCase(unittest.TestCase):
    def test_basic(self):
        item_keys = ['a', 'b', 'c']
        items = [
            SelectItem(title=key, option_info=OptionInfo(key))
            for key in item_keys
        ]
        w = CarouselSelectWidget(items)
        self.assertEqual(
            w.render(),
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

import unittest

from apiaiassistant.widgets import SelectItem
from apiaiassistant.widgets import OptionInfo


class SelectItemTestCase(unittest.TestCase):
    def test_basic(self):
        key = "foobar"
        title = "bario"
        w_slct_item = SelectItem(title=title, option_info=OptionInfo(key))
        self.assertEqual(
            w_slct_item.render(),
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

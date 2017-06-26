import unittest

from apiaiassistant.widgets import Button
from apiaiassistant.widgets import Image


class ImageTestCase(unittest.TestCase):
    def test_basic(self):
        url = "https://abc.com/foo.png"
        w = Image(url)
        self.assertEqual(
            w.render(),
            {
                "url": url,
                "accessibilityText": None
            }
        )


class ButtonTestCase(unittest.TestCase):
    def test_basic(self):
        title = "basic"
        w = Button(title)
        self.assertEqual(
            w.render(),
            {
                "title": title,
                "openUrlAction": {
                    "url": None
                }
            }
        )


if __name__ == '__main__':
    unittest.main()

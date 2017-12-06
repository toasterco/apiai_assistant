import unittest

from apiai_assistant import Platforms
from apiai_assistant.widgets import WidgetTypes
from apiai_assistant.widgets import Button
from apiai_assistant.widgets import Image


class ImageTestCase(unittest.TestCase):
    def test_google_basic(self):
        url = "https://abc.com/foo.png"
        w = Image(url)
        self.assertEqual(
            w.render(Platforms.GOOGLE_ASSISTANT),
            {
                "url": url,
                "accessibilityText": None
            }
        )

    def test_apiai_basic(self):
        url = "https://abc.com/foo.png"
        w = Image(url)
        origin = Platforms.FACEBOOK_MESSENGER
        self.assertEqual(
            w.render(origin),
            {
                'type': WidgetTypes.Image,
                'platform': origin,
                'imageUrl': url
            }
        )


class ButtonTestCase(unittest.TestCase):
    def test_google_basic(self):
        title = "basic"
        w = Button(title)
        self.assertEqual(
            w.render(Platforms.GOOGLE_ASSISTANT),
            {
                "title": title,
                "openUrlAction": {
                    "url": None
                }
            }
        )

    def test_apiai_basic(self):
        title = "basic"
        w = Button(title)
        self.assertEqual(
            w.render(Platforms.FACEBOOK_MESSENGER),
            {
                "postback": None,
                "text": title
            }
        )


if __name__ == '__main__':
    unittest.main()

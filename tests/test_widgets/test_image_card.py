import unittest

from apiaiassistant.widgets import ImageCardWidget
from apiaiassistant.widgets import Button
from apiaiassistant.widgets import Image
from apiaiassistant.widgets import InvalidGoogleAssistantWidget


class ImageCardWidgetTestCase(unittest.TestCase):
    def test_basic_no_button(self):
        title = "image card test"
        text = "image card text"
        w = ImageCardWidget(title, text)
        self.assertEqual(
            w.render(),
            {
                "platform": "google",
                "type": "basic_card",
                "title": title,
                "formattedText": text,
                "image": None,
                "buttons": []
            }
        )

    def test_basic_button(self):
        title = "image card test"
        text = "image card text"
        button = Button(title)
        w = ImageCardWidget(title, text=text, button=button)
        self.assertEqual(
            w.render(),
            {
                "platform": "google",
                "type": "basic_card",
                "title": title,
                "formattedText": text,
                "image": None,
                "buttons": [{
                    "title": title,
                    "openUrlAction": {"url": None}
                }]
            }
        )

    def test_basic_image(self):
        title = "image card test"
        text = "image card text"
        url = "foo.com"
        image_w = Image(url)
        w = ImageCardWidget(title, text=text, image=image_w)
        self.assertEqual(
            w.render(),
            {
                "platform": "google",
                "type": "basic_card",
                "title": title,
                "formattedText": text,
                "image": {
                    "url": url,
                    "accessibilityText": None
                },
                "buttons": []
            }
        )

    def test_validation(self):
        title = "image card test"
        with self.assertRaises(InvalidGoogleAssistantWidget):
            ImageCardWidget(title)


if __name__ == '__main__':
    unittest.main()

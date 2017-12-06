import unittest

from apiai_assistant import Platforms
from apiai_assistant.widgets import Image
from apiai_assistant.widgets import Button
from apiai_assistant.widgets import WidgetTypes
from apiai_assistant.widgets import ImageCardWidget
from apiai_assistant.widgets import InvalidGoogleAssistantWidget
from apiai_assistant.widgets import InvalidWidget


class ImageCardWidgetTestCase(unittest.TestCase):
    def test_google_basic_no_button(self):
        title = "image card test"
        text = "image card text"
        w = ImageCardWidget(title, text)
        origin = Platforms.GOOGLE_ASSISTANT
        self.assertEqual(
            w.render(origin),
            {
                "platform": origin,
                "type": "basic_card",
                "title": title,
                "formattedText": text,
                "image": None,
                "buttons": []
            }
        )

    def test_apiai_basic_no_button(self):
        title = "image card test"
        text = "image card text"
        w = ImageCardWidget(title, text)
        origin = Platforms.FACEBOOK_MESSENGER
        self.assertEqual(
            w.render(origin),
            {
                "platform": origin,
                'buttons': [],
                'imageUrl': None,
                'subtitle': text,
                'title': title,
                'type': WidgetTypes.Card
            }
        )

    def test_google_basic_button(self):
        title = "image card test"
        text = "image card text"
        button = Button(title)
        w = ImageCardWidget(title, text=text, button=button)
        origin = Platforms.GOOGLE_ASSISTANT
        self.assertEqual(
            w.render(origin),
            {
                "platform": origin,
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

    def test_apiai_basic_button(self):
        title = "image card test"
        text = "image card text"
        button = Button(title)
        w = ImageCardWidget(title, text, button=button)
        origin = Platforms.FACEBOOK_MESSENGER
        self.assertEqual(
            w.render(origin),
            {
                "platform": origin,
                'buttons': [{
                    'postback': None,
                    'text': title
                }],
                'imageUrl': None,
                'subtitle': text,
                'title': title,
                'type': WidgetTypes.Card
            }
        )

    def test_google_basic_image(self):
        title = "image card test"
        text = "image card text"
        url = "foo.com"
        image_w = Image(url)
        w = ImageCardWidget(title, text=text, image=image_w)
        origin = Platforms.GOOGLE_ASSISTANT
        self.assertEqual(
            w.render(origin),
            {
                "platform": origin,
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

    def test_amazon_text_only(self):
        title = 'foo'
        text = 'bar'
        w = ImageCardWidget(title, text=text)
        origin = Platforms.AMAZON_ALEXA
        self.assertEqual(
            w.render(origin),
            {
                'content': text,
                'title': title,
                'type': 'Simple'
            }
        )

    def test_amazon_image(self):
        title = 'foo'
        text = 'bar'
        url = 'https://foo.bar'
        image_w = Image(url)
        w = ImageCardWidget(title, text=text, image=image_w)
        origin = Platforms.AMAZON_ALEXA
        self.assertEqual(
            w.render(origin),
            {
                'text': text,
                'title': title,
                'type': 'Standard',
                'image': {
                    'largeImageUrl': url,
                    'smallImageUrl': url
                }
            }
        )

    def test_validation(self):
        title = "image card test"
        with self.assertRaises(InvalidWidget):
            ImageCardWidget(title)


if __name__ == '__main__':
    unittest.main()

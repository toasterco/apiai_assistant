import unittest

from apiai_assistant import Platforms
from apiai_assistant.widgets import WidgetTypes
from apiai_assistant.widgets import SimpleResponseWidget
from apiai_assistant.widgets import InvalidWidget


class SimpleResponseWidgetTestCase(unittest.TestCase):
    def test_validation(self):
        with self.assertRaises(InvalidWidget):
            SimpleResponseWidget(None, None)

    def test_google_basic(self):
        speech = "foo"
        text = "bar"
        w = SimpleResponseWidget(speech, text)
        self.assertEqual(
            w.render(Platforms.GOOGLE_ASSISTANT),
            {
                "platform": "google",
                "type": "simple_response",
                "displayText": text,
                "ssml": w.ssml_format(speech)
            }
        )

    def test_google_basic_no_ssml(self):
        speech = "foo"
        text = "bar"
        w = SimpleResponseWidget(speech, text, ssml=False)
        self.assertEqual(
            w.render(Platforms.GOOGLE_ASSISTANT),
            {
                "platform": "google",
                "type": "simple_response",
                "displayText": text,
                "textToSpeech": speech
            }
        )

    def test_google_text(self):
        speech = "foo"
        w = SimpleResponseWidget(speech, None)
        self.assertEqual(
            w.render(Platforms.GOOGLE_ASSISTANT),
            {
                "platform": "google",
                "type": "simple_response",
                "displayText": speech,
                "ssml": w.ssml_format(speech)
            }
        )

    def test_amazon_basic(self):
        speech = "foo"
        text = "bar"
        w = SimpleResponseWidget(speech, text)
        self.assertEqual(
            w.render(Platforms.AMAZON_ALEXA),
            {
                "outputSpeech": {
                    "type": "SSML",
                    "text": text,
                    "ssml": w.ssml_format(speech)
                }
            }
        )

    def test_amazon_basic_no_ssml(self):
        speech = "foo"
        text = "bar"
        w = SimpleResponseWidget(speech, text, ssml=False)
        self.assertEqual(
            w.render(Platforms.AMAZON_ALEXA),
            {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": text,
                }
            }
        )

    def test_amazon_text(self):
        speech = "foo"
        w = SimpleResponseWidget(speech, None)
        self.assertEqual(
            w.render(Platforms.AMAZON_ALEXA),
            {
                "outputSpeech": {
                    "type": "SSML",
                    "text": speech,
                    "ssml": w.ssml_format(speech)
                }
            }
        )

    def test_apiai_basic(self):
        speech = "foo"
        text = "bar"
        origin = Platforms.FACEBOOK_MESSENGER
        w = SimpleResponseWidget(speech, text)
        self.assertEqual(
            w.render(origin),
            {
                "type": WidgetTypes.Text,
                "speech": text,
                "platform": origin
            }
        )

    def test_apiai_basic_no_ssml(self):
        speech = "foo"
        text = "bar"
        origin = Platforms.FACEBOOK_MESSENGER
        w = SimpleResponseWidget(speech, text, ssml=False)
        self.assertEqual(
            w.render(origin),
            {
                "type": WidgetTypes.Text,
                "speech": text,
                "platform": origin
            }
        )

    def test_apiai_text(self):
        speech = "foo"
        w = SimpleResponseWidget(speech, None)
        origin = Platforms.FACEBOOK_MESSENGER
        self.assertEqual(
            w.render(origin),
            {
                "type": WidgetTypes.Text,
                "speech": speech,
                "platform": origin
            }
        )


if __name__ == '__main__':
    unittest.main()

import unittest

from apiaiassistant.widgets import SimpleResponseWidget
from apiaiassistant.widgets import InvalidGoogleAssistantWidget


class SimpleResponseWidgetTestCase(unittest.TestCase):
    def test_basic(self):
        speech = "foo"
        text = "bar"
        w = SimpleResponseWidget(speech, text)
        self.assertEqual(
            w.render(),
            {
                "platform": "google",
                "type": "simple_response",
                "displayText": text,
                "speech": w.ssml_format(speech)
            }
        )

    def test_basic_ssml(self):
        speech = "foo"
        text = "bar"
        w = SimpleResponseWidget(speech, text, ssml=False)
        self.assertEqual(
            w.render(),
            {
                "platform": "google",
                "type": "simple_response",
                "displayText": text,
                "speech": speech
            }
        )

    def test_validation(self):
        with self.assertRaises(InvalidGoogleAssistantWidget):
            SimpleResponseWidget(None, None)

    def test_text(self):
        speech = "foo"
        w = SimpleResponseWidget(speech, None)
        self.assertEqual(
            w.render(),
            {
                "platform": "google",
                "type": "simple_response",
                "displayText": speech,
                "speech": w.ssml_format(speech)
            }
        )


if __name__ == '__main__':
    unittest.main()

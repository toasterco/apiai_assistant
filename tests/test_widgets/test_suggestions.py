import unittest

from apiai_assistant import Platforms
from apiai_assistant.widgets import WidgetTypes
from apiai_assistant.widgets import SuggestionsWidget


class SuggestionsWidgetTestCase(unittest.TestCase):
    def test_google_basic(self):
        suggestions = ["Yes", "No"]
        w = SuggestionsWidget(suggestions)
        origin = Platforms.GOOGLE_ASSISTANT
        self.assertEqual(
            w.render(origin),
            {
                "type": "suggestion_chips",
                "platform": "google",
                "suggestions": [
                    {"title": "Yes"},
                    {"title": "No"},
                ]
            }
        )

    def test_google_no_suggestions(self):
        w = SuggestionsWidget(None)
        origin = Platforms.GOOGLE_ASSISTANT
        self.assertEqual(
            w.render(origin),
            {
                "type": "suggestion_chips",
                "platform": "google",
                "suggestions": []
            }
        )

    def test_api_ai_basic(self):
        suggestions = ["Yes", "No"]
        w = SuggestionsWidget(suggestions)
        origin = Platforms.FACEBOOK_MESSENGER
        self.assertEqual(
            w.render(origin),
            {
                "type": WidgetTypes.Suggestions,
                "platform": origin,
                "replies": suggestions,
                "title": "Please pick one"
            }
        )

    def test_api_ai_no_suggestions(self):
        w = SuggestionsWidget(None)
        origin = Platforms.FACEBOOK_MESSENGER
        self.assertEqual(
            w.render(origin),
            {
                "type": WidgetTypes.Suggestions,
                "platform": origin,
                "replies": [],
                "title": "Please pick one"
            }
        )

    def test_amazon_basic(self):
        suggestions = ["Yes", "No"]
        w = SuggestionsWidget(suggestions)
        origin = Platforms.AMAZON_ALEXA
        self.assertEqual(w.render(origin), {})


if __name__ == '__main__':
    unittest.main()

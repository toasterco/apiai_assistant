import unittest

from apiaiassistant.widgets import SuggestionsWidget


class SuggestionsWidgetTestCase(unittest.TestCase):
    def test_basic(self):
        suggestions = ["Yes", "No"]
        w = SuggestionsWidget(suggestions)
        self.assertEqual(
            w.render(),
            {
                "type": "suggestion_chips",
                "platform": "google",
                "suggestions": [
                    {"title": "Yes"},
                    {"title": "No"},
                ]
            }
        )

    def test_no_suggestions(self):
        w = SuggestionsWidget(None)
        self.assertEqual(
            w.render(),
            {
                "type": "suggestion_chips",
                "platform": "google",
                "suggestions": []
            }
        )


if __name__ == '__main__':
    unittest.main()

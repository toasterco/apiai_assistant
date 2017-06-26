import unittest

from apiaiassistant.widgets import GoogleAssistantWidget


class GoogleAssistantWidgetTestCase(unittest.TestCase):
    def test_basic(self):
        w = GoogleAssistantWidget()
        self.assertEqual(w.platform, 'google')
        self.assertEqual(w.render(), {'platform': 'google'})


if __name__ == '__main__':
    unittest.main()

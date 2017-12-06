import unittest

from apiai_assistant import Platforms
from apiai_assistant.widgets import GoogleAssistantLinkOutChipWidget


class GoogleAssistantLinkOutChipWidgetTestCase(unittest.TestCase):
    def test_basic(self):
        title = "foo"
        url = "bar.com"
        w = GoogleAssistantLinkOutChipWidget(title, url)
        self.assertEqual(
            w.render(Platforms.GOOGLE_ASSISTANT),
            {
                "platform": "google",
                "type": "link_out_chip",
                "title": title,
                "url": url
            }
        )


if __name__ == '__main__':
    unittest.main()

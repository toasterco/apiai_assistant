import unittest

from apiai_assistant.widgets import LinkOutChipWidget


class LinkOutChipWidgetTestCase(unittest.TestCase):
    def test_basic(self):
        title = "foo"
        url = "bar.com"
        w = LinkOutChipWidget(title, url)
        self.assertEqual(
            w.render(),
            {
                "platform": "google",
                "type": "link_out_chip",
                "title": title,
                "url": url
            }
        )


if __name__ == '__main__':
    unittest.main()

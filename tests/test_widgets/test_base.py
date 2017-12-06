import mock
import unittest

from apiai_assistant import Platforms
from apiai_assistant.widgets import BaseWidget
from apiai_assistant.widgets import GoogleAssistantWidget


class GoogleAssistantWidgetTestCase(unittest.TestCase):
    def test_basic(self):
        w = GoogleAssistantWidget()
        self.assertEqual(w.platform, 'google')
        self.assertEqual(w.render(Platforms.GOOGLE_ASSISTANT), {'platform': 'google'})


class BaseWidgetTestCase(unittest.TestCase):
    @mock.patch.object(BaseWidget, 'render_amazon_alexa')
    @mock.patch.object(BaseWidget, 'render_google_assistant')
    @mock.patch.object(BaseWidget, 'render_api_ai')
    def test_basic(self,
                   mocked_render_api_ai,
                   mocked_render_google_assistant,
                   mocked_render_amazon_alexa):

        w = BaseWidget()

        w.render(Platforms.API_AI)
        self.assertEqual(mocked_render_api_ai.call_count, 1)
        self.assertEqual(mocked_render_amazon_alexa.call_count, 0)
        self.assertEqual(mocked_render_google_assistant.call_count, 0)

        w.render(Platforms.FACEBOOK_MESSENGER)
        self.assertEqual(mocked_render_api_ai.call_count, 2)
        self.assertEqual(mocked_render_amazon_alexa.call_count, 0)
        self.assertEqual(mocked_render_google_assistant.call_count, 0)

        w.render(Platforms.SLACK_BOT)
        self.assertEqual(mocked_render_api_ai.call_count, 3)
        self.assertEqual(mocked_render_amazon_alexa.call_count, 0)
        self.assertEqual(mocked_render_google_assistant.call_count, 0)

        w.render(Platforms.GOOGLE_ASSISTANT)
        self.assertEqual(mocked_render_api_ai.call_count, 3)
        self.assertEqual(mocked_render_amazon_alexa.call_count, 0)
        self.assertEqual(mocked_render_google_assistant.call_count, 1)

        w.render(Platforms.AMAZON_ALEXA)
        self.assertEqual(mocked_render_api_ai.call_count, 3)
        self.assertEqual(mocked_render_amazon_alexa.call_count, 1)
        self.assertEqual(mocked_render_google_assistant.call_count, 1)

    def test_renders(self):
        w = BaseWidget()

        self.assertEqual(w.render(Platforms.AMAZON_ALEXA), {})
        self.assertEqual(w.render(Platforms.FACEBOOK_MESSENGER), {})
        self.assertEqual(w.render(Platforms.SLACK_BOT), {})
        self.assertEqual(w.render(Platforms.API_AI), {})
        self.assertEqual(w.render(Platforms.GOOGLE_ASSISTANT), {})

if __name__ == '__main__':
    unittest.main()

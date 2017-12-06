from .. import Platforms
from .. import utils

WidgetTypes = utils.enum(Image=3, Text=0, Card=1, Suggestions=2)


class InvalidWidget(Exception):
    pass


class InvalidGoogleAssistantWidget(Exception):
    pass


class BaseWidget(object):
    def render(self, origin):
        renderers = {
            Platforms.API_AI: self.render_api_ai,
            Platforms.GOOGLE_ASSISTANT: self.render_google_assistant,
            Platforms.AMAZON_ALEXA: self.render_amazon_alexa,
        }

        renderer = renderers.get(origin)
        if renderer:
            return renderer(origin)
        else:
            return self.render_api_ai(origin)

    def render_amazon_alexa(self, origin):
        return {}

    def render_google_assistant(self, origin):
        return {}

    def render_api_ai(self, origin):
        return {}


class GoogleAssistantWidget(BaseWidget):
    def __init__(self):
        self.platform = 'google'

    def render_google_assistant(self, origin):
        return {
            'platform': self.platform
        }

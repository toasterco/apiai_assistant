from . import WidgetTypes
from . import BaseWidget


class Button(BaseWidget):
    def __init__(self, title, weblink=None):
        self.title = title
        self.weblink = weblink

        super(Button, self).__init__()

    def render_api_ai(self, origin):
        return {
            'postback': self.weblink,
            'text': self.title
        }

    def render_google_assistant(self, origin):
        return {
            'title': self.title,
            'openUrlAction': {
                'url': self.weblink,
            }
        }


class Image(BaseWidget):
    def __init__(self, url, alt=None):
        self.url = url
        self.alt = alt

        super(Image, self).__init__()

    def render_api_ai(self, origin):
        return {
            'type': WidgetTypes.Image,
            'platform': origin,
            'imageUrl': self.url
        }

    def render_google_assistant(self, origin):
        return {
            'url': self.url,
            'accessibilityText': self.alt
        }

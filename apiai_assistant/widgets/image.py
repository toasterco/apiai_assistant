from . import GoogleAssistantWidget


class Button(GoogleAssistantWidget):
    def __init__(self, title, weblink=None):
        self.title = title
        self.weblink = weblink

        super(Button, self).__init__()

    def render(self):
        return {
            'title': self.title,
            'openUrlAction': {
                'url': self.weblink,
            }
        }


class Image(GoogleAssistantWidget):
    def __init__(self, url, alt=None):
        self.url = url
        self.alt = alt

        super(Image, self).__init__()

    def render(self):
        return {'url': self.url, 'accessibilityText': self.alt}

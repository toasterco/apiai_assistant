from . import WidgetTypes
from . import BaseWidget
from . import InvalidWidget


class ImageCardWidget(BaseWidget):
    def __init__(self,
                 title,
                 text=None, image=None, button=None):
        self.title = title

        if text is None and image is None:
            raise InvalidWidget(
                'Please specify at least text or image'
            )

        self.text = text
        self.image = image
        self.button = button

    def render_api_ai(self, origin):
        return {
            'buttons': [self.button.render(origin)] if self.button else [],
            'imageUrl': self.image.url if self.image else None,
            'platform': origin,
            'subtitle': self.text,
            'title': self.title,
            'type': WidgetTypes.Card
        }

    def render_amazon_alexa(self, origin):
        payload = {'title': self.title}

        if not self.image or not self.image.url:
            payload['type'] = 'Simple'
            payload['content'] = self.text
        else:
            payload['type'] = 'Standard'
            payload['text'] = self.text
            payload['image'] = {
                'smallImageUrl': self.image.url,
                'largeImageUrl': self.image.url
            }

        return payload

    def render_google_assistant(self, origin):
        return {
            'platform': origin,
            'type': 'basic_card',
            'title': self.title,
            'formattedText': self.text,
            'image': self.image.render(origin) if self.image else None,
            'buttons': [self.button.render(origin)] if self.button else []
        }

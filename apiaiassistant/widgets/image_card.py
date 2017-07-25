from . import GoogleAssistantWidget
from . import InvalidGoogleAssistantWidget


class ImageCardWidget(GoogleAssistantWidget):
    def __init__(self,
                 title,
                 text=None, image=None, button=None):
        self.title = title

        if text is None and image is None:
            raise InvalidGoogleAssistantWidget(
                'Please specify at least text or image'
            )

        self.text = text
        self.image = image
        self.button = button
        self.type = 'basic_card'

        super(ImageCardWidget, self).__init__()

    def render(self):
        payload = super(ImageCardWidget, self).render()

        payload.update({
            'type': self.type,
            'title': self.title,
            'formattedText': self.text,
            'image': self.image.render() if self.image else None,
            'buttons': [self.button.render()] if self.button else []
        })

        return payload


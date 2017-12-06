from . import GoogleAssistantWidget


class GoogleAssistantCarouselSelectWidget(GoogleAssistantWidget):
    def __init__(self, items):
        self.items = items
        self.type = 'carousel_card'

        super(GoogleAssistantCarouselSelectWidget, self).__init__()

    def render_google_assistant(self, origin):
        payload = super(GoogleAssistantCarouselSelectWidget, self).render_google_assistant(origin)

        payload.update({
            'type': self.type,
            'items': [item.render(origin) for item in self.items]
        })

        return payload

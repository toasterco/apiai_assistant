from . import GoogleAssistantWidget


class GoogleAssistantListSelectWidget(GoogleAssistantWidget):
    def __init__(self, items, title=None):
        self.title = title
        self.items = items
        self.type = 'list_card'

        super(GoogleAssistantListSelectWidget, self).__init__()

    def render_google_assistant(self, origin):
        payload = super(GoogleAssistantListSelectWidget, self).render_google_assistant(origin)

        payload.update({
            'type': self.type,
            'title': self.title,
            'items': [item.render(origin) for item in self.items]
        })

        return payload

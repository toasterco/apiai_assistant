from . import GoogleAssistantWidget


class GoogleAssistantLinkOutChipWidget(GoogleAssistantWidget):
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.type = 'link_out_chip'

        super(GoogleAssistantLinkOutChipWidget, self).__init__()

    def render_google_assistant(self, origin):
        payload = super(GoogleAssistantLinkOutChipWidget, self).render_google_assistant(origin)

        payload.update({
            'type': self.type,
            'title': self.title,
            'url': self.url
        })

        return payload

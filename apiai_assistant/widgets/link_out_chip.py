from . import GoogleAssistantWidget


class LinkOutChipWidget(GoogleAssistantWidget):
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.type = 'link_out_chip'

        super(LinkOutChipWidget, self).__init__()

    def render(self):
        payload = super(LinkOutChipWidget, self).render()

        payload.update({
            'type': self.type,
            'title': self.title,
            'url': self.url
        })

        return payload

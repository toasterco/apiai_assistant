from . import GoogleAssistantWidget


class ListSelectWidget(GoogleAssistantWidget):
    def __init__(self, items, title=None):
        self.title = title
        self.items = items
        self.type = 'list_card'

        super(ListSelectWidget, self).__init__()

    def render(self):
        payload = super(ListSelectWidget, self).render()

        payload.update({
            'type': self.type,
            'title': self.title,
            'items': [item.render() for item in self.items]
        })

        return payload

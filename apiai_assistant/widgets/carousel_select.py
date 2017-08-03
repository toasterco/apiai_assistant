from . import GoogleAssistantWidget


class CarouselSelectWidget(GoogleAssistantWidget):
    def __init__(self, items):
        self.items = items
        self.type = 'carousel_card'

        super(CarouselSelectWidget, self).__init__()

    def render(self):
        payload = super(CarouselSelectWidget, self).render()

        payload.update({
            'type': self.type,
            'items': [item.render() for item in self.items]
        })

        return payload

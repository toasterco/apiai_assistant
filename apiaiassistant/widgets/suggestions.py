from . import GoogleAssistantWidget


class SuggestionsWidget(GoogleAssistantWidget):
    def __init__(self, suggestions):
        self.suggestions = suggestions or []
        self.type = 'suggestion_chips'

        super(SuggestionsWidget, self).__init__()

    def render(self):
        payload = super(SuggestionsWidget, self).render()

        payload.update({
            'type': self.type,
            'suggestions': [
                {'title': suggestion}
                for suggestion in self.suggestions
            ]
        })

        return payload

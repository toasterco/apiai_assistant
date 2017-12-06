from . import BaseWidget
from . import WidgetTypes


class SuggestionsWidget(BaseWidget):
    def __init__(self, suggestions):
        self.suggestions = suggestions or []

    def render_google_assistant(self, origin):
        return {
            'platform': origin,
            'type': 'suggestion_chips',
            'suggestions': [
                {'title': suggestion}
                for suggestion in self.suggestions
            ]
        }

    def render_api_ai(self, origin):
        return {
            'platform': origin,
            'replies': self.suggestions,
            'title': 'Please pick one',
            'type': WidgetTypes.Suggestions
        }

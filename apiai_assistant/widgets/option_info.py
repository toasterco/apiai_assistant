from . import GoogleAssistantWidget
from . import InvalidGoogleAssistantWidget


class GoogleAssistantOptionInfo(GoogleAssistantWidget):
    def __init__(self, key, synonyms=None):
        if key is None and synonyms is None:
            raise InvalidGoogleAssistantWidget(
                'Please specify at least key or synonyms')

        self.key = key
        self.synonyms = synonyms or []

    def render_google_assistant(self, origin):
        return {
            'key': self.key,
            'synonyms': self.synonyms
        }

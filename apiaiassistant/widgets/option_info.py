from . import GoogleAssistantWidget
from . import InvalidGoogleAssistantWidget


class OptionInfo(GoogleAssistantWidget):
    def __init__(self, key, synonyms=None):
        if key is None and synonyms is None:
            raise InvalidGoogleAssistantWidget(
                'Please specify at least key or synonyms')

        self.key = key
        self.synonyms = synonyms or []

    def render(self):
        return {
            'key': self.key,
            'synonyms': self.synonyms
        }

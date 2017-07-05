from . import GoogleAssistantWidget
from . import InvalidGoogleAssistantWidget


class SimpleResponseWidget(GoogleAssistantWidget):
    def __init__(self, speech, text, ssml=True):
        self.speech = speech
        self.text = text
        if text is None:
            self.text = speech

        if speech is None and text is None:
            raise InvalidGoogleAssistantWidget(
                'Please at least specify text or speech')

        self.type = 'simple_response'
        self._ssml = ssml

        super(SimpleResponseWidget, self).__init__()

    def ssml_format(self, s):
        return '<speak>{}</speak>'.format(s)

    def render(self):
        payload = super(SimpleResponseWidget, self).render()

        payload.update({
            'type': self.type,
            'displayText': self.text,
            'speech': self.ssml_format(self.speech) if self._ssml else self.speech
        })

        return payload

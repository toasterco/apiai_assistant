from . import BaseWidget
from . import WidgetTypes
from . import InvalidWidget


class SimpleResponseWidget(BaseWidget):
    def __init__(self, speech, text, ssml=True):
        self.speech = speech
        self.text = text
        if text is None:
            self.text = speech

        if speech is None and text is None:
            raise InvalidWidget(
                'Please at least specify text or speech')

        self._ssml = ssml

        super(SimpleResponseWidget, self).__init__()

    def ssml_format(self, s):
        return '<speak>{}</speak>'.format(s)

    def render_api_ai(self, origin):
        return {
            'platform': origin,
            'speech': self.text,
            'type': WidgetTypes.Text
        }

    def render_amazon_alexa(self, origin):
        payload = {
            'type': 'PlainText',
            'text': self.text,
        }
        if self._ssml:
            payload['type'] = 'SSML'
            payload['ssml'] = self.ssml_format(self.speech)

        return {'outputSpeech': payload}

    def render_google_assistant(self, origin):
        payload = {
            'platform': origin,
            'displayText': self.text,
            'type': 'simple_response'
        }

        if self._ssml:
            payload['ssml'] = self.ssml_format(self.speech)
        else:
            payload['textToSpeech'] = self.speech

        return payload

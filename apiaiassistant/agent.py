from . import utils
from . import parser
from . import widgets


Status = utils.enum('OK', 'KO')


class Response(object):
    def __init__(self):
        self.expect_user_response = False
        self._messages = [
            {"type": 0, "speech": ""}
        ]
        self._contexts = []

    def close_mic(self):
        self.expect_user_response = False

    def open_mic(self):
        self.expect_user_response = True

    def add_message(self, message, position=None):
        if position is not None:
            self._messages.insert(position, message)
        else:
            self._messages.append(message)

    def add_context(self, context, position=None):
        if position is not None:
            self._contexts.insert(position, context)
        else:
            self._contexts.append(context)

    def to_dict(self):
        payload = {
            'messages': self._messages,
            'data': {
                'google': {
                    'expectUserResponse': self.expect_user_response
                }
            }
        }

        if self._contexts:
            payload['contextOut'] = self._contexts

        return payload


class Agent(object):
    def __init__(self, corpus=None, request=None, ssml=True, *args, **kwargs):
        self.code = Status.OK
        self.error_message = None

        self._ssml = ssml

        self.corpus = corpus
        self.parser = parser.get_parser(request)

        self.response = Response()

    def __repr__(self):
        return '<Agent: ({}{})>'.format(
            self.code,
            '- {}'.format(self.error_message) if self.code != Status.OK else ''
        )

    def tell(self, speech, text=None):
        # Resolve corpus id here and format or w/e

        self.tell_raw(speech, text)

    def ask(self, speech, text=None):
        # Resolve corpus id here and format or w/e

        self.ask_raw(speech, text)

    def suggest(self, suggestions):
        # Resolve corpus id here and format or w/e

        self.suggest_raw(suggestions)

    def tell_raw(self, speech, text=None):
        self.response.close_mic()

        widget = widgets.SimpleResponseWidget(speech, text, ssml=self._ssml)
        self.response.add_message(widget.render())

    def ask_raw(self, speech, text=None):
        self.response.open_mic()

        widget = widgets.SimpleResponseWidget(speech, text, ssml=self._ssml)
        self.response.add_message(widget.render())

    def suggest_raw(self, suggestions):
        if type(suggestions) != list:
            suggestions = [suggestions]

        suggestion_widget = widgets.SuggestionsWidget(suggestions)

        self.show(suggestion_widget)

    def show(self, obj):
        message = obj.render()

        self.response.add_message(message)

    def add_context(self, context_name, parameters=None, lifespan=5):
        self.response.add_context({
            "name": context_name,
            "lifespan": lifespan,
            "parameters": parameters or {}
        })

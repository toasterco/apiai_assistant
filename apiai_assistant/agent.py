""" API.ai Agent

This module provides a Agent class to be used within an Assistant class
implementation to be able to interact with the user through the agent """


from . import utils
from . import parser
from . import widgets


Status = utils.enum(
    'OK',
    'GenericError', 'InvalidData', 'NotImplemented',
    'Aborted', 'AccessDenied')
""" :obj:`apiai_assistant.utils.enum`: statuses of the agent """


class Agent(object):
    """
    Provides methods to instruct the agent on how to respond tu user queries

    Args:
        corpus (:obj:`apiai_assistant.corpus.Corpus`): Corpus to get the outputs from
        request (:obj:`dict`, optional): API.ai request
        ssml (boolean, optional, True): if True, will format speech to support SSML
    """

    SupportedPermissions = utils.enum(
        'NAME', 'COARSE_LOCATION', 'PRECISE_LOCATION')
    """ :obj:`apiai_assistant.utils.enum`: permissions supported by the agent """

    def __init__(self, corpus=None, request=None, ssml=True, *args, **kwargs):
        self.code = Status.OK
        self.error_message = None
        self._ssml = ssml

        self.corpus = corpus
        self.parser = None
        if request:
            self.parser = parser.GoogleAssistantParser(request)

        self.response = Response()

    def __repr__(self):
        return '<Agent: ({}{})>'.format(
            Status.by_value.get(self.code),
            ' - {}'.format(self.error_message) if self.code != Status.OK else ''
        )

    def abort(self, reason):
        self.code = Status.Aborted
        self.error_message = reason

        self.response.abort(self.error_message, self.code)

    def error(self, error_message, code=Status.GenericError):
        self.code = code
        self.error_message = error_message

        self.response.abort(error_message)

    def tell(self, corpus_id, context=None):
        """
        Looks for the output id in the corpus and formats with the context

        Args:
            corpus_id (str): ID of the output to tell
            context (:obj:`dict`, optional): context to format the output with
        """

        output = self.corpus[corpus_id]
        if context is not None:
            output = output.format(**context)

        self.tell_raw(output)

    def ask(self, corpus_id, context=None):
        """
        Looks for the output id in the corpus and formats with the context

        Args:
            corpus_id (str): ID of the output to ask
            context (:obj:`dict`, optional): context to format the output with
        """

        output = self.corpus[corpus_id]
        if context is not None:
            output = output.format(**context)

        self.ask_raw(output)

    def suggest(self, corpus_id):
        """
        Looks for the output id in the corpus to suggest

        Args:
            corpus_id (str): ID of the suggestions to show
        """

        suggestions = self.corpus.get(corpus_id, self.corpus.suggestions)

        if suggestions:
            self.suggest_raw(suggestions)

    def tell_raw(self, speech, text=None):
        """
        Tells the user by adding the speech and/or text to the response's messages

        Args:
            speech (str): speech to tell
            text (str, optional): text to tell, if None, speech will be used
        """

        self.response.close_mic()

        widget = widgets.SimpleResponseWidget(speech, text, ssml=self._ssml)
        self.show(widget)

    def ask_raw(self, speech, text=None):
        """
        Asks the user by adding the speech and/or text to the response's messages

        Args:
            speech (str): speech to ask
            text (str, optional): text to ask, if None, speech will be used
        """

        self.response.open_mic()

        widget = widgets.SimpleResponseWidget(speech, text, ssml=self._ssml)
        self.show(widget)

    def suggest_raw(self, suggestions):
        """
        Suggests the user by adding the suggestions to the response's messages

        Args:
            suggestions (:obj:`list`): suggestions
        """

        if type(suggestions) != list:
            suggestions = [suggestions]

        suggestion_widget = widgets.SuggestionsWidget(suggestions)

        self.show(suggestion_widget)

    def show(self, obj):
        """
        Renders a rich response widget and add it to the response's messages
        """

        message = obj.render()

        self.response.add_message(message)

    def add_context(self, context_name, parameters=None, lifespan=5):
        """
        Adds a context to the response's contexts

        Args:
            context_name (str): name of the context to add
            parameters (:obj:`dict`, optional): parameters of the context
            lifespan (:obj:`int`, optional, 5): lifespan of the context
        """

        self.response.add_context({
            'name': context_name,
            'lifespan': lifespan,
            'parameters': parameters or {}
        })

    def ask_for_permissions(self, reason, permissions):
        self.response.add_permission(reason, permissions)

    def ask_for_confirmation(self, corpus_id):
        self.ask(corpus_id)
        self.suggest_raw(self.corpus.get_confirmation())

    def ask_for_confirmation_raw(self, question):
        self.ask_raw(question)
        self.suggest_raw(self.corpus.get_confirmation())


class Response(object):
    """ Abstraction to build API.ai compatible responses """

    PERMISSIONS = {
        Agent.SupportedPermissions.NAME: 'NAME',
        Agent.SupportedPermissions.COARSE_LOCATION: 'DEVICE_COARSE_LOCATION',
        Agent.SupportedPermissions.PRECISE_LOCATION: 'DEVICE_PRECISE_LOCATION'
    }

    def __init__(self):
        self.code = Status.OK
        self.error_message = None
        self.expect_user_response = False
        self._messages = [
            self.initial_message
        ]
        self._permissions = []
        self._contexts = []

    @property
    def initial_message(self):
        return {'type': 0, 'speech': ''}

    def abort(self, error_message, code=Status.GenericError):
        self.code = code
        self.error_message = error_message

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

    def add_permission(self, reason, permissions):
        self._permissions.append((reason, [self.PERMISSIONS[p] for p in permissions]))

    def to_dict(self):
        if self.code != Status.OK:
            return {'error': '400'}

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

        if self._permissions:
            reason = self._permissions[0][0]
            permissions = list(
                {p for _, perms in self._permissions for p in perms})

            payload['data']['google']['systemIntent'] = {
                "intent": "actions.intent.PERMISSION",
                "data": {
                    "@type": "type.googleapis.com/google.actions.v2.PermissionValueSpec",
                    "optContext": reason,
                    "permissions": permissions
                }

            }

        return payload

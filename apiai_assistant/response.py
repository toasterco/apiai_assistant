""" Response.

Provides Response classes for API.ai integrations
to build responses according to their respective format
"""

import agent
from . import Platforms


class BaseResponse(object):
    """ Abstraction to build API.ai compatible responses """
    def __init__(self):
        self.code = agent.Status.OK
        self.error_message = None
        self.expect_user_response = False
        self._messages = []
        self._contexts = []
        self._permissions = []

    @property
    def error_payload(self):
        return {'error': '400'}

    def abort(self, error_message, code=agent.Status.GenericError):
        self.code = code
        self.error_message = error_message

    def close_mic(self):
        self.expect_user_response = False

    def open_mic(self):
        self.expect_user_response = True

    def add_message(self, message, position=None):
        if position is not None and message:
            self._messages.insert(position, message)
        elif message:
            self._messages.append(message)

    def add_context(self, context, position=None):
        if position is not None:
            self._contexts.insert(position, context)
        else:
            self._contexts.append(context)

    def add_permission(self, reason, permissions):
        """ Implement permission handling if supported """
        pass

    def to_dict(self):
        if self.code != agent.Status.OK:
            return self.error_payload

        payload = {
            'messages': self._messages,
        }

        if self._contexts:
            payload['contextOut'] = self._contexts

        return payload


class GoogleAssistantResponse(BaseResponse):
    PERMISSIONS = {
        agent.Agent.SupportedPermissions.NAME: 'NAME',
        agent.Agent.SupportedPermissions.COARSE_LOCATION: 'DEVICE_COARSE_LOCATION',
        agent.Agent.SupportedPermissions.PRECISE_LOCATION: 'DEVICE_PRECISE_LOCATION'
    }

    def __init__(self):
        super(GoogleAssistantResponse, self).__init__()

        self._messages = [
            self.initial_message
        ]
        self._permissions = []

    def add_permission(self, reason, permissions):
        self._permissions.append(
            (reason, [self.PERMISSIONS[p] for p in permissions])
        )

    @property
    def initial_message(self):
        return {'type': 0, 'speech': ''}

    def to_dict(self):
        payload = super(GoogleAssistantResponse, self).to_dict()

        if self.code != agent.Status.OK:
            return self.error_payload

        payload['data'] = {
            'google': {
                'expectUserResponse': self.expect_user_response
            }
        }

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


class AmazonAlexaResponse(BaseResponse):
    def to_dict(self):
        payload = {
            "version": "1.0",
            "response": {
                "shouldEndSession": not self.expect_user_response,
            }
        }

        for message in self._messages:
            key = message.keys()[0]
            payload['response'][key] = message[key]

        return payload

RESPONSES = {
    Platforms.API_AI: GoogleAssistantResponse,
    Platforms.GOOGLE_ASSISTANT: GoogleAssistantResponse,
    Platforms.AMAZON_ALEXA: AmazonAlexaResponse
}


def get_response(origin):
    response = RESPONSES.get(origin, BaseResponse)
    if response:
        response = response()
    return response

import json
from . import utils


def get_parser(request, magic_key=None):
    if not request:
        return None

    r_magic_key = request.headers.get('magic-key')
    if r_magic_key and magic_key and r_magic_key != magic_key:
        return None

    data = json.loads(request.body)
    return GoogleAssistantParser(data)


class User(object):
    def __init__(self, name, user_id):
        self.name = name
        self.id = user_id


class PayloadParser(object):
    PARAM_TYPES = utils.enum('NUMBER', 'STRING', 'LIST')

    def __init__(self, data):
        self.data = data
        self._user = None

    def get(self, param, _type=None, default=None, globbing=False):
        # Useful for numerated param names (i.e.: give-name, given-name2, etc)
        if globbing:
            value = [
                _value
                for field, _value in self.parameters.items()
                if field.startswith(param)]
        else:
            value = self.parameters.get(param)

        if _type == self.PARAM_TYPES.NUMBER:
            if isinstance(value, list):
                value = map(utils.text_to_int, value)
            else:
                value = default if not value else utils.text_to_int(value)

        return value


class GoogleAssistantParser(PayloadParser):

    CAPABILITIES = {
        'screen': 'actions.capability.SCREEN_OUTPUT',
        'audio': 'actions.capability.AUDIO_OUTPUT'
    }

    PERMISSIONS = {
        'name': 'NAME',
        'coarse_loc': 'DEVICE_COARSE_LOCATION',
        'precise_loc': 'DEVICE_PRECISE_LOCATION',
    }

    @property
    def action(self):
        return self.request.get('action')

    @property
    def parameters(self):
        return self.request.get('parameters', {})

    def get_contexts(self, name=None):
        contexts = self.request.get('contexts', [])
        if name:
            for context in contexts:
                if context['name'] == name:
                    return context['parameters']
            return {}
        return contexts

    @property
    def request(self):
        return self.data.get('result', {})

    def has_screen_capability(self):
        return self.CAPABILITIES['screen'] in self.capabilities

    def has_audio_capability(self):
        return self.CAPABILITIES['audio'] in self.capabilities

    @property
    def capabilities(self):
        try:
            return [
                c['name'] for c in self.data['originalRequest']['data']['surface']['capabilities']
            ]
        except:
            return []

    @property
    def user(self):
        if self._user is None:
            self._user = self._init_user()
        return self._user

    def _init_user(self):
        name = 'APIAITEST'
        user_id = 'APIAITEST'

        user = self.data.get(
            'originalRequest', {}).get('data', {}).get('user', {})
        if user:
            name = user['userName']
            user_id = user['userId']

        return User(name=name, user_id=user_id)

""" Parser.

Provides Actions on Google Parser classes to read from the API.ai POST
request payload and offers abstractions to access objects of the payload
"""


from . import utils

DEFAULT_LOCALE = 'en-US'
DEFAULT_USER_ID = 'APIAITEST'


class User(object):
    """
    A simple user class used to encapsulate the user object from the request

    Args:
        user_id (str): uid of the user
        locale (str): locale of the user
        display_name (str): display name of the user
        given_name (str): given name of the user (first name)
        family_name (str): family name of the user (last name)
        device (:obj:`Device`): device of the user
    """

    def __init__(
            self,
            user_id=DEFAULT_USER_ID, locale=DEFAULT_LOCALE,
            display_name=None, given_name=None, family_name=None,
            device=None):
        self.display_name = display_name
        self.id = user_id
        self.given_name = given_name
        self.family_name = family_name
        self.device = device
        self.locale = locale

class Device(object):
    """
    A simple device class used to encapsulate the device object from the reuqest

    Args:
        device_id (str): unique id of the device
        coordinates (:obj:`dict`): longitude and latitude of device location
        address (str): formatted address of the device
        city (str): city of the device
        zip_code (str): zip_code of the device
        phone_number (str): phone number of the device location
        notes (str): notes about the device location
    """

    def __init__(self,
                 device_id=None, coordinates=None, address=None,
                 city=None, zip_code=None, phone_number=None, notes=None):
        self.id = device_id
        self.coordinates = coordinates
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.notes = notes


class PayloadParser(object):
    """
    Base class for all PayloadParser

    Args:
        data (:obj:`dict`): POST payload from API.ai
    """

    PARAM_TYPES = utils.enum('NUMBER', 'STRING', 'LIST')

    def __init__(self, data):
        self.data = data or {}
        self._user = None

    @property
    def is_valid(self):
        """
        Validation method, called in apiai_assistant.assistant.Assistant.process

        Returns:
            bool: True if the parser is valid. False otherwise
        """

        raise NotImplementedError

    def get(self, param, default=None, _type=None, globbing=False):
        """
        General getter to access parameters inside the API.ai request

        Args:
            param (str): key of the parameter to get
            default (*, optional, None): default value if the parameter
                                         couldn't be found
            _type (:obj:`PARAM_TYPES`, optional): type of the parameter, mostly
                                                  needed when getting a number
                                                  parameter
            globbing (bool, optional, False): if true, will also get all the
                                              duplicated parameters

        Returns:
            *: the value of the parameter
        """

        # Useful for numerated param names (i.e.: give-name, given-name2, etc)
        if globbing:
            value = [
                _value
                for field, _value in self.parameters.items()
                if field.startswith(param)]
        else:
            value = self.parameters.get(param, default)

        if _type == self.PARAM_TYPES.NUMBER:
            if isinstance(value, list) and value:
                value = map(utils.text_to_int, value)
            else:
                value = default if not value else utils.text_to_int(value)

        return value


class GoogleAssistantParser(PayloadParser):
    """ Parser for the Actions on Google integration """

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
    def is_valid(self):
        return not not self.request

    @property
    def action(self):
        return self.request.get('action')

    @property
    def parameters(self):
        return self.request.get('parameters', {})

    def get_contexts(self, name=None):
        """ Get the contexts of the request or the context with name `name`

        Args:
            name (str, optional): name of the context to get
        Returns:
            list of contexts if `name` is None, otherwise the context with name
            `name` or an empty :obj:`dict` if it couldn't be found
        """

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
        except KeyError:
            return []

    @property
    def user(self):
        if self._user is None:
            self._user = self._init_user()
        return self._user

    @property
    def device(self):
        if self._user is None:
            self._user = self._init_user()
        return self._user.device

    def _init_user(self):
        """
        Initialise the user instance.

        If the user object can't be found in the request it is assumed
        that we are in a test environment and thus use dummy strings
        """

        data = self.data.get(
            'originalRequest', {}).get('data', {})
        device_data = data.get('device', {})
        user_data = data.get('user', {})

        device = Device(
            device_id=device_data.get('uniqueDeviceId'),
            coordinates=device_data.get('location', {}).get('coordinates'),
            address=device_data.get('location', {}).get('formattedAddress'),
            city=device_data.get('location', {}).get('city'),
            zip_code=device_data.get('location', {}).get('zipCode'),
            phone_number=device_data.get('location', {}).get('phoneNumber'),
            notes=device_data.get('location', {}).get('notes'))

        return User(
            locale=user_data.get('locale', DEFAULT_LOCALE),
            user_id=user_data.get('userId', DEFAULT_USER_ID),
            display_name=user_data.get('profile', {}).get('displayName'),
            given_name=user_data.get('profile', {}).get('givenName'),
            family_name=user_data.get('profile', {}).get('familyName'),
            device=device)

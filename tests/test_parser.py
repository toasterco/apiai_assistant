import unittest

from apiai_assistant import Platforms
from apiai_assistant.parser import get_parser
from apiai_assistant.parser import WELCOME_ACTION
from apiai_assistant.parser import PayloadParser
from apiai_assistant.parser import GoogleAssistantParser
from apiai_assistant.parser import AmazonAlexaParser

from tests import get_dummy_google_request
from tests import get_dummy_amazon_request


class PayloadParserTestCase(unittest.TestCase):
    def test_is_valid_not_implemented(self):
        parser = PayloadParser({})
        with self.assertRaises(NotImplementedError):
            parser.is_valid

    def test_get_parser(self):
        self.assertEqual(
            type(get_parser(Platforms.API_AI, {})),
            GoogleAssistantParser)
        self.assertEqual(
            type(get_parser(Platforms.FACEBOOK_MESSENGER, {})),
            GoogleAssistantParser)
        self.assertEqual(
            type(get_parser(Platforms.SLACK_BOT, {})),
            GoogleAssistantParser)
        self.assertEqual(
            type(get_parser(Platforms.AMAZON_ALEXA, {})),
            AmazonAlexaParser)
        self.assertEqual(
            type(get_parser(Platforms.GOOGLE_ASSISTANT, {})),
            GoogleAssistantParser)
        self.assertEqual(get_parser(None, {}), None)


class GoogleAssistantParserTestCase(unittest.TestCase):
    def setUp(self):
        self.request = get_dummy_google_request()

    def test_is_valid(self):
        parser = GoogleAssistantParser(self.request)
        self.assertTrue(parser.is_valid)

        parser.data = {}
        self.assertFalse(parser.is_valid)

    def test_action(self):
        action = 'foobar'
        self.request['result']['action'] = action

        parser = GoogleAssistantParser(self.request)
        self.assertEqual(parser.action, action)

    def test_parameters(self):
        self.request['result']['parameters'] = {
            "given-name": "Zack",
            "given-name2": "Alberto",
            "given-name3": "Dom",
            "ordinal": "33rd",
            "number": "thirty-three",
            "other-ordinal": "thirty third",
            "number-list": ["2nd", "second"],
            "names": "Zack Alberto Dom Martina",
            "names2": "Zack,Alberto,Dom,Martina"
        }

        parser = GoogleAssistantParser(self.request)
        self.assertEqual(parser.get('given-name'), "Zack")
        self.assertEqual(
            set(parser.get('given-name', globbing=True)),
            {"Zack", "Alberto", "Dom"})
        self.assertEqual(
            parser.get('ordinal', _type=parser.PARAM_TYPES.NUMBER), 33)
        self.assertEqual(
            parser.get('number', _type=parser.PARAM_TYPES.NUMBER), 33)
        self.assertEqual(
            parser.get('other-ordinal', _type=parser.PARAM_TYPES.NUMBER), 33)
        self.assertEqual(
            parser.get('number-list', _type=parser.PARAM_TYPES.NUMBER), [2, 2])
        self.assertEqual(
            parser.get('names', _type=parser.PARAM_TYPES.LIST),
            ['Zack', 'Alberto', 'Dom', 'Martina'])
        self.assertEqual(
            parser.get('names2', _type=parser.PARAM_TYPES.LIST, split_char=','),
            ['Zack', 'Alberto', 'Dom', 'Martina'])

    def test_contexts(self):
        contexts = [
            {'name': 'c1', 'parameters': {'foo': 'bar'}, 'lifespan': 5},
            {'name': 'c2', 'parameters': {'bar': 'foo'}, 'lifespan': 5},
            {'name': 'c3', 'parameters': {'foobar': 42}, 'lifespan': 5},
        ]
        self.request['result']['contexts'] = contexts

        parser = GoogleAssistantParser(self.request)
        self.assertEqual(parser.get_contexts(), contexts)
        self.assertEqual(parser.get_contexts('c1'), {'foo': 'bar'})
        self.assertEqual(parser.get_contexts('c4'), {})

    def test_capabilities(self):
        self.request['originalRequest']['data']['surface']['capabilities'] = [
            {'name': 'actions.capability.AUDIO_OUTPUT'},
            {'name': 'actions.capability.SCREEN_OUTPUT'}
        ]
        parser = GoogleAssistantParser(self.request)
        self.assertTrue(parser.has_screen_capability())
        self.assertTrue(parser.has_audio_capability())

        self.request['originalRequest']['data']['surface']['capabilities'] = []
        parser = GoogleAssistantParser(self.request)
        self.assertFalse(parser.has_screen_capability())
        self.assertFalse(parser.has_audio_capability())

        self.request['originalRequest']['data'] = {}
        parser = GoogleAssistantParser(self.request)
        self.assertFalse(parser.has_screen_capability())
        self.assertFalse(parser.has_audio_capability())

    def test_user(self):
        user_name = 'foo bar'
        user_id = 'bar'
        self.request['originalRequest']['data']['user'] = {
            'profile': {'displayName': user_name,
                        'givenName': user_name.split(' ')[0],
                        'familyName': user_name.split(' ')[1]},
            'userId': user_id
        }

        parser = GoogleAssistantParser(self.request)
        self.assertEqual(parser.user.display_name, user_name)
        self.assertEqual(parser.user.given_name, user_name.split(' ')[0])
        self.assertEqual(parser.user.family_name, user_name.split(' ')[1])
        self.assertEqual(parser.user.id, user_id)

        # Make sure User is not re-initialized if payload is tinkered with
        self.request['originalRequest']['data']['user']['userName'] = user_name[::-1]
        self.assertEqual(parser.user.display_name, user_name)

    def test_device(self):
        device_id = 'bar'
        coordinates = {'latitude': 1, 'longitude': -1}
        zip_code = 'WC2H 8DY'
        phone_number = '07 42 42 4242 42'
        address = 'North wing, 9th floor, Central St Giles, London, UK'
        city = 'London'
        notes = 'gfit'

        self.request['originalRequest']['data']['device'] = {
            'location': {'coordinates': coordinates,
                         'zipCode': zip_code,
                         'city': city,
                         'phoneNumber': phone_number,
                         'formattedAddress': address,
                         'notes': notes},
            'uniqueDeviceId': device_id
        }

        parser = GoogleAssistantParser(self.request)
        self.assertEqual(parser.device.id, device_id)
        self.assertEqual(parser.device.coordinates, coordinates)
        self.assertEqual(parser.device.city, city)
        self.assertEqual(parser.device.phone_number, phone_number)
        self.assertEqual(parser.device.address, address)
        self.assertEqual(parser.device.zip_code, zip_code)
        self.assertEqual(parser.device.notes, notes)

    def test_location(self):
        device_id = 'bar'
        coordinates = {'latitude': 1, 'longitude': -1}
        zip_code = 'WC2H 8DY'
        phone_number = '07 42 42 4242 42'
        address = 'North wing, 9th floor, Central St Giles, London, UK'
        city = 'London'
        notes = 'gfit'

        self.request['originalRequest']['data']['device'] = {
            'location': {'coordinates': coordinates,
                         'zipCode': zip_code,
                         'city': city,
                         'phoneNumber': phone_number,
                         'formattedAddress': address,
                         'notes': notes},
            'uniqueDeviceId': device_id
        }

        parser = GoogleAssistantParser(self.request)
        self.assertEqual(parser.user.device.id, device_id)
        self.assertEqual(parser.user.device.coordinates, coordinates)
        self.assertEqual(parser.user.device.city, city)
        self.assertEqual(parser.user.device.phone_number, phone_number)
        self.assertEqual(parser.user.device.address, address)
        self.assertEqual(parser.user.device.zip_code, zip_code)
        self.assertEqual(parser.user.device.notes, notes)


class AmazonAlexaParserTestCase(unittest.TestCase):
    def setUp(self):
        self.request = get_dummy_amazon_request()

    def test_is_valid(self):
        parser = AmazonAlexaParser(self.request)
        self.assertTrue(parser.is_valid)

        parser.data = {}
        self.assertFalse(parser.is_valid)

    def test_action(self):
        action = 'foobar'
        self.request['request']['type'] = 'IntentRequest'
        self.request['request']['intent']['name'] = action

        parser = AmazonAlexaParser(self.request)
        self.assertEqual(parser.action, action)

    def test_no_action(self):
        self.request['request']['type'] = 'IntentRequest'
        self.request['request']['intent'] = {}

        parser = AmazonAlexaParser(self.request)
        self.assertEqual(parser.action, None)

    def test_action_launch_request(self):
        action = 'foobar'
        self.request['request']['type'] = 'LaunchRequest'
        self.request['request']['intent']['name'] = action

        parser = AmazonAlexaParser(self.request)
        self.assertNotEqual(parser.action, action)
        self.assertEqual(parser.action, WELCOME_ACTION)

    def test_parameters(self):
        self.request['request']['intent']['slots'] = {
            "given-name": {"value": "Zack"},
            "given-name2": {"value": "Alberto"},
            "given-name3": {"value": "Dom"},
            "ordinal": {"value": "33rd"},
            "number": {"value": "thirty-three"},
            "other-ordinal": {"value": "thirty third"},
            "number-list": {"value": ["2nd", "second"]},
            "names": {"value": "Zack Alberto Dom Martina"},
            "names2": {"value": "Zack,Alberto,Dom,Martina"}
        }

        parser = AmazonAlexaParser(self.request)
        self.assertEqual(parser.get('given-name'), "Zack")
        self.assertEqual(
            set(parser.get('given-name', globbing=True)),
            {"Zack", "Alberto", "Dom"})
        self.assertEqual(
            parser.get('ordinal', _type=parser.PARAM_TYPES.NUMBER), 33)
        self.assertEqual(
            parser.get('number', _type=parser.PARAM_TYPES.NUMBER), 33)
        self.assertEqual(
            parser.get('other-ordinal', _type=parser.PARAM_TYPES.NUMBER), 33)
        self.assertEqual(
            parser.get('number-list', _type=parser.PARAM_TYPES.NUMBER), [2, 2])
        self.assertEqual(
            parser.get('names', _type=parser.PARAM_TYPES.LIST),
            ['Zack', 'Alberto', 'Dom', 'Martina'])
        self.assertEqual(
            parser.get('names2', _type=parser.PARAM_TYPES.LIST, split_char=','),
            ['Zack', 'Alberto', 'Dom', 'Martina'])

    def test_contexts(self):
        # to do
        pass

    def test_capabilities(self):
        self.request['context']['System']['device']['supportedInterfaces'] = {
            "AudioPlayer": {},
            "Display": {}
        }

        parser = AmazonAlexaParser(self.request)
        self.assertTrue(parser.has_screen_capability())
        self.assertTrue(parser.has_audio_capability())

        self.request['context']['System']['device']['supportedInterfaces'] = {}
        parser = AmazonAlexaParser(self.request)
        self.assertFalse(parser.has_screen_capability())
        self.assertFalse(parser.has_audio_capability())

        self.request['context']['System'] = {}
        parser = AmazonAlexaParser(self.request)
        self.assertFalse(parser.has_screen_capability())
        self.assertFalse(parser.has_audio_capability())

    def test_user(self):
        user_id = 'bar'
        self.request['context']['System']['user'] = {
            'userId': user_id
        }

        parser = AmazonAlexaParser(self.request)
        self.assertEqual(parser.user.display_name, None)
        self.assertEqual(parser.user.given_name, None)
        self.assertEqual(parser.user.family_name, None)
        self.assertEqual(parser.user.id, user_id)

        # Make sure User is not re-initialized if payload is tinkered with
        self.request['context']['System'] = {}
        self.assertEqual(parser.user.id, user_id)

    def test_device(self):
        device_id = 'bar'
        self.request['context']['System']['device'] = {
            'deviceId': device_id
        }

        parser = AmazonAlexaParser(self.request)
        self.assertEqual(parser.device.id, device_id)


if __name__ == '__main__':
    unittest.main()

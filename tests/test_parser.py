import unittest

from apiaiassistant.parser import PayloadParser
from apiaiassistant.parser import GoogleAssistantParser

from tests import get_dummy_request


class PayloadParserTestCase(unittest.TestCase):
    def test_is_valid_not_implemented(self):
        parser = PayloadParser({})
        with self.assertRaises(NotImplementedError):
            parser.is_valid


class GoogleAssistantParserTestCase(unittest.TestCase):
    def setUp(self):
        self.request = get_dummy_request()

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
            "number-list": ["2nd", "second"]
        }

        parser = GoogleAssistantParser(self.request)
        self.assertEqual(parser.get('given-name'), "Zack")
        self.assertEqual(
            parser.get('given-name', globbing=True),
            ["Zack", "Alberto", "Dom"])
        self.assertEqual(
            parser.get('ordinal', _type=parser.PARAM_TYPES.NUMBER), 33)
        self.assertEqual(
            parser.get('number', _type=parser.PARAM_TYPES.NUMBER), 33)
        self.assertEqual(
            parser.get('other-ordinal', _type=parser.PARAM_TYPES.NUMBER), 33)
        self.assertEqual(
            parser.get('number-list', _type=parser.PARAM_TYPES.NUMBER), [2, 2])

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


if __name__ == '__main__':
    unittest.main()

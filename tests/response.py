import unittest

from apiai_assistant.agent import Agent
from apiai_assistant import response


FAKE_CORPUS = {
    "corpus": {'foo': ['bar']},
    "suggestions": {'confirmation': [['Yes', 'No']]}
}


class BaseResponseTestCase(unittest.TestCase):
    def test_to_dict(self):
        r = response.BaseResponse()
        payload = r.to_dict()
        self.assertTrue('messages' in payload)
        self.assertTrue('contextOut' not in payload)

        r.add_context({'foo': 'bar'})
        payload = r.to_dict()
        self.assertTrue('messages' in payload)
        self.assertTrue('contextOut' in payload)

    def test_add_context(self):
        r = response.BaseResponse()
        self.assertEqual(r._contexts, [])

        r.add_context({'foo': 'bar'})
        self.assertEqual(
            r._contexts,
            [{'foo': 'bar'}]
        )

        r.add_context({'bar': 'foo'}, 0)
        self.assertEqual(
            r._contexts,
            [{'bar': 'foo'}, {'foo': 'bar'}]
        )


class GoogleAssistantResponseTestCase(unittest.TestCase):
    def test_open_mic(self):
        r = response.GoogleAssistantResponse()
        self.assertFalse(r.to_dict()['data']['google']['expectUserResponse'])
        r.open_mic()
        self.assertTrue(r.to_dict()['data']['google']['expectUserResponse'])

    def test_close_mic(self):
        r = response.GoogleAssistantResponse()
        r.open_mic()
        self.assertTrue(r.to_dict()['data']['google']['expectUserResponse'])
        r.close_mic()
        self.assertFalse(r.to_dict()['data']['google']['expectUserResponse'])

    def test_add_message(self):
        r = response.GoogleAssistantResponse()
        self.assertEqual(r._messages, [r.initial_message])

        r.add_message({'foo': 'bar'})
        self.assertEqual(
            r._messages,
            [r.initial_message, {'foo': 'bar'}]
        )

        r.add_message({'bar': 'foo'}, 0)
        self.assertEqual(
            r._messages,
            [{'bar': 'foo'}, r.initial_message, {'foo': 'bar'}]
        )

    def test_add_permission(self):
        r = response.GoogleAssistantResponse()
        self.assertEqual(r._permissions, [])

        r.add_permission('because', [Agent.SupportedPermissions.NAME])
        self.assertEqual(
            r._permissions,
            [('because', [r.PERMISSIONS[Agent.SupportedPermissions.NAME]])]
        )

        r.add_permission('cause', [Agent.SupportedPermissions.NAME])
        self.assertEqual(
            r._permissions,
            [('because', [r.PERMISSIONS[Agent.SupportedPermissions.NAME]]),
             ('cause', [r.PERMISSIONS[Agent.SupportedPermissions.NAME]])]
        )

    def test_to_dict_permissions(self):
        r = response.GoogleAssistantResponse()
        r.add_permission('because', [Agent.SupportedPermissions.NAME])
        r.add_permission('cause', [Agent.SupportedPermissions.NAME])

        data = r.to_dict()['data']['google']['systemIntent']['data']
        self.assertEqual(
            data['permissions'],
            [r.PERMISSIONS[Agent.SupportedPermissions.NAME]])

        r.add_permission('because', [Agent.SupportedPermissions.COARSE_LOCATION,
                                     Agent.SupportedPermissions.PRECISE_LOCATION])
        data = r.to_dict()['data']['google']['systemIntent']['data']
        self.assertEqual(
            set(data['permissions']),
            {r.PERMISSIONS[Agent.SupportedPermissions.NAME],
             r.PERMISSIONS[Agent.SupportedPermissions.COARSE_LOCATION],
             r.PERMISSIONS[Agent.SupportedPermissions.PRECISE_LOCATION]})

if __name__ == '__main__':
    unittest.main()
